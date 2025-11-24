# OCPP 2.1.0 Schema Generation

This directory contains the JSON-LD schema files for OCPP 2.1 Edition 1, generated from the official OCPP 2.1 JSON Schema files.

## Generation Process

- The source files for "OCPP 2.1 Edition 1" are downloaded from https://openchargealliance.org/my-oca/ocpp/ and unzipped to folder `OCPP-2.1_all_files/`. Also unzip `Appendices_CSV_v2.0.zip` within it to a folder `OCPP-2.1_all_files/Appendices_CSV_v2.0`.
- Convert JSON Schemas to OpenAPI spec.yaml. Run the following after changing paths to the OCPP files.

    **Command:**
    ```bash
    python3 scripts/convert_ocpp_json_to_openapi.py \
    ~/Downloads/OCPP-2.1_all_files/OCPP-2.1_part3_JSON_schemas/ \
    schema/ocpp/v2.1.0/spec.yaml \
    --version 2.1.0 \
    --appendices-dir ~/Downloads/OCPP-2.1_all_files/Appendices_CSV_v2.0 \
    --pretty
    ```

    **Note:** The script also reads CSV files from `Appendices_CSV_v2.0/` to add/enhance enum types that may not be fully defined in the JSON Schema files. This includes:
    - `ConnectorEnumType` (31 values)
    - `IdTokenEnumType` (11 values)
    - `ChargingLimitSourceEnumType` (4 values)
    - `UnitOfMeasureEnumType` (34 values)
    - `AdditionalInfoTypeEnumType` (2 values)
    - `AdditionalInfoTypeAdHocEnumType` (11 values)
    - `PaymentBrandEnumType` (22 values)
    - `PaymentRecognitionEnumType` (9 values)
    - `SigningMethodEnumType` (7 values)


    **Output:** `schema/ocpp/v2.1.0/spec.yaml`
- Generate the JSON-LD vocabulary file containing all schemas and enum values.

    **Command:**
    ```bash
    python3 scripts/generate_vocab.py schema/ocpp/v2.1.0/spec.yaml --pretty
    ```

    **Output:** `schema/ocpp/v2.1.0/vocab.jsonld`

    **What it contains:**
    - All object schemas as `rdfs:Class`
    - All enum types as `schema:Enumeration`
    - All enum values as individual entities with `ocpp:` prefix
    - Base IRI: `https://schemas.ocpp.org/2.1.0/`

- Creates the JSON-LD context file for compact IRIs.

    **Process:**
    1. Start with `schema/ocpp/2.0.1/context.jsonld.example` as a template
    2. Update version to `2.1.0`
    3. Update base IRI to `https://schemas.ocpp.org/2.1.0/`
    4. Add schema type mappings for commonly used types
    5. Add enum value aliases as needed (e.g., connector types)

    **Manual creation or template-based generation**

    **Output:** `schema/ocpp/v2.1.0/context.jsonld`

- Generate SHACL shapes for validation.

    **Command:**
    ```bash
    python3 scripts/generate_shacl.py schema/ocpp/v2.1.0/spec.yaml --pretty
    ```

    **Output:** `schema/ocpp/v2.1.0/shacl_spec.jsonld`

    **What it contains:**
    - SHACL NodeShapes for all object schemas
    - Property shapes with constraints (required, datatypes, enums)
    - Enum values in `sh:in` for enum properties


## File Structure

```
schema/ocpp/v2.1.0/
├── README.md              # This file
├── spec.yaml              # Consolidated OpenAPI 3.1.0 specification
├── vocab.jsonld           # JSON-LD vocabulary with all schemas and enum values
├── context.jsonld         # JSON-LD context for compact IRIs
└── shacl_spec.jsonld      # SHACL shapes for validation
```

## Statistics

Based on the generated files:

- **Total JSON Schema files**: 181
- **Unique schema definitions**: 241 (includes enum types from CSV)
- **Enum types**: 119
- **Enum values**: 730
- **Vocab entries**: 971 (schemas + enum types + enum values)

## Key Differences from OCPP 2.0.1

OCPP 2.1.0 includes:
- New message types (e.g., `BatterySwapRequest`, `AFRRSignalRequest`, `AdjustPeriodicEventStreamRequest`)
- Additional enum types and values
- Enhanced schemas with new fields marked with `*(2.1)*` in descriptions
- New connector types: `cChaoJi`, `cGBT-DC`, `cLECCS`, `cMCS`, `cNACS`, `cNACS-CCS1`, `cCCS1-NACS`, `cUltraChaoJi`, `sType1`
- Additional enum types from CSV appendices (PaymentBrand, PaymentRecognition, SigningMethod, UnitOfMeasure, etc.)

## Verification

After generation, verify:

1. **spec.yaml**: Check that all schemas from source files are present (241 schemas)
2. **vocab.jsonld**: Verify enum values are correctly generated (971 entries, including new connector types like `cGBT-DC`, `cChaoJi`, `cNACS`)
3. **context.jsonld**: Ensure base IRI and prefix mappings are correct (`https://schemas.ocpp.org/2.1.0/`)
4. **shacl_spec.jsonld**: Verify `sh:in` contains all enum values for enum properties (122 shapes)

## Maintenance

When OCPP 2.1 errata or updates are released:

1. Download new JSON schema files
2. Re-run the conversion script
3. Regenerate vocab.jsonld, context.jsonld, and shacl_spec.jsonld
4. Update this README with new statistics and changes

## References

- [OCPP 2.1 Specification](https://www.openchargealliance.org/)
- [OCPP 2.1 JSON Schemas](https://www.openchargealliance.org/downloads/)
- Base IRI: `https://schemas.ocpp.org/2.1.0/`

## License

OCPP 2.1 is licensed under Creative Commons Attribution-NoDerivatives 4.0 International Public License.

