# EnergyProvider Schema (v0.2)

## Introduction

The **EnergyProvider** schema composes with the core Beckn `Provider` entity to represent energy-specific provider information for P2P energy trading systems. This schema provides source meter identification for energy generation.

### Use Cases

- **Source Meter Identification**: Identifies the meter where energy originates
- **Grid Validation**: Enables utility BPP to validate source meter against grid registry during offer discovery
- **Energy Tracking**: Supports energy flow tracking from source to target

### Key Features

- Source meter ID in DER address format
- Validated by utility BPP during offer processing and order validation

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `sourceMeterId` | string | No | Source meter identifier in DER address format (der://meter/{id}) | Identifies where energy originates. Validated by utility BPP against grid registry during offer discovery and order processing. Used for energy flow tracking and settlement. |
| `sourceType` | enum | No | Type of energy source: SOLAR, BATTERY, GRID, HYBRID, RENEWABLE | Indicates the type of energy source. Source verification occurs at onboarding but can change post-onboarding. Source type influences price but not workflow. |
| `certification` | object | No | Energy certification details including status and certificates | Tracks certification status and certificate references for green energy or carbon offset verification. |
| `certification.status` | string | No | Certification status (e.g., "Carbon Offset Certified", "Green Energy Certified") | Text description of certification status. |
| `certification.certificates` | array&lt;uri&gt; | No | Array of certificate references (URLs or identifiers) | Links to certification documents (e.g., solar panel certificates, green energy certificates). |

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Provider.providerAttributes`

## Example Usage

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyProvider",
  "sourceMeterId": "der://meter/100200300",
  "sourceType": "SOLAR",
  "certification": {
    "status": "Carbon Offset Certified",
    "certificates": ["https://example.com/certs/solar-panel-cert.pdf"]
  }
}
```

## Usage in Discovery

Attached to `Item.provider.providerAttributes` in discover responses:

```json
{
  "beckn:provider": {
    "beckn:id": "provider-solar-farm-001",
    "beckn:providerAttributes": {
      "@context": "./context.jsonld",
      "@type": "EnergyProvider",
      "sourceMeterId": "der://meter/100200300",
      "sourceType": "SOLAR",
      "certification": {
        "status": "Carbon Offset Certified",
        "certificates": ["https://example.com/certs/solar-panel-cert.pdf"]
      }
    }
  }
}
```

