#!/usr/bin/env python3
"""Generate minified JSON-LD context from OpenAPI spec.yaml"""
import json
import yaml
import sys
from pathlib import Path

def generate_context(spec_path, base_iri=None):
    """
    Generate minified JSON-LD context from OpenAPI spec.yaml
    
    Args:
        spec_path: Path to spec.yaml file
        base_iri: Base IRI for the vocabulary (optional, defaults to https://schemas.{name}/version/)
    """
    spec_path = Path(spec_path)
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")
    
    # Load spec
    with open(spec_path) as f:
        spec = yaml.safe_load(f)
    
    schemas = spec.get('components', {}).get('schemas', {})
    
    # Determine base IRI if not provided
    if base_iri is None:
        # Extract name and version from path (e.g., ocpi2.2, ocpp2.0.1)
        folder_name = spec_path.parent.name
        if folder_name.startswith('ocpi'):
            base_iri = "https://schemas.ocpi.org/2.2/"
        elif folder_name.startswith('ocpp'):
            base_iri = "https://schemas.ocpp.org/2.0.1/"
        else:
            # Generic fallback
            base_iri = f"https://schemas.{folder_name}/"
    
    # Create context
    ctx = {
        "@context": {
            "@version": 1.1,
            "@vocab": base_iri
        }
    }
    
    # Map each schema to @id so it resolves to @vocab + schema_name
    for name in sorted(schemas.keys()):
        ctx["@context"][name] = "@id"
    
    # Write to file
    context_path = spec_path.parent / 'context.jsonld'
    with open(context_path, 'w') as f:
        json.dump(ctx, f, separators=(',', ':'))
        f.write('\n')
    
    print(f"Generated context.jsonld with {len(schemas)} schemas")
    print(f"Base IRI: {base_iri}")
    return context_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: generate_context.py <spec.yaml> [base_iri]")
        sys.exit(1)
    
    spec_path = sys.argv[1]
    base_iri = sys.argv[2] if len(sys.argv) > 2 else None
    generate_context(spec_path, base_iri)

