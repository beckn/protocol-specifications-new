# EnergyResource Schema (v0.2)

## Introduction

The **EnergyResource** schema composes with the core Beckn `Item` entity to represent tradable energy resources in Peer-to-Peer (P2P) energy trading systems. This schema defines the characteristics of energy being traded, including source type, delivery mode, certification status, and availability details.

### Use Cases

- **Discovery**: Enables consumers to discover available energy resources based on source type, delivery mode, and availability windows
- **Resource Cataloging**: Allows energy generators to list their available energy with detailed specifications
- **Certification Tracking**: Supports green energy certification and carbon offset verification
- **Meter-Based Identification**: Uses DER (Distributed Energy Resource) address format for meter identification, enabling meter-based discovery rather than provider-name-based discovery

### Key Features

- Supports multiple energy source types (solar, battery, grid, hybrid, renewable)
- Defines delivery modes (EV charging, battery swap, V2G, grid injection)
- Tracks source verification and certification status
- Supports asynchronous production and trade scenarios
- Uses inverter as consistent interface between source and grid

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `sourceType` | enum | No | Type of energy source: SOLAR, BATTERY, GRID, HYBRID, RENEWABLE | Filter discovery by energy source type. Source verification occurs at onboarding but can change post-onboarding (e.g., switching from solar to diesel). Source type influences price but not workflow. |
| `deliveryMode` | enum | No | Mode of energy delivery: EV_CHARGING, BATTERY_SWAP, V2G, GRID_INJECTION | Match consumer requirements with available delivery methods. Used as discovery filter to find compatible energy resources. |
| `certificationStatus` | string | No | Carbon offset or green energy certification status (e.g., "Carbon Offset Certified", "Green Energy Certified") | Display certification information to consumers who prioritize green energy. Used for compliance and marketing purposes. |
| `meterId` | string | No | Source meter identifier using IEEE 2030.5 mRID (meter Resource ID) | Unique identification of the energy source meter. Used for discovery and fulfillment tracking. Enables meter-based discovery where provider names are irrelevant. Format: plain identifier (e.g., `"100200300"`), not `der://` format. |
| `inverterId` | string | No | Inverter identifier serving as consistent interface between source and grid | Provides stable reference point even if energy source changes. The inverter remains constant and serves as the interface between source and grid infrastructure. |
| `availableQuantity` | number | No | Available energy quantity in kilowatt-hours (kWh) | Indicates how much energy is currently available for trading. Used in discovery to match consumer quantity requirements. |
| `productionWindow` | object | No | Time window when energy is produced or available for trading | Defines when energy is available. Contains start and end timestamps (ISO 8601). Used to match consumer time requirements with producer availability. |
| `productionWindow.start` | date-time | No | Start time of production/availability window | Beginning of the time window when energy is available for trading. |
| `productionWindow.end` | date-time | No | End time of production/availability window | End of the time window when energy is available for trading. |
| `sourceVerification` | object | No | Source verification details including certificates and verification status | Tracks verification status and certificate references. Used for compliance and trust building. |
| `sourceVerification.verified` | boolean | No | Whether the source has been verified | Indicates if the energy source has passed verification checks. |
| `sourceVerification.verificationDate` | date-time | No | Date when source was last verified | Timestamp of the most recent verification. Used for compliance tracking and audit purposes. |
| `sourceVerification.certificates` | array&lt;uri&gt; | No | Array of certificate references (URLs or identifiers) | Links to certification documents (e.g., solar panel certificates, green energy certificates). Used for verification and compliance. |
| `productionAsynchronous` | boolean | No | Whether production and trade may be asynchronous (before, during, or after the transaction). Default: false | Indicates if energy production can occur independently of the trade transaction timing. Supports scenarios where energy is stored and traded later, or produced on-demand. |

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Item.itemAttributes`

## Example Usage

See complete examples in:
- **Schema Example**: `examples/schema/item-example.json`
- **Transaction Flow Examples**: `examples/flows/` (discover, select, init, confirm, status)
- **Implementation Guide**: `../../docs/EnergyTrading_implementation_guide.md`

### Quick Example

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyResource",
  "sourceType": "SOLAR",
  "deliveryMode": "GRID_INJECTION",
  "certificationStatus": "Carbon Offset Certified",
  "meterId": "100200300",
  "inverterId": "inv-12345",
  "availableQuantity": 30.5,
  "productionWindow": {
    "start": "2024-10-04T10:00:00Z",
    "end": "2024-10-04T18:00:00Z"
  },
  "sourceVerification": {
    "verified": true,
    "verificationDate": "2024-09-01T00:00:00Z",
    "certificates": ["https://example.com/certs/solar-panel-cert.pdf"]
  },
  "productionAsynchronous": true
}
```

**Note**: Meter ID uses IEEE 2030.5 mRID format (`100200300`), not the legacy `der://meter/100200300` format.

