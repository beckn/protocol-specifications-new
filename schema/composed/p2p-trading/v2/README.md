# Composed P2P Trading Schema (v2)

This directory contains a **composed JSON-LD context** that merges all necessary schemas for P2P energy trading into a single context file. This reduces payload verbosity by allowing a single `@context` declaration instead of multiple nested contexts.

## Files

- `context.jsonld`: Unified composed context merging:
  - Core Beckn Protocol schemas (`core/v2`)
  - Energy Buyer attributes (`EnergyBuyer/v0.2`)
  - Energy Provider attributes (`EnergyProvider/v0.2`)
  - Energy Resource attributes (`EnergyResource/v0.2`)
  - Energy Trade Offer attributes (`EnergyTradeOffer/v0.2`)
  - Energy Trade Delivery attributes (`EnergyTradeDelivery/v0.2`)

## Usage

### In JSON Examples

Instead of multiple `@context` declarations:

```json
{
  "message": {
    "order": {
      "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/core/v2/context.jsonld",
      "@type": "beckn:Order",
      "buyer": {
        "buyerAttributes": {
          "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/EnergyBuyer/v0.2/context.jsonld",
          "@type": "EnergyBuyer"
        }
      }
    }
  }
}
```

Use a single composed context at the root:

```json
{
  "message": {
    "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/composed/p2p-trading/v2/context.jsonld",
    "order": {
      "@type": "beckn:Order",
      "buyer": {
        "buyerAttributes": {
          "@type": "EnergyBuyer"
        }
      }
    }
  }
}
```

## Validation

The validator (`DEG/scripts/validate_schema.py`) supports composed contexts with the `--jsonld` flag:

```bash
python3 scripts/validate_schema.py --jsonld examples/p2p-trading/v2/*.json
```

This will:
1. Detect composed context URLs
2. Expand JSON-LD using pyld library
3. Validate against OpenAPI schemas

## Benefits

- ✅ **Reduced verbosity**: Single `@context` instead of multiple nested contexts
- ✅ **Cleaner payloads**: No repeated context declarations
- ✅ **Easier maintenance**: All mappings in one place
- ✅ **Backward compatible**: Can coexist with distributed contexts

## Implementation Notes

- The composed context manually merges all individual context files
- All CURIE mappings are preserved
- Schema validation still uses individual `attributes.yaml` files
- JSON-LD expansion is optional (requires `pyld` library)

## Future Enhancements

- Consider using JSON-LD 1.1 `@import` if/when it becomes standardized
- Automate context merging from individual schema files
- Add CURIE shortcuts for commonly used properties

