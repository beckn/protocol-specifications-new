#!/usr/bin/env python3
"""Generate SHACL shapes from OpenAPI spec.yaml"""
import json
import yaml
import sys
from pathlib import Path

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

def get_iri(name, vocab_base):
    """Get IRI for a schema or property name"""
    return f"{vocab_base}{name}"

def get_property_iri(prop_name, vocab_base):
    """Get IRI for a property"""
    return f"{vocab_base}{prop_name}"

def convert_property(prop_name, prop_def, required_fields, all_schemas, vocab_base):
    """Convert an OpenAPI property to SHACL property shape"""
    prop_shape = {
        'sh:path': get_property_iri(prop_name, vocab_base),
        'sh:name': prop_name
    }
    
    # Handle required
    if prop_name in required_fields:
        prop_shape['sh:minCount'] = 1
    
    # Handle $ref first
    if '$ref' in prop_def:
        ref = prop_def['$ref']
        if ref.startswith('#/components/schemas/'):
            ref_name = ref.split('/')[-1]
            prop_shape['sh:class'] = get_iri(ref_name, vocab_base)
        return prop_shape
    
    # Handle type
    prop_type = prop_def.get('type')
    
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
            else:
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
    
    return prop_shape

def convert_schema(schema_name, schema_def, all_schemas, vocab_base):
    """Convert an OpenAPI schema to a SHACL NodeShape"""
    shape = {
        '@id': get_iri(schema_name, vocab_base),
        '@type': 'sh:NodeShape',
        'sh:targetClass': get_iri(schema_name, vocab_base),
        'sh:name': schema_name
    }
    
    properties = []
    required_fields = schema_def.get('required', [])
    props = schema_def.get('properties', {})
    
    for prop_name, prop_def in props.items():
        try:
            prop_shape = convert_property(prop_name, prop_def, required_fields, all_schemas, vocab_base)
            if prop_shape:
                properties.append(prop_shape)
        except Exception as e:
            print(f"Error converting property {prop_name} in {schema_name}: {e}", file=sys.stderr)
            continue
    
    if properties:
        shape['sh:property'] = properties
    
    return shape

def generate_shacl(spec_path, context_path=None, base_iri=None):
    """
    Generate SHACL shapes from OpenAPI spec.yaml
    
    Args:
        spec_path: Path to spec.yaml file
        context_path: Path to context.jsonld (optional, will be inferred if not provided)
        base_iri: Base IRI for the vocabulary (optional, will be read from context if not provided)
    """
    spec_path = Path(spec_path)
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")
    
    # Load context to get IRIs
    if context_path is None:
        context_path = spec_path.parent / 'context.jsonld'
    
    vocab_base = None
    if Path(context_path).exists():
        with open(context_path) as f:
            context = json.load(f)
        vocab_base = context['@context']['@vocab']
    elif base_iri:
        vocab_base = base_iri
    else:
        # Determine base IRI from folder name
        folder_name = spec_path.parent.name
        if folder_name.startswith('ocpi'):
            vocab_base = "https://schemas.ocpi.org/2.2/"
        elif folder_name.startswith('ocpp'):
            vocab_base = "https://schemas.ocpp.org/2.0.1/"
        else:
            vocab_base = f"https://schemas.{folder_name}/"
    
    # Load spec
    with open(spec_path) as f:
        spec = yaml.safe_load(f)
    
    schemas = spec.get('components', {}).get('schemas', {})
    
    # Generate SHACL shapes
    shapes = []
    for schema_name, schema_def in schemas.items():
        if schema_def.get('type') == 'object':
            try:
                shape = convert_schema(schema_name, schema_def, schemas, vocab_base)
                shapes.append(shape)
            except Exception as e:
                print(f"Error converting schema {schema_name}: {e}", file=sys.stderr)
                continue
    
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
    output_path = spec_path.parent / 'shacl.jsonld'
    with open(output_path, 'w') as f:
        json.dump(shacl_doc, f, indent=2)
        f.write('\n')
    
    print(f"Generated shacl.jsonld with {len(shapes)} shapes")
    print(f"Base IRI: {vocab_base}")
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: generate_shacl.py <spec.yaml> [context.jsonld] [base_iri]")
        sys.exit(1)
    
    spec_path = sys.argv[1]
    context_path = sys.argv[2] if len(sys.argv) > 2 else None
    base_iri = sys.argv[3] if len(sys.argv) > 3 else None
    generate_shacl(spec_path, context_path, base_iri)

