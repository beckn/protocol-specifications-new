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

def expand_iri(iri: str, vocab_base: str, context: dict) -> str:
    """Expand a compact IRI (e.g., 'beckn:ChargingSession') to full IRI"""
    if not iri:
        return iri
    
    # If already a full IRI (starts with http:// or https://), return as is
    if iri.startswith('http://') or iri.startswith('https://'):
        return iri
    
    # If it's a compact IRI (contains ':'), expand it
    if ':' in iri and not iri.startswith('urn:'):
        prefix, local = iri.split(':', 1)
        ctx = context.get('@context', {})
        
        # Check if prefix is defined in context
        if prefix in ctx:
            base = ctx[prefix]
            if isinstance(base, str):
                # Remove trailing # or / if present
                base = base.rstrip('#/')
                return f"{base}/{local}" if not base.endswith('/') else f"{base}{local}"
        
        # Fallback: use vocab_base if prefix is 'vocab' or unknown
        if prefix == 'vocab':
            return f"{vocab_base}{local}"
    
    # If no prefix, assume it's a local name and use vocab_base
    return f"{vocab_base}{iri}"

def get_property_iri(prop_name: str, vocab_base: str, context: dict) -> str:
    """Get full IRI for a property from context or construct from vocab_base"""
    # Check if property is in context
    if prop_name in context.get('@context', {}):
        prop_iri = context['@context'][prop_name]
        if isinstance(prop_iri, dict):
            iri = prop_iri.get('@id', f"{vocab_base}{prop_name}")
        else:
            iri = prop_iri
        # Expand to full IRI
        return expand_iri(iri, vocab_base, context)
    return f"{vocab_base}{prop_name}"

def convert_property(prop_name: str, prop_def: dict, required_fields: list, 
                     all_schemas: dict, vocab_base: str, context: dict, use_full_iris: bool = False):
    """Convert an OpenAPI property to SHACL property shape"""
    prop_iri = get_property_iri(prop_name, vocab_base, context)
    
    if use_full_iris:
        shacl_ns = 'http://www.w3.org/ns/shacl#'
        prop_shape = {
            f'{shacl_ns}path': prop_iri,
            f'{shacl_ns}name': prop_name
        }
        min_count_key = f'{shacl_ns}minCount'
        max_count_key = f'{shacl_ns}maxCount'
        class_key = f'{shacl_ns}class'
        node_kind_key = f'{shacl_ns}nodeKind'
        datatype_key = f'{shacl_ns}datatype'
        in_key = f'{shacl_ns}in'
        min_inclusive_key = f'{shacl_ns}minInclusive'
        max_inclusive_key = f'{shacl_ns}maxInclusive'
        node_kind_value = f'{shacl_ns}IRIOrLiteral'
    else:
        prop_shape = {
            'sh:path': prop_iri,
            'sh:name': prop_name
        }
        min_count_key = 'sh:minCount'
        max_count_key = 'sh:maxCount'
        class_key = 'sh:class'
        node_kind_key = 'sh:nodeKind'
        datatype_key = 'sh:datatype'
        in_key = 'sh:in'
        min_inclusive_key = 'sh:minInclusive'
        max_inclusive_key = 'sh:maxInclusive'
        node_kind_value = 'sh:IRIOrLiteral'
    
    # Handle required
    if prop_name in required_fields:
        prop_shape[min_count_key] = 1
    
    # Handle nullable
    if prop_def.get('nullable', False):
        prop_shape[max_count_key] = 1  # Allow 0 or 1
    
    # Handle $ref first
    if '$ref' in prop_def:
        ref = prop_def['$ref']
        if ref.startswith('#/components/schemas/'):
            ref_name = ref.split('/')[-1]
            ref_iri = get_iri(ref_name, vocab_base)
            if use_full_iris:
                ref_iri = expand_iri(ref_iri, vocab_base, context)
            prop_shape[class_key] = ref_iri
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
                ref_iri = get_iri(ref_name, vocab_base)
                if use_full_iris:
                    ref_iri = expand_iri(ref_iri, vocab_base, context)
                prop_shape[node_kind_key] = node_kind_value
                prop_shape[class_key] = ref_iri
        else:
            item_type = items.get('type')
            if item_type in type_map:
                prop_shape[datatype_key] = type_map[item_type]
            elif item_type == 'object':
                prop_shape[node_kind_key] = node_kind_value
        return prop_shape
    
    # Handle format before type (format can override)
    if 'format' in prop_def:
        format_type = prop_def['format']
        if format_type in type_map:
            prop_shape[datatype_key] = type_map[format_type]
        elif prop_type in type_map:
            prop_shape[datatype_key] = type_map[prop_type]
    elif prop_type in type_map:
        prop_shape[datatype_key] = type_map[prop_type]
    elif prop_type == 'object':
        prop_shape[node_kind_key] = node_kind_value
    
    # Handle enum
    if 'enum' in prop_def:
        enum_values = prop_def['enum']
        # sh:in expects a list of values
        prop_shape[in_key] = enum_values
    
    # Handle minimum/maximum for numbers
    if 'minimum' in prop_def:
        prop_shape[min_inclusive_key] = prop_def['minimum']
    if 'maximum' in prop_def:
        prop_shape[max_inclusive_key] = prop_def['maximum']
    
    return prop_shape

