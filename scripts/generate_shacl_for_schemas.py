#!/usr/bin/env python3
"""Generate SHACL shapes from OpenAPI YAML files for grammar/shape validation.

This script takes a YAML file adhering to OpenAPI format (e.g., attributes.yaml)
and generates a corresponding shacl.jsonld file in the same directory.

Usage:
    python3 scripts/generate_shacl_for_schemas.py <yaml_file> [--dry-run]
    
Example:
    python3 scripts/generate_shacl_for_schemas.py schema/EnergyResource/v0.2/attributes.yaml
"""
import json
import yaml
import sys
from pathlib import Path
from typing import Optional

# Map OpenAPI types to XSD datatypes
type_map = {
    'string': 'http://www.w3.org/2001/XMLSchema#string',
    'integer': 'http://www.w3.org/2001/XMLSchema#integer',
    'int32': 'http://www.w3.org/2001/XMLSchema#int',
    'int64': 'http://www.w3.org/2001/XMLSchema#long',
    'number': 'http://www.w3.org/2001/XMLSchema#double',
    'float': 'http://www.w3.org/2001/XMLSchema#float',
    'boolean': 'http://www.w3.org/2001/XMLSchema#boolean',
    'date-time': 'http://www.w3.org/2001/XMLSchema#dateTime',
    'date': 'http://www.w3.org/2001/XMLSchema#date',
}

def get_iri(name: str, vocab_base: str) -> str:
    """Get IRI for a schema or property name"""
    return f"{vocab_base}{name}"

def get_property_iri(prop_name: str, vocab_base: str, context: dict) -> str:
    """Get IRI for a property from context or construct from vocab_base"""
    # Check if property is in context
    if prop_name in context.get('@context', {}):
        prop_iri = context['@context'][prop_name]
        if isinstance(prop_iri, dict):
            return prop_iri.get('@id', f"{vocab_base}{prop_name}")
        return prop_iri
    return f"{vocab_base}{prop_name}"

def convert_property(prop_name: str, prop_def: dict, required_fields: list, 
                     all_schemas: dict, vocab_base: str, context: dict):
    """Convert an OpenAPI property to SHACL property shape"""
    prop_iri = get_property_iri(prop_name, vocab_base, context)
    
    prop_shape = {
        'sh:path': prop_iri,
        'sh:name': prop_name
    }
    
    # Handle required
    if prop_name in required_fields:
        prop_shape['sh:minCount'] = 1
    
    # Handle nullable
    if prop_def.get('nullable', False):
        prop_shape['sh:maxCount'] = 1  # Allow 0 or 1
    
    # Handle $ref first
    if '$ref' in prop_def:
        ref = prop_def['$ref']
        if ref.startswith('#/components/schemas/'):
            ref_name = ref.split('/')[-1]
            prop_shape['sh:class'] = get_iri(ref_name, vocab_base)
        return prop_shape
    
    # Handle type
    prop_type = prop_def.get('type')
    
    # Handle array type
    if prop_type == 'array':
        items = prop_def.get('items', {})
        if '$ref' in items:
            ref = items['$ref']
            if ref.startswith('#/components/schemas/'):
                ref_name = ref.split('/')[-1]
                prop_shape['sh:nodeKind'] = 'sh:IRIOrLiteral'
                prop_shape['sh:class'] = get_iri(ref_name, vocab_base)
        else:
            item_type = items.get('type')
            if item_type in type_map:
                prop_shape['sh:datatype'] = type_map[item_type]
            elif item_type == 'object':
                prop_shape['sh:nodeKind'] = 'sh:IRIOrLiteral'
        return prop_shape
    
    # Handle format before type (format can override)
    if 'format' in prop_def:
        format_type = prop_def['format']
        if format_type in type_map:
            prop_shape['sh:datatype'] = type_map[format_type]
        elif prop_type in type_map:
            prop_shape['sh:datatype'] = type_map[prop_type]
    elif prop_type in type_map:
        prop_shape['sh:datatype'] = type_map[prop_type]
    elif prop_type == 'object':
        prop_shape['sh:nodeKind'] = 'sh:IRIOrLiteral'
    
    # Handle enum
    if 'enum' in prop_def:
        enum_values = prop_def['enum']
        # sh:in expects a list of values
        prop_shape['sh:in'] = enum_values
    
    # Handle minimum/maximum for numbers
    if 'minimum' in prop_def:
        prop_shape['sh:minInclusive'] = prop_def['minimum']
    if 'maximum' in prop_def:
        prop_shape['sh:maxInclusive'] = prop_def['maximum']
    
    return prop_shape

def convert_schema(schema_name: str, schema_def: dict, all_schemas: dict, 
                   vocab_base: str, context: dict):
    """Convert an OpenAPI schema to a SHACL NodeShape"""
    shape_iri = get_iri(schema_name, vocab_base)
    
    # Check if schema has a specific IRI in context
    if schema_name in context.get('@context', {}):
        shape_iri = context['@context'][schema_name]
        if isinstance(shape_iri, str):
            pass  # Use as is
        elif isinstance(shape_iri, dict):
            shape_iri = shape_iri.get('@id', shape_iri)
    
    shape = {
        '@id': shape_iri,
        '@type': 'sh:NodeShape',
        'sh:targetClass': shape_iri,
        'sh:name': schema_name
    }
    
    properties = []
    required_fields = schema_def.get('required', [])
    props = schema_def.get('properties', {})
    
    for prop_name, prop_def in props.items():
        try:
            prop_shape = convert_property(prop_name, prop_def, required_fields, 
                                         all_schemas, vocab_base, context)
            if prop_shape:
                properties.append(prop_shape)
        except Exception as e:
            print(f"Error converting property {prop_name} in {schema_name}: {e}", file=sys.stderr)
            continue
    
    if properties:
        shape['sh:property'] = properties
    
    return shape

