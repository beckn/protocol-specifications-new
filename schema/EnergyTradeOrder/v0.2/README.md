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

---

# EnergyTradeOrderInterUtility Schema (v0.2)

## Introduction

The **EnergyTradeOrderInterUtility** schema extends `EnergyTradeOrder` for inter-utility (inter-discom) P2P energy trading scenarios. It adds required utility/discom identifiers for both the buyer and seller sides to support trades that cross distribution company boundaries.

### Use Cases

- **Inter-Discom Trading**: Enables P2P trades where the buyer and seller are connected to different distribution companies (discoms)
- **Grid Coordination**: Facilitates coordination between utilities for energy scheduling and settlement
- **Regulatory Compliance**: Supports tracking and reporting requirements for inter-utility energy transfers
- **Ledger Recording**: Provides the discom identifiers needed for immutable trade record creation

### Key Features

- Inherits all properties from `EnergyTradeOrder` (bap_id, bpp_id, total_quantity)
- Adds required utility/discom identifiers for both buyer and seller
- Clear distinction between utility IDs (discom) and customer IDs

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `bap_id` | string | Yes | (Inherited) BAP identifier | The buyer platform initiating the trade order |
| `bpp_id` | string | Yes | (Inherited) BPP identifier | The seller platform fulfilling the trade order |
| `total_quantity` | number | No | (Inherited) Total energy quantity (kWh) | Total energy for this trade order |
| `utilityIdBuyer` | string | Yes | Buyer-side utility/discom identifier | The distribution company the buyer is connected to. **NOT the buyer's customer ID.** |
| `utilityIdSeller` | string | Yes | Seller-side utility/discom identifier | The distribution company the seller is connected to. **NOT the seller's customer ID.** |

> **Important**: `utilityIdBuyer` and `utilityIdSeller` identify the distribution companies (discoms), not the customers. For customer identification, use `orderItemAttributes.utilityCustomerId`.

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Order.orderAttributes`

## Example Usage

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyTradeOrderInterUtility",
  "bap_id": "bap.energymarket.io",
  "bpp_id": "bpp.solarprovider.io",
  "total_quantity": 50.0,
  "utilityIdBuyer": "BESCOM-KA",
  "utilityIdSeller": "TPDDL-DL"
}
```
