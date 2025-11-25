# IEEE 2030.5 Schema Generation


This directory contains the JSON-LD schema files for IEEE 2030.5 (Smart Energy Profile 2.0), generated from the OpenAPI specification.

## File Structure

```
schema/ieee/2030.5/
├── README.md              # This file
├── spec.yaml              # OpenAPI 3.1.0 specification
├── vocab.jsonld           # JSON-LD vocabulary with all schemas, enum values, and important properties
├── context.jsonld         # JSON-LD context for compact IRIs
└── shacl_spec.jsonld      # SHACL shapes for validation
```

## Generation Process

### Step 1: Generate vocab.jsonld

Generate the JSON-LD vocabulary file containing all schemas, enum values, and important properties.

**Command:**
```bash
python3 scripts/generate_vocab.py schema/ieee/2030.5/spec.yaml --pretty
```

**Output:** `schema/ieee/2030.5/vocab.jsonld`

**What it contains:**
- All object schemas as `rdfs:Class` (184 classes)
- All string enum types as `schema:Enumeration` with `schema:hasEnumerationMember`
- All enum values as individual entities with `ieee:` prefix
- Important properties as `rdf:Property` (e.g., `ieee:mRID`, `ieee:lFDI`)
- Base IRI: `https://schemas.ieee.org/2030.5/`

### Step 2: Create context.jsonld

Create the JSON-LD context file for compact IRIs.

**Process:**
1. Set `@vocab` to the base IRI
2. Map the `ieee:` prefix to the base IRI
3. Add term mappings for commonly used properties (mRID, lFDI)
4. Add term mappings for schema types as needed

**Output:** `schema/ieee/2030.5/context.jsonld`

### Step 3: Generate shacl_spec.jsonld

Generate SHACL shapes for validation.

**Command:**
```bash
python3 scripts/generate_shacl.py schema/ieee/2030.5/spec.yaml --pretty
```

**Output:** `schema/ieee/2030.5/shacl_spec.jsonld`

**What it contains:**
- SHACL NodeShapes for all object schemas
- Property shapes with constraints (required, datatypes, enums)
- Enum values in `sh:in` for enum properties

## Statistics

Based on the generated files:

- **Total schemas**: 184
- **Enum types**: 3 (string enums only)
- **Enum values**: 21
- **Properties**: 2 (mRID, lFDI)
- **Vocab entries**: 210 (classes + enum types + enum values + properties)

## Vocabulary Strategy

The vocabulary includes:

1. **All Object Schemas** ✓
   - Every `type: object` schema → `rdfs:Class`
   - Example: `ieee:EndDevice`, `ieee:File`, `ieee:FunctionSetAssignments`

2. **String Enum Types and Values** ✓
   - String enums → `schema:Enumeration` type + individual enum value entries
   - Currently: 3 enum types with 21 total values

3. **Important Properties** ✓
   - Commonly used properties like `mRID`, `lFDI` → `rdf:Property`
   - These are frequently referenced across multiple schemas

**Note:** Integer enums (78 occurrences) are **not** included as they are numeric constraints, not vocabulary terms.

## Usage Examples

### Using mRID and LFDI

```json
{
  "@context": "./context.jsonld",
  "@type": "ieee:EndDevice",
  "ieee:mRID": "urn:uuid:12345678-1234-1234-1234-123456789abc",
  "ieee:lFDI": "00000001"
}
```

Or using compact terms:
```json
{
  "@context": "./context.jsonld",
  "@type": "ieee:EndDevice",
  "mRID": "urn:uuid:12345678-1234-1234-1234-123456789abc",
  "lFDI": "00000001"
}
```

### Using Enum Values

```json
{
  "@context": "./context.jsonld",
  "@type": "ieee:File",
  "ieee:type": "ieee:00"
}
```

## Verification

After generation, verify:

1. **spec.yaml**: Check that all schemas are present (184 schemas)
2. **vocab.jsonld**: Verify enum values and properties are correctly generated
   - Check for `ieee:mRID` and `ieee:lFDI` properties
   - Verify enum types have `schema:hasEnumerationMember`
3. **context.jsonld**: Ensure base IRI and prefix mappings are correct (`https://schemas.ieee.org/2030.5/`)
4. **shacl_spec.jsonld**: Verify `sh:in` contains all enum values for enum properties

## Maintenance

When IEEE 2030.5 updates are released:

1. Update the spec.yaml file
2. Regenerate vocab.jsonld, context.jsonld, and shacl_spec.jsonld
3. Update this README with new statistics and changes

## References

- [IEEE 2030.5 Specification](https://standards.ieee.org/standard/2030_5-2018.html)
- Base IRI: `https://schemas.ieee.org/2030.5/`

## License

IEEE 2030.5 is an IEEE standard. Refer to IEEE for licensing information.

