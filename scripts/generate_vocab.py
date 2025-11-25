#!/usr/bin/env python3
"""Generate JSON-LD vocabulary (vocab.jsonld) from OpenAPI spec.yaml including all schemas and enum values.

This script generates a full vocabulary file with:
- All schema types as classes
- All enum types as schema:Enumeration
- All enum values as individual entities

Usage:
    python3 scripts/generate_vocab.py <spec.yaml> [base_iri] [--output OUTPUT] [--pretty]

Examples:
    # Basic usage - uses base IRI inferred from folder structure
    python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml

    # Specify base IRI
    python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml https://schemas.ocpp.org/2.0.1/

    # Custom output file
    python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml -o custom_vocab.jsonld

    # Pretty-printed output
    python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml --pretty
"""
import json
import yaml
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Tuple

def get_base_iri(spec_path: Path, base_iri: Optional[str] = None) -> str:
    """Determine base IRI from path or provided value"""
    if base_iri:
        if base_iri.startswith('http://') or base_iri.startswith('https://'):
            return base_iri if base_iri.endswith('/') else base_iri + '/'
    
    # Infer from folder structure
    # Check parent directories for schema name and version
    parts = spec_path.parent.parts
    schema_name = None
    version = None
    
    for part in parts:
        if part.startswith('ocpi'):
            return "https://schemas.ocpi.org/2.2/"
        elif part.startswith('ocpp'):
            # Extract version from path
            for p in parts:
                if p.startswith('v') and '.' in p:
                    # Remove 'v' prefix if present (e.g., v2.1.0 -> 2.1.0)
                    version = p[1:] if p.startswith('v') else p
                elif p.startswith('2.') or p.startswith('1.'):
                    version = p
            if version:
                return f"https://schemas.ocpp.org/{version}/"
            return "https://schemas.ocpp.org/2.0.1/"
        elif part.startswith('Energy') or part.startswith('EvCharging'):
            schema_name = part
        elif part.startswith('v') and '.' in part:
            version = part
    
    if schema_name and version:
        return f"https://schemas.beckn.org/{schema_name}/{version}/"
    elif schema_name:
        return f"https://schemas.beckn.org/{schema_name}/"
    
    # Fallback
    folder_name = spec_path.parent.name
    return f"https://schemas.{folder_name}/"

def sanitize_enum_value(value: str) -> str:
    """Sanitize enum value to be a valid identifier"""
    # Replace problematic characters
    value = value.replace('.', '_')
    value = value.replace('-', '_')
    value = value.replace('/', '_')
    value = value.replace(' ', '_')
    return value

def get_prefix(spec_path: Path) -> str:
    """Determine prefix name from path (e.g., 'ocpp', 'ocpi', 'beckn')"""
    parts = spec_path.parent.parts
    for part in parts:
        if part.startswith('ocpi'):
            return 'ocpi'
        elif part.startswith('ocpp'):
            return 'ocpp'
        elif part.startswith('Energy') or part.startswith('EvCharging'):
            return 'beckn'
    return 'vocab'

def get_enum_value_id(enum_type_name: str, enum_value: str, prefix: str) -> str:
    """Generate compact IRI for an enum value (e.g., ocpp:cType2)"""
    return f"{prefix}:{enum_value}"

def get_schema_id(schema_name: str, prefix: str) -> str:
    """Generate compact IRI for a schema (e.g., ocpp:ConnectorEnumType)"""
    return f"{prefix}:{schema_name}"

