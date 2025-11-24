#!/usr/bin/env python3
"""Convert OCPP 2.1 JSON Schema files to OpenAPI 3.1.0 spec.yaml

This script consolidates individual JSON Schema files from OCPP 2.1 into a single
OpenAPI 3.1.0 YAML file compatible with the existing schema generation tools.
It also reads CSV files from Appendices to add/enhance enum types.

Usage:
    python3 scripts/convert_ocpp_json_to_openapi.py <json_schemas_dir> <output_spec.yaml> [--version VERSION] [--appendices-dir DIR]

Example:
    python3 scripts/convert_ocpp_json_to_openapi.py \
      ~/Downloads/OCPP-2.1_all_files/OCPP-2.1_part3_JSON_schemas/ \
      schema/ocpp/v2.1.0/spec.yaml \
      --version 2.1.0 \
      --appendices-dir ~/Downloads/OCPP-2.1_all_files/Appendices_CSV_v2.0
"""
import json
import yaml
import sys
import csv
import argparse
from pathlib import Path
from collections import OrderedDict
from typing import Dict, Any, Set, Optional

def convert_json_schema_to_openapi_schema(json_schema: Dict[str, Any], definitions: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a JSON Schema definition to OpenAPI schema format"""
    openapi_schema = {}
    
    # Copy basic properties
    if 'type' in json_schema:
        openapi_schema['type'] = json_schema['type']
    if 'description' in json_schema:
        openapi_schema['description'] = json_schema['description']
    if 'enum' in json_schema:
        openapi_schema['enum'] = json_schema['enum']
    if 'additionalProperties' in json_schema:
        openapi_schema['additionalProperties'] = json_schema['additionalProperties']
    if 'required' in json_schema:
        openapi_schema['required'] = json_schema['required']
    if 'properties' in json_schema:
        openapi_schema['properties'] = {}
        for prop_name, prop_schema in json_schema['properties'].items():
            openapi_schema['properties'][prop_name] = convert_json_schema_to_openapi_schema(prop_schema, definitions)
    if 'items' in json_schema:
        if isinstance(json_schema['items'], dict):
            openapi_schema['items'] = convert_json_schema_to_openapi_schema(json_schema['items'], definitions)
        else:
            openapi_schema['items'] = json_schema['items']
    if 'minItems' in json_schema:
        openapi_schema['minItems'] = json_schema['minItems']
    if 'maxItems' in json_schema:
        openapi_schema['maxItems'] = json_schema['maxItems']
    if 'minLength' in json_schema:
        openapi_schema['minLength'] = json_schema['minLength']
    if 'maxLength' in json_schema:
        openapi_schema['maxLength'] = json_schema['maxLength']
    if 'minimum' in json_schema:
        openapi_schema['minimum'] = json_schema['minimum']
    if 'maximum' in json_schema:
        openapi_schema['maximum'] = json_schema['maximum']
    if 'format' in json_schema:
        openapi_schema['format'] = json_schema['format']
    if 'default' in json_schema:
        openapi_schema['default'] = json_schema['default']
    if 'nullable' in json_schema:
        openapi_schema['nullable'] = json_schema['nullable']
    
    # Convert $ref from JSON Schema format to OpenAPI format
    if '$ref' in json_schema:
        ref = json_schema['$ref']
        if ref.startswith('#/definitions/'):
            # Convert JSON Schema ref to OpenAPI ref
            schema_name = ref.split('/')[-1]
            openapi_schema['$ref'] = f'#/components/schemas/{schema_name}'
        else:
            openapi_schema['$ref'] = ref
    
    # Handle additionalItems (OpenAPI uses items with array)
    if 'additionalItems' in json_schema and json_schema['additionalItems'] is False:
        # This is handled by not having additional items, but we can note it
        pass
    
    # Preserve x-* extensions (like x-javaType)
    for key, value in json_schema.items():
        if key.startswith('x-'):
            openapi_schema[key] = value
    
    return openapi_schema

def merge_definitions(all_definitions: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Merge definitions from multiple files, handling duplicates"""
    merged = OrderedDict()
    
    for def_name, def_schema in all_definitions.items():
        if def_name in merged:
            # If duplicate, prefer the one with more complete information
            existing = merged[def_name]
            # Simple heuristic: prefer the one with more keys
            if len(def_schema) > len(existing):
                merged[def_name] = def_schema
            # Or prefer the one with description if current doesn't have it
            elif 'description' in def_schema and 'description' not in existing:
                merged[def_name] = def_schema
        else:
            merged[def_name] = def_schema
    
    return merged

def convert_refs_in_schema(schema: Dict[str, Any], definitions: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively convert all $ref in a schema from JSON Schema to OpenAPI format"""
    if isinstance(schema, dict):
        result = {}
        for key, value in schema.items():
            if key == '$ref' and isinstance(value, str) and value.startswith('#/definitions/'):
                schema_name = value.split('/')[-1]
                result[key] = f'#/components/schemas/{schema_name}'
            elif key == 'definitions':
                # Skip definitions, they'll be in components.schemas
                continue
            else:
                result[key] = convert_refs_in_schema(value, definitions)
        return result
    elif isinstance(schema, list):
        return [convert_refs_in_schema(item, definitions) for item in schema]
    else:
        return schema

def load_enum_from_csv(csv_file: Path, enum_type_name_override: Optional[str] = None, value_column: Optional[str] = None):
    """Load enum values from a CSV file.
    
    Args:
        csv_file: Path to CSV file
        enum_type_name_override: Override the auto-generated enum type name
        value_column: Override the column name to read values from (default: 'Value' or first column)
    
    Returns:
        (enum_type_name, list of enum values)
    """
    if enum_type_name_override:
        enum_type_name = enum_type_name_override
    else:
        enum_type_name = csv_file.stem
        # Convert filename to enum type name (e.g., connectorenumtype -> ConnectorEnumType)
        enum_type_name = ''.join(word.capitalize() for word in enum_type_name.split('_'))
        if not enum_type_name.endswith('EnumType'):
            enum_type_name += 'EnumType'
    
    enum_values = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            # Try semicolon delimiter first (OCPP CSV format)
            reader = csv.DictReader(f, delimiter=';')
            fieldnames = reader.fieldnames or []
            
            # Determine which column to use
            if value_column:
                col_name = value_column
            elif 'Value' in fieldnames:
                col_name = 'Value'
            elif len(fieldnames) > 0:
                # Use first column
                col_name = fieldnames[0]
            else:
                return enum_type_name, []
            
            if col_name in fieldnames:
                enum_values = [row[col_name] for row in reader if row.get(col_name)]
            else:
                # Try comma delimiter
                f.seek(0)
                reader = csv.DictReader(f, delimiter=',')
                fieldnames = reader.fieldnames or []
                if value_column and value_column in fieldnames:
                    enum_values = [row[value_column] for row in reader if row.get(value_column)]
                elif 'Value' in fieldnames:
                    enum_values = [row['Value'] for row in reader if row.get('Value')]
                elif len(fieldnames) > 0:
                    enum_values = [row[fieldnames[0]] for row in reader if row.get(fieldnames[0])]
    except Exception as e:
        print(f"Warning: Error reading CSV {csv_file.name}: {e}", file=sys.stderr)
    
    return enum_type_name, enum_values

def enhance_definitions_from_csv(definitions: Dict[str, Dict[str, Any]], 
                                  appendices_dir: Optional[Path]) -> Dict[str, Dict[str, Any]]:
    """Enhance or add enum definitions from CSV files in Appendices directory"""
    if not appendices_dir or not appendices_dir.exists():
        return definitions
    
    # Map of CSV filenames to (enum_type_name, value_column)
    csv_enum_mapping = {
        'connectorenumtype.csv': ('ConnectorEnumType', 'Value'),
        'idtokenenumtype.csv': ('IdTokenEnumType', 'Value'),
        'charginglimitsourceenumtype.csv': ('ChargingLimitSourceEnumType', 'Value'),
        'units_of_measure.csv': ('UnitOfMeasureEnumType', 'Value'),
        'additional_info_types.csv': ('AdditionalInfoTypeEnumType', 'additionalInfo.type'),
        'additional_info_types_adhoc.csv': ('AdditionalInfoTypeAdHocEnumType', 'additionalInfo.type'),
        'paymentbrand.csv': ('PaymentBrandEnumType', 'PaymentBrand'),
        'paymentrecognition.csv': ('PaymentRecognitionEnumType', 'PaymentRecognition'),
        'signingmethod.csv': ('SigningMethodEnumType', 'SigningMethod'),
        # Note: reason_codes.csv and security_events.csv have complex structures
        # (grouped/hierarchical) and may not be simple enum types
    }
    
    for csv_file in appendices_dir.glob('*.csv'):
        csv_name = csv_file.name.lower()
        if csv_name in csv_enum_mapping:
            enum_type_name, value_column = csv_enum_mapping[csv_name]
            enum_type_name_from_csv, enum_values = load_enum_from_csv(csv_file, enum_type_name, value_column)
            
            if enum_values:
                # Create or update the enum type definition
                if enum_type_name in definitions:
                    # Update existing enum with values from CSV (CSV is authoritative)
                    definitions[enum_type_name]['enum'] = enum_values
                    print(f"Updated {enum_type_name} with {len(enum_values)} values from CSV")
                else:
                    # Create new enum type definition
                    definitions[enum_type_name] = {
                        'type': 'string',
                        'additionalProperties': False,
                        'enum': enum_values,
                        'description': f'Enumeration values from {csv_file.name}'
                    }
                    print(f"Added {enum_type_name} with {len(enum_values)} values from CSV")
    
    return definitions

def process_json_schemas(json_schemas_dir: Path, appendices_dir: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """Process all JSON Schema files and extract definitions"""
    all_definitions = {}
    message_types = []
    
    for json_file in sorted(json_schemas_dir.glob('*.json')):
        try:
            with open(json_file) as f:
                data = json.load(f)
                
                # Extract message type name from filename
                message_name = json_file.stem
                message_types.append(message_name)
                
                # Extract all definitions
                if 'definitions' in data:
                    for def_name, def_schema in data['definitions'].items():
                        # Convert JSON Schema to OpenAPI format
                        openapi_def = convert_json_schema_to_openapi_schema(def_schema, {})
                        all_definitions[def_name] = openapi_def
        except Exception as e:
            print(f"Warning: Error processing {json_file.name}: {e}", file=sys.stderr)
            continue
    
    # Merge duplicate definitions
    merged_definitions = merge_definitions(all_definitions)
    
    # Enhance with CSV data from Appendices
    merged_definitions = enhance_definitions_from_csv(merged_definitions, appendices_dir)
    
    # Convert all $ref in merged definitions
    final_definitions = {}
    for def_name, def_schema in merged_definitions.items():
        final_definitions[def_name] = convert_refs_in_schema(def_schema, merged_definitions)
    
    return final_definitions, message_types

def create_openapi_spec(definitions: Dict[str, Dict[str, Any]], message_types: list, version: str = "2.1.0") -> Dict[str, Any]:
    """Create OpenAPI 3.1.0 specification structure"""
    
    # Create tags for all message types (similar to OCPP 2.0.1 structure)
    tags = []
    for msg_type in sorted(message_types):
        tag_name = msg_type.lower()
        display_name = ''.join(word.capitalize() for word in msg_type.split('_'))
        tags.append({
            'name': tag_name,
            'x-displayName': display_name,
            'description': f'<SchemaDefinition schemaRef="#/components/schemas/{msg_type}" />'
        })
    
    spec = {
        'openapi': '3.1.0',
        'info': {
            'title': 'OCPP JSON Schemas',
            'version': version
        },
        'paths': {},
        'tags': tags,
        'components': {
            'schemas': definitions
        }
    }
    
    return spec

def main():
    parser = argparse.ArgumentParser(
        description='Convert OCPP 2.1 JSON Schema files to OpenAPI 3.1.0 spec.yaml',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'json_schemas_dir',
        type=Path,
        help='Directory containing OCPP JSON Schema files'
    )
    parser.add_argument(
        'output_file',
        type=Path,
        help='Output OpenAPI spec.yaml file path'
    )
    parser.add_argument(
        '--version',
        type=str,
        default='2.1.0',
        help='OCPP version (default: 2.1.0)'
    )
    parser.add_argument(
        '--appendices-dir',
        type=Path,
        default=None,
        help='Directory containing CSV appendices (e.g., Appendices_CSV_v2.0)'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print YAML output'
    )
    
    args = parser.parse_args()
    
    if not args.json_schemas_dir.exists():
        print(f"Error: Directory not found: {args.json_schemas_dir}", file=sys.stderr)
        return 1
    
    if not args.json_schemas_dir.is_dir():
        print(f"Error: Not a directory: {args.json_schemas_dir}", file=sys.stderr)
        return 1
    
    print(f"Processing JSON Schema files from: {args.json_schemas_dir}")
    if args.appendices_dir:
        print(f"Using appendices from: {args.appendices_dir}")
    
    try:
        # Process all JSON files
        definitions, message_types = process_json_schemas(args.json_schemas_dir, args.appendices_dir)
        
        print(f"Found {len(message_types)} message types")
        print(f"Extracted {len(definitions)} unique schema definitions")
        
        # Create OpenAPI spec
        spec = create_openapi_spec(definitions, message_types, args.version)
        
        # Ensure output directory exists
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write YAML file
        with open(args.output_file, 'w') as f:
            if args.pretty:
                yaml.dump(spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)
            else:
                yaml.dump(spec, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"✓ Generated {args.output_file}")
        print(f"  Version: {args.version}")
        print(f"  Schemas: {len(definitions)}")
        print(f"  Message types: {len(message_types)}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

