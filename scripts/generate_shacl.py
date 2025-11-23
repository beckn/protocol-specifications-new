#!/usr/bin/env python3
"""Generate SHACL shapes from OpenAPI YAML files for grammar/shape validation.

This script works with any OpenAPI YAML file (spec.yaml, attributes.yaml, etc.)
and generates a corresponding shacl_{filename}.jsonld file.

Usage:
    python3 scripts/generate_shacl.py <yaml_file> [context.jsonld] [base_iri] [--output OUTPUT] [--pretty] [--dry-run]

Examples:
    # Basic usage - uses context.jsonld from same directory
    python3 scripts/generate_shacl.py schema/ocpi/2.2/spec.yaml

    # Specify context and base IRI
    python3 scripts/generate_shacl.py schema/EnergyResource/v0.2/attributes.yaml schema/EnergyResource/v0.2/context.jsonld

    # Custom output file
    python3 scripts/generate_shacl.py schema/ocpp/2.0.1/spec.yaml -o custom_shacl.jsonld

    # Pretty-printed output
    python3 scripts/generate_shacl.py schema/ocpi/2.2/spec.yaml --pretty
"""
import json
import yaml
import sys
import argparse
from pathlib import Path
from typing import Optional

# Map OpenAPI types to XSD datatypes (using CURIEs)
type_map = {
    'string': 'xsd:string',
    'integer': 'xsd:integer',
    'int32': 'xsd:int',
    'int64': 'xsd:long',
    'number': 'xsd:double',
    'float': 'xsd:float',
    'boolean': 'xsd:boolean',
    'date-time': 'xsd:dateTime',
    'date': 'xsd:date',
}

def get_iri(name: str, vocab_base: str) -> str:
    """Get IRI for a schema or property name"""
    return f"{vocab_base}{name}"

def get_curie(name: str, vocab_prefix: str = "vocab") -> str:
    """Get CURIE for a schema or property name"""
    return f"{vocab_prefix}:{name}"

def get_schema_iri(schema_name: str, vocab_base: str, context: dict, use_curie: bool = True) -> str:
    """Get IRI or CURIE for a schema, handling JSON-LD @id keyword"""
    if use_curie:
        # Use CURIE format: vocab:SchemaName
        return get_curie(schema_name)
    
    # Otherwise, return full IRI (for backward compatibility)
    # Check if schema has a specific IRI in context
    if schema_name in context.get('@context', {}):
        shape_iri_raw = context['@context'][schema_name]
        if isinstance(shape_iri_raw, str):
            # Handle JSON-LD keyword "@id" - means use @vocab + term name
            if shape_iri_raw == "@id":
                return get_iri(schema_name, vocab_base)
            # If it's a relative path like "./vocab.jsonld#", use vocab_base
            if shape_iri_raw.startswith('./'):
                return get_iri(schema_name, vocab_base)
            # If it's a compact IRI, expand it
            if ':' in shape_iri_raw and not shape_iri_raw.startswith('http'):
                prefix, local = shape_iri_raw.split(':', 1)
                ctx = context.get('@context', {})
                if prefix in ctx:
                    base = ctx[prefix]
                    if isinstance(base, str):
                        # Handle relative paths in base - always use vocab_base for absolute IRI
                        if base.startswith('./'):
                            return get_iri(local, vocab_base)
                        # Ensure base is absolute (starts with http)
                        if base.startswith('http://') or base.startswith('https://'):
                            base = base.rstrip('#/')
                            return f"{base}/{local}" if not base.endswith('/') else f"{base}{local}"
                        # If base is not absolute, fall back to vocab_base
                        return get_iri(local, vocab_base)
            # If it's not a compact IRI and not absolute, ensure it's absolute
            if not shape_iri_raw.startswith('http://') and not shape_iri_raw.startswith('https://'):
                return get_iri(schema_name, vocab_base)
            return shape_iri_raw
        elif isinstance(shape_iri_raw, dict):
            iri = shape_iri_raw.get('@id', get_iri(schema_name, vocab_base))
            if iri == "@id" or (isinstance(iri, str) and iri.startswith('./')):
                return get_iri(schema_name, vocab_base)
            return iri
    
    return get_iri(schema_name, vocab_base)