def convert_schema(schema_name: str, schema_def: dict, all_schemas: dict, 
                   vocab_base: str, context: dict, use_full_iris: bool = False):
    """Convert an OpenAPI schema to a SHACL NodeShape"""
    shape_iri = get_iri(schema_name, vocab_base)
    
    # Check if schema has a specific IRI in context
    if schema_name in context.get('@context', {}):
        shape_iri_raw = context['@context'][schema_name]
        if isinstance(shape_iri_raw, str):
            shape_iri = shape_iri_raw
        elif isinstance(shape_iri_raw, dict):
            shape_iri = shape_iri_raw.get('@id', shape_iri)
    
    if use_full_iris:
        # Expand to full IRI
        shape_iri = expand_iri(shape_iri, vocab_base, context)
        shacl_ns = 'http://www.w3.org/ns/shacl#'
        shape = {
            '@id': shape_iri,
            '@type': f'{shacl_ns}NodeShape',
            f'{shacl_ns}targetClass': shape_iri,
            f'{shacl_ns}name': schema_name
        }
    else:
        # Use compact IRIs
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
                                         all_schemas, vocab_base, context, use_full_iris)
            if prop_shape:
                properties.append(prop_shape)
        except Exception as e:
            print(f"Error converting property {prop_name} in {schema_name}: {e}", file=sys.stderr)
            continue
    
    if properties:
        if use_full_iris:
            shape['http://www.w3.org/ns/shacl#property'] = properties
        else:
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

def generate_shacl_for_file(attributes_path: Path, output_path: Path = None, dry_run: bool = False, pretty: bool = False, use_full_iris: bool = False) -> bool:
    """Generate SHACL shapes from an attributes.yaml file"""
    if not attributes_path.exists():
        print(f"Error: File not found: {attributes_path}", file=sys.stderr)
        return False
    
    schema_dir = attributes_path.parent
    context_path = schema_dir / 'context.jsonld'
    
    # Determine output path
    if output_path is None:
        # Default: shacl_{inputfilename}.jsonld in same directory
        input_stem = attributes_path.stem  # filename without extension
        output_path = schema_dir / f'shacl_{input_stem}.jsonld'
    else:
        # If output_path is provided but not absolute, make it relative to schema_dir
        if not output_path.is_absolute():
            output_path = schema_dir / output_path
    
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
                shape = convert_schema(schema_name, schema_def, schemas, vocab_base, context, use_full_iris)
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
        print(f"  Format: {'Pretty-printed' if pretty else 'Minified'}")
        return True
    
    # Create SHACL document
    if use_full_iris:
        # Minimal context when using full IRIs
        shacl_doc = {
            '@context': {
                '@version': 1.1
            },
            '@graph': shapes
        }
    else:
        # Full context with prefixes when using compact IRIs
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
  # Generate minified SHACL with compact IRIs (default)
  # Output: schema/EnergyResource/v0.2/shacl_attributes.jsonld
  python3 scripts/generate_shacl_for_schemas.py schema/EnergyResource/v0.2/attributes.yaml

  # Generate with full IRIs (minified)
  python3 scripts/generate_shacl_for_schemas.py schema/EnergyResource/v0.2/attributes.yaml --full-iris

  # Generate pretty-printed SHACL with compact IRIs
  python3 scripts/generate_shacl_for_schemas.py schema/EnergyResource/v0.2/attributes.yaml --pretty

  # Specify custom output file
  python3 scripts/generate_shacl_for_schemas.py schema/EnergyResource/v0.2/attributes.yaml -o custom_shacl.jsonld

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
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output with indentation (default: minified)'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output file path (default: shacl_{inputfilename}.jsonld in same directory as input)'
    )
    parser.add_argument(
        '--full-iris',
        action='store_true',
        help='Use full IRIs instead of compact IRIs (default: compact IRIs with prefixes)'
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
    
    success = generate_shacl_for_file(yaml_path, output_path=args.output, dry_run=args.dry_run, pretty=args.pretty, use_full_iris=args.full_iris)
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())

