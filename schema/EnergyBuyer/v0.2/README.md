# EnergyBuyer Schema (v0.2)

## Introduction

The **EnergyBuyer** schema composes with the core Beckn `Buyer` entity to represent energy-specific buyer information for P2P energy trading systems. This schema provides target meter identification for energy delivery.

### Use Cases

- **Target Meter Identification**: Identifies the meter where energy will be delivered
- **Grid Validation**: Enables utility BPP to validate target meter against grid registry
- **Delivery Routing**: Supports grid routing and energy delivery tracking

### Key Features

- Target meter ID in DER address format
- Validated by utility BPP during order processing

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `targetMeterId` | string | No | Target meter identifier in DER address format (der://meter/{id}) | Identifies where energy will be delivered. Validated by utility BPP against grid registry. Used for fulfillment tracking and grid routing. |

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Buyer.buyerAttributes`

## Example Usage

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyBuyer",
  "targetMeterId": "der://meter/98765456"
}
```

## Usage in Orders

Attached to `Order.buyer.buyerAttributes` in init/confirm requests:

```json
{
  "beckn:buyer": {
    "beckn:id": "buyer-001",
    "beckn:buyerAttributes": {
      "@context": "./context.jsonld",
      "@type": "EnergyBuyer",
      "targetMeterId": "der://meter/98765456"
    }
  }
}
```