def get_property_iri(prop_name: str, vocab_base: str, context: dict, use_curie: bool = True) -> str:
    """Get IRI or CURIE for a property from context or construct from vocab_base"""
    if use_curie:
        # Check if property maps to an external IRI (like schema:name, ieee:mRID)
        if prop_name in context.get('@context', {}):
            prop_iri = context['@context'][prop_name]
            if isinstance(prop_iri, dict):
                iri = prop_iri.get('@id', None)
            else:
                iri = prop_iri
            
            # If it's a compact IRI, check if it's from an external namespace
            if isinstance(iri, str) and ':' in iri and not iri.startswith('http'):
                prefix, local = iri.split(':', 1)
                ctx = context.get('@context', {})
                # If prefix is 'beckn' and it maps to a relative path, use vocab: instead
                if prefix == 'beckn' and prefix in ctx:
                    beckn_val = ctx[prefix]
                    if isinstance(beckn_val, str) and beckn_val.startswith('./'):
                        # This is a vocab property, use vocab: prefix
                        return get_curie(prop_name)
                # Otherwise, it's an external namespace (schema:, ieee:, etc.), use as is
                return iri
            # If it's a full external IRI, keep it as is
            if isinstance(iri, str) and (iri.startswith('http://') or iri.startswith('https://')):
                return iri
            # Otherwise, use vocab prefix
            return get_curie(prop_name)
        return get_curie(prop_name)
    
    # Otherwise, return full IRI (for backward compatibility)
    # Check if property is in context
    if prop_name in context.get('@context', {}):
        prop_iri = context['@context'][prop_name]
        if isinstance(prop_iri, dict):
            iri = prop_iri.get('@id', f"{vocab_base}{prop_name}")
        else:
            iri = prop_iri
        
        # Handle JSON-LD keyword "@id" - means use @vocab + term name
        if iri == "@id":
            return f"{vocab_base}{prop_name}"
        
        # If it's a relative path like "./vocab.jsonld#", use vocab_base
        if isinstance(iri, str) and iri.startswith('./'):
            return f"{vocab_base}{prop_name}"
        
        # If it's a compact IRI, expand it
        if isinstance(iri, str) and ':' in iri and not iri.startswith('http'):
            prefix, local = iri.split(':', 1)
            ctx = context.get('@context', {})
            if prefix in ctx:
                base = ctx[prefix]
                if isinstance(base, str):
                    # Handle relative paths in base - always use vocab_base for absolute IRI
                    if base.startswith('./'):
                        return f"{vocab_base}{local}"
                    # Ensure base is absolute (starts with http)
                    if base.startswith('http://') or base.startswith('https://'):
                        base = base.rstrip('#/')
                        return f"{base}/{local}" if not base.endswith('/') else f"{base}{local}"
                    # If base is not absolute, fall back to vocab_base
                    return f"{vocab_base}{local}"
        
        # If it's not a compact IRI and not absolute, ensure it's absolute
        if isinstance(iri, str) and not iri.startswith('http://') and not iri.startswith('https://'):
            return f"{vocab_base}{prop_name}"
        
        return iri
    
    return f"{vocab_base}{prop_name}"

def convert_property(prop_name: str, prop_def: dict, required_fields: list, 
                     all_schemas: dict, vocab_base: str, context: dict, use_curie: bool = True):
    """Convert an OpenAPI property to SHACL property shape"""
    prop_iri = get_property_iri(prop_name, vocab_base, context, use_curie)
    
    prop_shape = {
        'sh:path': prop_iri,
        'sh:name': prop_name
    }
    
    # Handle required
    if prop_name in required_fields:
        prop_shape['sh:minCount'] = 1
    
    # Handle nullable
    if prop_def.get('nullable', False):
        prop_shape['sh:maxCount'] = 1
    
    # Handle $ref first
    if '$ref' in prop_def:
        ref = prop_def['$ref']
        if ref.startswith('#/components/schemas/'):
            ref_name = ref.split('/')[-1]
            ref_iri = get_schema_iri(ref_name, vocab_base, context, use_curie)
            
            # Look up the referenced schema to check for enum values
            if ref_name in all_schemas:
                ref_schema = all_schemas[ref_name]
                
                # If the referenced schema has enum values, add sh:in
                if 'enum' in ref_schema:
                    enum_values = ref_schema['enum']
                    prop_shape['sh:in'] = enum_values
                
                # If the referenced schema has a type, add datatype
                ref_type = ref_schema.get('type')
                if ref_type in type_map:
                    prop_shape['sh:datatype'] = type_map[ref_type]
                
                # Only add sh:class if it's an object type (not a simple enum type)
                if ref_type == 'object':
                    prop_shape['sh:class'] = ref_iri
            else:
                # Fallback: if schema not found, just use sh:class
                prop_shape['sh:class'] = ref_iri
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
                ref_iri = get_schema_iri(ref_name, vocab_base, context, use_curie)
                prop_shape['sh:nodeKind'] = 'sh:IRIOrLiteral'
                prop_shape['sh:class'] = ref_iri
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
        prop_shape['sh:in'] = enum_values
    
    # Handle minimum/maximum for numbers
    if 'minimum' in prop_def:
        prop_shape['sh:minInclusive'] = prop_def['minimum']
    if 'maximum' in prop_def:
        prop_shape['sh:maxInclusive'] = prop_def['maximum']
    
    return prop_shape