def get_vocab_base_from_context(context_path: Path) -> Optional[str]:
    """Extract vocab base IRI from context.jsonld"""
    if not context_path.exists():
        return None
    
    try:
        with open(context_path) as f:
            context = json.load(f)
        
        # Try to get @vocab from context
        ctx = context.get('@context', {})
        if '@vocab' in ctx:
            return ctx['@vocab']
        
        # Try to infer from beckn prefix
        if 'beckn' in ctx:
            beckn_val = ctx['beckn']
            if isinstance(beckn_val, str):
                # Remove trailing # or / to get base
                base = beckn_val.rstrip('#/')
                return base + '/'
        
        return None
    except Exception as e:
        print(f"Warning: Could not read context from {context_path}: {e}", file=sys.stderr)
        return None

def generate_shacl_for_file(attributes_path: Path, dry_run: bool = False) -> bool:
    """Generate SHACL shapes from an attributes.yaml file"""
    if not attributes_path.exists():
        print(f"Error: File not found: {attributes_path}", file=sys.stderr)
        return False
    
    schema_dir = attributes_path.parent
    context_path = schema_dir / 'context.jsonld'
    output_path = schema_dir / 'shacl.jsonld'
    
    # Load context to get IRIs
    vocab_base = get_vocab_base_from_context(context_path)
    if not vocab_base:
        # Fallback: construct from folder structure
        parts = schema_dir.parts
        schema_idx = -1
        for i, part in enumerate(parts):
            if part.startswith('Energy') or part.startswith('EvCharging'):
                schema_idx = i
                break
        
        if schema_idx >= 0:
            schema_name = parts[schema_idx]
            vocab_base = f"https://schemas.beckn.org/{schema_name.lower()}/"
        else:
            vocab_base = "https://schemas.beckn.org/"
    
    # Load context for property IRIs
    context = {}
    if context_path.exists():
        try:
            with open(context_path) as f:
                context = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load context: {e}", file=sys.stderr)
    
    # Load attributes.yaml
    try:
        with open(attributes_path) as f:
            spec = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Could not load {attributes_path}: {e}", file=sys.stderr)
        return False
    
    schemas = spec.get('components', {}).get('schemas', {})
    
    if not schemas:
        print(f"Warning: No schemas found in {attributes_path}", file=sys.stderr)
        return False
    
    # Generate SHACL shapes
    shapes = []
    for schema_name, schema_def in schemas.items():
        if schema_def.get('type') == 'object':
            try:
                shape = convert_schema(schema_name, schema_def, schemas, vocab_base, context)
                shapes.append(shape)
            except Exception as e:
                print(f"Error converting schema {schema_name}: {e}", file=sys.stderr)
                continue
    
    if not shapes:
        print(f"Warning: No shapes generated for {attributes_path}", file=sys.stderr)
        return False
    
    if dry_run:
        print(f"[DRY RUN] Would generate {output_path} with {len(shapes)} shape(s)")
        print(f"  Base IRI: {vocab_base}")
        return True
    
    # Create SHACL document
    shacl_doc = {
        '@context': {
            '@version': 1.1,
            'sh': 'http://www.w3.org/ns/shacl#',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'vocab': vocab_base
        },
        '@graph': shapes
    }
    
    # Write to file
    try:
        with open(output_path, 'w') as f:
            json.dump(shacl_doc, f, indent=2)
            f.write('\n')
        print(f"✓ Generated {output_path} with {len(shapes)} shape(s)")
        print(f"  Base IRI: {vocab_base}")
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}", file=sys.stderr)
        return False

def find_schema_files(repo_root: Path) -> list[Path]:
    """Find all attributes.yaml files under Energy* and EvCharging* folders"""
    schema_dir = repo_root / 'schema'
    if not schema_dir.exists():
        return []
    
    files = []
    for pattern in ['Energy*', 'EvCharging*']:
        for folder in schema_dir.glob(pattern):
            for attributes_file in folder.rglob('attributes.yaml'):
                files.append(attributes_file)
    
    return sorted(files)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate SHACL shapes from OpenAPI attributes.yaml files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate SHACL for a specific attributes.yaml file
  python3 scripts/generate_shacl_for_schemas.py schema/EnergyResource/v0.2/attributes.yaml

  # Dry run to see what would be generated
  python3 scripts/generate_shacl_for_schemas.py schema/EnergyResource/v0.2/attributes.yaml --dry-run
        """
    )
    parser.add_argument(
        'yaml_file',
        type=Path,
        help='Path to YAML file adhering to OpenAPI format (e.g., attributes.yaml)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without writing files'
    )
    
    args = parser.parse_args()
    
    # Determine repo root (parent of scripts directory)
    repo_root = Path(__file__).resolve().parent.parent
    
    # Process the provided YAML file
    yaml_path = Path(args.yaml_file)
    if not yaml_path.is_absolute():
        # Try relative to current directory first, then repo root
        if not yaml_path.exists():
            yaml_path = repo_root / yaml_path
    
    if not yaml_path.exists():
        print(f"Error: File not found: {args.yaml_file}", file=sys.stderr)
        return 1
    
    success = generate_shacl_for_file(yaml_path, dry_run=args.dry_run)
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())

