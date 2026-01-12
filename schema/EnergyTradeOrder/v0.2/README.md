# EnergyTradeOrder Schema (v0.2)

## Introduction

The **EnergyTradeOrder** schema composes with the core Beckn `Order` entity to represent trade orders for energy resources in P2P energy trading systems. This schema identifies the BAP and BPP participants involved in the trade, along with order quantity details.

### Use Cases

- **Order Identification**: Identifies the buyer (BAP) and seller (BPP) platforms participating in the energy trade
- **Quantity Tracking**: Tracks the total energy quantity being traded in the order
- **Platform Coordination**: Enables coordination between BAP and BPP for order fulfillment

### Key Features

- Required BAP and BPP identification for trade participants
- Optional total quantity specification for the order

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `bap_id` | string | Yes | Beckn Application Platform (BAP) identifier | The subscriber ID of the buyer/consumer platform initiating the trade order. Used for routing and identification. |
| `bpp_id` | string | Yes | Beckn Provider Platform (BPP) identifier | The subscriber ID of the seller/provider platform fulfilling the trade order. Used for routing and identification. |
| `total_quantity` | number | No | Total quantity of energy in kilowatt-hours (kWh) | The total energy quantity for this trade order. Used for order aggregation and settlement calculations. |

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Order.orderAttributes`

## Example Usage

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyTradeOrder",
  "bap_id": "bap.energymarket.io",
  "bpp_id": "bpp.solarprovider.io",
  "total_quantity": 50.0
}
```