def convert_schema(schema_name: str, schema_def: dict, all_schemas: dict, 
                   vocab_base: str, context: dict, use_curie: bool = True):
    """Convert an OpenAPI schema to a SHACL NodeShape"""
    shape_iri = get_schema_iri(schema_name, vocab_base, context, use_curie)
    
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
                                         all_schemas, vocab_base, context, use_curie)
            if prop_shape:
                properties.append(prop_shape)
        except Exception as e:
            print(f"Error converting property {prop_name} in {schema_name}: {e}", file=sys.stderr)
            continue
    
    if properties:
        shape['sh:property'] = properties
    
    return shape

def get_vocab_base(context_path: Optional[Path], base_iri: Optional[str], spec_path: Path) -> str:
    """Get vocab base IRI from context, base_iri, or infer from folder structure.
    Always returns an absolute IRI (starts with http:// or https://).
    """
    # Use provided base_iri if it's absolute
    if base_iri:
        if base_iri.startswith('http://') or base_iri.startswith('https://'):
            return base_iri if base_iri.endswith('/') else base_iri + '/'
        # If base_iri is relative, we'll infer from folder structure instead
    
    # Try context file first
    if context_path and context_path.exists():
        try:
            with open(context_path) as f:
                context = json.load(f)
            ctx = context.get('@context', {})
            
            # Try @vocab first (must be absolute)
            if '@vocab' in ctx:
                vocab = ctx['@vocab']
                if isinstance(vocab, str) and (vocab.startswith('http://') or vocab.startswith('https://')):
                    return vocab if vocab.endswith('/') else vocab + '/'
            
            # Try to infer from beckn prefix
            if 'beckn' in ctx:
                beckn_val = ctx['beckn']
                if isinstance(beckn_val, str):
                    # If relative path, infer from folder structure with version
                    if beckn_val.startswith('./'):
                        parts = spec_path.parent.parts
                        schema_name = None
                        version = None
                        for i, part in enumerate(parts):
                            if part.startswith('Energy') or part.startswith('EvCharging'):
                                schema_name = part  # Keep original case
                            elif part.startswith('v') and '.' in part:
                                version = part
                        if schema_name and version:
                            return f"https://schemas.beckn.org/{schema_name}/{version}/"
                        elif schema_name:
                            return f"https://schemas.beckn.org/{schema_name}/"
                    # If absolute, use it
                    elif beckn_val.startswith('http://') or beckn_val.startswith('https://'):
                        base = beckn_val.rstrip('#/')
                        return base + '/' if not base.endswith('/') else base
        except Exception as e:
            print(f"Warning: Could not read context: {e}", file=sys.stderr)
    
    # Infer from folder structure (always returns absolute IRI)
    parts = spec_path.parent.parts
    schema_name = None
    version = None
    for i, part in enumerate(parts):
        if part.startswith('ocpi'):
            return "https://schemas.ocpi.org/2.2/"
        elif part.startswith('ocpp'):
            return "https://schemas.ocpp.org/2.0.1/"
        elif part.startswith('Energy') or part.startswith('EvCharging'):
            schema_name = part  # Keep original case
        elif part.startswith('v') and '.' in part:
            version = part
    
    if schema_name and version:
        return f"https://schemas.beckn.org/{schema_name}/{version}/"
    elif schema_name:
        return f"https://schemas.beckn.org/{schema_name}/"
    
    # Fallback (always absolute)
    folder_name = spec_path.parent.name
    return f"https://schemas.beckn.org/{folder_name}/"