def generate_vocab(spec_path: Path, base_iri: Optional[str] = None, 
                   output_path: Optional[Path] = None, pretty: bool = False) -> Path:
    """
    Generate JSON-LD vocabulary from OpenAPI spec.yaml
    
    Args:
        spec_path: Path to spec.yaml file
        base_iri: Base IRI for the vocabulary (optional)
        output_path: Output file path (optional, defaults to vocab.jsonld in same directory)
        pretty: Whether to pretty-print JSON output
    """
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")
    
    # Load spec
    with open(spec_path) as f:
        spec = yaml.safe_load(f)
    
    schemas = spec.get('components', {}).get('schemas', {})
    
    # Determine base IRI and prefix
    vocab_base = get_base_iri(spec_path, base_iri)
    prefix = get_prefix(spec_path)
    
    # Build vocabulary graph
    graph = []
    enum_types = {}  # Track enum types and their values
    
    # First pass: collect all enum types from top-level schemas
    for schema_name, schema_def in schemas.items():
        if schema_def.get('type') == 'string' and 'enum' in schema_def:
            enum_values = schema_def.get('enum', [])
            enum_types[schema_name] = {
                'values': enum_values,
                'description': schema_def.get('description', ''),
                'schema': schema_def
            }
    
    # Also collect enum types from properties within object schemas
    # (e.g., Connector.connector_standard -> ConnectorStandardEnumType)
    for schema_name, schema_def in schemas.items():
        if schema_def.get('type') == 'object' and 'properties' in schema_def:
            for prop_name, prop_def in schema_def.get('properties', {}).items():
                if prop_def.get('type') == 'string' and 'enum' in prop_def:
                    # Create enum type name from property (e.g., connector_standard -> ConnectorStandardEnumType)
                    enum_type_name = ''.join(word.capitalize() for word in prop_name.split('_')) + 'EnumType'
                    enum_values = prop_def.get('enum', [])
                    
                    # Only add if not already exists (prefer top-level schema if it exists)
                    if enum_type_name not in enum_types:
                        enum_types[enum_type_name] = {
                            'values': enum_values,
                            'description': prop_def.get('description', f'Enumeration for {prop_name}'),
                            'schema': prop_def,
                            'property_name': prop_name,
                            'parent_schema': schema_name
                        }
    
    # Second pass: generate vocabulary entries for schemas
    for schema_name, schema_def in schemas.items():
        schema_id = get_schema_id(schema_name, prefix)
        
        # Determine schema type
        schema_type = schema_def.get('type', 'object')
        
        if schema_type == 'string' and 'enum' in schema_def:
            # Enum type
            enum_values = schema_def.get('enum', [])
            description = schema_def.get('description', '')
            
            # Create enum type entry
            enum_type_entry = {
                "@id": schema_id,
                "@type": "schema:Enumeration",
                "schema:name": schema_name,
            }
            
            if description:
                enum_type_entry["rdfs:comment"] = description
            
            # Add enum members
            enum_members = []
            for enum_value in enum_values:
                enum_value_id = get_enum_value_id(schema_name, enum_value, prefix)
                enum_members.append({"@id": enum_value_id})
            
            if enum_members:
                enum_type_entry["schema:hasEnumerationMember"] = enum_members
            
            graph.append(enum_type_entry)
            
            # Create individual enum value entries
            for enum_value in enum_values:
                enum_value_id = get_enum_value_id(schema_name, enum_value, prefix)
                
                enum_value_entry = {
                    "@id": enum_value_id,
                    "@type": [
                        schema_id,  # The enum type
                        "schema:Enumeration"
                    ],
                    "schema:name": enum_value,
                    "schema:identifier": enum_value
                }
                
                graph.append(enum_value_entry)
        
        elif schema_type == 'object':
            # Object/Class type
            description = schema_def.get('description', '')
            
            class_entry = {
                "@id": schema_id,
                "@type": "rdfs:Class",
                "rdfs:label": schema_name,
            }
            
            if description:
                class_entry["rdfs:comment"] = description
            
            graph.append(class_entry)
    
    # Third pass: generate vocabulary entries for enum types found in properties
    for enum_type_name, enum_info in enum_types.items():
        # Skip if already processed as a top-level schema
        if enum_type_name in schemas:
            continue
        
        schema_id = get_schema_id(enum_type_name, prefix)
        enum_values = enum_info['values']
        description = enum_info['description']
        
        # Create enum type entry
        enum_type_entry = {
            "@id": schema_id,
            "@type": "schema:Enumeration",
            "schema:name": enum_type_name,
        }
        
        if description:
            enum_type_entry["rdfs:comment"] = description
        
        # Add enum members
        enum_members = []
        for enum_value in enum_values:
            enum_value_id = get_enum_value_id(enum_type_name, enum_value, prefix)
            enum_members.append({"@id": enum_value_id})
        
        if enum_members:
            enum_type_entry["schema:hasEnumerationMember"] = enum_members
        
        graph.append(enum_type_entry)
        
        # Create individual enum value entries
        for enum_value in enum_values:
            enum_value_id = get_enum_value_id(enum_type_name, enum_value, prefix)
            
            enum_value_entry = {
                "@id": enum_value_id,
                "@type": [
                    schema_id,  # The enum type
                    "schema:Enumeration"
                ],
                "schema:name": enum_value,
                "schema:identifier": enum_value
            }
            
            graph.append(enum_value_entry)
    
    # Create vocab document with prefix mapping in context
    vocab_doc = {
        "@context": {
            "@version": 1.1,
            prefix: vocab_base,  # Map prefix to base IRI (e.g., "ocpp": "https://schemas.ocpp.org/2.0.1/")
            "schema": "https://schema.org/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        },
        "@graph": graph
    }
    
    # Determine output path
    if output_path is None:
        output_path = spec_path.parent / 'vocab.jsonld'
    elif not output_path.is_absolute():
        output_path = spec_path.parent / output_path
    
    # Write to file
    with open(output_path, 'w') as f:
        if pretty:
            json.dump(vocab_doc, f, indent=2, ensure_ascii=False)
            f.write('\n')
        else:
            json.dump(vocab_doc, f, separators=(',', ':'), ensure_ascii=False)
    
    enum_count = sum(len(et['values']) for et in enum_types.values())
    print(f"✓ Generated {output_path}")
    print(f"  Base IRI: {vocab_base}")
    print(f"  Total entries: {len(graph)}")
    print(f"  Enum types: {len(enum_types)}")
    print(f"  Enum values: {enum_count}")
    print(f"  Format: {'Pretty-printed' if pretty else 'Minified'}")
    
    return output_path

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate JSON-LD vocabulary from OpenAPI YAML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - uses base IRI inferred from folder structure
  python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml

  # Specify base IRI
  python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml https://schemas.ocpp.org/2.0.1/

  # Custom output file
  python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml -o custom_vocab.jsonld

  # Pretty-printed output
  python3 scripts/generate_vocab.py schema/ocpp/2.0.1/spec.yaml --pretty
        """
    )
    parser.add_argument(
        'spec_file',
        type=Path,
        help='Path to YAML file adhering to OpenAPI format'
    )
    parser.add_argument(
        'base_iri',
        type=str,
        nargs='?',
        default=None,
        help='Base IRI for vocabulary (optional, will be inferred from folder structure)'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output file path (default: vocab.jsonld in same directory)'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output with indentation (default: minified)'
    )
    
    args = parser.parse_args()
    
    # Determine repo root (parent of scripts directory)
    repo_root = Path(__file__).resolve().parent.parent
    
    # Process the provided YAML file
    spec_path = Path(args.spec_file)
    if not spec_path.is_absolute():
        if not spec_path.exists():
            spec_path = repo_root / spec_path
    
    if not spec_path.exists():
        print(f"Error: File not found: {args.spec_file}", file=sys.stderr)
        return 1
    
    try:
        generate_vocab(
            spec_path=spec_path,
            base_iri=args.base_iri,
            output_path=args.output,
            pretty=args.pretty
        )
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())