def generate_shacl(yaml_path: Path, context_path: Optional[Path] = None, 
                   base_iri: Optional[str] = None, output_path: Optional[Path] = None,
                   pretty: bool = False, dry_run: bool = False) -> bool:
    """Generate SHACL shapes from an OpenAPI YAML file"""
    if not yaml_path.exists():
        print(f"Error: File not found: {yaml_path}", file=sys.stderr)
        return False
    
    schema_dir = yaml_path.parent
    
    # Determine context path
    if context_path is None:
        context_path = schema_dir / 'context.jsonld'
    
    # Get vocab base
    vocab_base = get_vocab_base(context_path, base_iri, yaml_path)
    
    # Load context for property IRIs
    context = {}
    if context_path and context_path.exists():
        try:
            with open(context_path) as f:
                context = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load context: {e}", file=sys.stderr)
    
    # Load YAML
    try:
        with open(yaml_path) as f:
            spec = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: Could not load {yaml_path}: {e}", file=sys.stderr)
        return False
    
    schemas = spec.get('components', {}).get('schemas', {})
    
    if not schemas:
        print(f"Warning: No schemas found in {yaml_path}", file=sys.stderr)
        return False
    
    # Generate SHACL shapes
    shapes = []
    for schema_name, schema_def in schemas.items():
        if schema_def.get('type') == 'object':
            try:
                shape = convert_schema(schema_name, schema_def, schemas, vocab_base, context, use_curie=True)
                shapes.append(shape)
            except Exception as e:
                print(f"Error converting schema {schema_name}: {e}", file=sys.stderr)
                continue
    
    if not shapes:
        print(f"Warning: No shapes generated for {yaml_path}", file=sys.stderr)
        return False
    
    # Determine output path
    if output_path is None:
        input_stem = yaml_path.stem
        output_path = schema_dir / f'shacl_{input_stem}.jsonld'
    elif not output_path.is_absolute():
        output_path = schema_dir / output_path
    
    if dry_run:
        print(f"[DRY RUN] Would generate {output_path} with {len(shapes)} shape(s)")
        print(f"  Base IRI: {vocab_base}")
        print(f"  Format: {'Pretty-printed' if pretty else 'Minified'}")
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
            if pretty:
                json.dump(shacl_doc, f, indent=2, ensure_ascii=False)
                f.write('\n')
            else:
                json.dump(shacl_doc, f, separators=(',', ':'), ensure_ascii=False)
        print(f"✓ Generated {output_path} with {len(shapes)} shape(s)")
        print(f"  Base IRI: {vocab_base}")
        print(f"  Format: {'Pretty-printed' if pretty else 'Minified'}")
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}", file=sys.stderr)
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate SHACL shapes from OpenAPI YAML files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - uses context.jsonld from same directory
  python3 scripts/generate_shacl.py schema/ocpi/2.2/spec.yaml

  # Specify context file
  python3 scripts/generate_shacl.py schema/EnergyResource/v0.2/attributes.yaml schema/EnergyResource/v0.2/context.jsonld

  # Specify base IRI
  python3 scripts/generate_shacl.py schema/ocpp/2.0.1/spec.yaml --base-iri "https://schemas.ocpp.org/2.0.1/"

  # Custom output file
  python3 scripts/generate_shacl.py schema/ocpi/2.2/spec.yaml -o custom_shacl.jsonld

  # Pretty-printed output
  python3 scripts/generate_shacl.py schema/ocpi/2.2/spec.yaml --pretty

  # Dry run
  python3 scripts/generate_shacl.py schema/ocpi/2.2/spec.yaml --dry-run
        """
    )
    parser.add_argument(
        'yaml_file',
        type=Path,
        help='Path to YAML file adhering to OpenAPI format'
    )
    parser.add_argument(
        'context_file',
        type=Path,
        nargs='?',
        default=None,
        help='Path to context.jsonld file (optional, defaults to context.jsonld in same directory)'
    )
    parser.add_argument(
        '--base-iri',
        type=str,
        default=None,
        help='Base IRI for vocabulary (optional, will be inferred from context or folder structure)'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output file path (default: shacl_{inputfilename}.jsonld in same directory)'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output with indentation (default: minified)'
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
        if not yaml_path.exists():
            yaml_path = repo_root / yaml_path
    
    if not yaml_path.exists():
        print(f"Error: File not found: {args.yaml_file}", file=sys.stderr)
        return 1
    
    context_path = args.context_file
    if context_path and not context_path.is_absolute():
        context_path = repo_root / context_path
    
    success = generate_shacl(
        yaml_path=yaml_path,
        context_path=context_path,
        base_iri=args.base_iri,
        output_path=args.output,
        pretty=args.pretty,
        dry_run=args.dry_run
    )
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
