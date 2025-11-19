# v1 to v2 Field Mapping Table

## Overview

This document provides a comprehensive mapping between v1 layer2 fields and v2 composable schema fields for P2P Energy Trading.

## Field Mapping Reference

### Item Attributes (EnergyResource)

| v1 Location | v1 Format/Example | v2 Location | v2 Schema | Status | Notes |
|-------------|-------------------|-------------|-----------|--------|-------|
| `Item.attributes.sourceType` | `Tag.value: "SOLAR"` or direct attribute | `Item.itemAttributes.sourceType` | `EnergyResource` | ✅ Mapped | Enum: SOLAR, BATTERY, GRID, HYBRID, RENEWABLE |
| `Item.attributes.deliveryMode` | `Tag.value: "GRID_INJECTION"` or direct | `Item.itemAttributes.deliveryMode` | `EnergyResource` | ✅ Mapped | Enum: EV_CHARGING, BATTERY_SWAP, V2G, GRID_INJECTION |
| `Item.attributes.certificationStatus` | String: "Carbon Offset Certified" | `Item.itemAttributes.certificationStatus` | `EnergyResource` | ✅ Mapped | Free-form string |
| `Item.attributes.meterId` | `der://meter/100200300` | `Item.itemAttributes.meterId` | `EnergyResource` | ✅ Mapped | **Format change**: v1 uses `der://`, v2 uses IEEE mRID `100200300` |
| `Item.attributes.inverterId` | String: "inv-12345" | `Item.itemAttributes.inverterId` | `EnergyResource` | ✅ Mapped | |
| `Item.attributes.availableQuantity` | Number: 30.5 | `Item.itemAttributes.availableQuantity` | `EnergyResource` | ✅ Mapped | Units: kWh |
| `Item.attributes.productionWindow.start` | ISO 8601: "2024-10-04T10:00:00Z" | `Item.itemAttributes.productionWindow.start` | `EnergyResource` | ✅ Mapped | |
| `Item.attributes.productionWindow.end` | ISO 8601: "2024-10-04T18:00:00Z" | `Item.itemAttributes.productionWindow.end` | `EnergyResource` | ✅ Mapped | |
| `Item.attributes.sourceVerification.verified` | Boolean: true | `Item.itemAttributes.sourceVerification.verified` | `EnergyResource` | ✅ Mapped | |
| `Item.attributes.sourceVerification.verificationDate` | ISO 8601: "2024-09-01T00:00:00Z" | `Item.itemAttributes.sourceVerification.verificationDate` | `EnergyResource` | ✅ Mapped | |
| `Item.attributes.sourceVerification.certificates` | Array of URIs | `Item.itemAttributes.sourceVerification.certificates` | `EnergyResource` | ✅ Mapped | |
| `Item.attributes.productionAsynchronous` | Boolean: true | `Item.itemAttributes.productionAsynchronous` | `EnergyResource` | ✅ Mapped | Default: false |

### Offer Attributes (EnergyTradeOffer)

| v1 Location | v1 Format/Example | v2 Location | v2 Schema | Status | Notes |
|-------------|-------------------|-------------|-----------|--------|-------|
| `Offer.attributes.pricingModel` | `Tag.value: "PER_KWH"` or direct | `Offer.offerAttributes.pricingModel` | `EnergyTradeOffer` | ✅ Mapped | Enum: PER_KWH, TIME_OF_DAY, SUBSCRIPTION, FIXED |
| `Offer.attributes.settlementType` | `Tag.value: "DAILY"` or direct | `Offer.offerAttributes.settlementType` | `EnergyTradeOffer` | ✅ Mapped | Enum: REAL_TIME, HOURLY, DAILY, WEEKLY, MONTHLY |
| `Offer.attributes.wheelingCharges.amount` | Number: 2.5 | `Offer.offerAttributes.wheelingCharges.amount` | `EnergyTradeOffer` | ✅ Mapped | |
| `Offer.attributes.wheelingCharges.currency` | String: "USD" | `Offer.offerAttributes.wheelingCharges.currency` | `EnergyTradeOffer` | ✅ Mapped | ISO 4217 |
| `Offer.attributes.wheelingCharges.description` | String: "PG&E Grid Services..." | `Offer.offerAttributes.wheelingCharges.description` | `EnergyTradeOffer` | ✅ Mapped | |
| `Offer.attributes.minimumQuantity` | Number: 1.0 | `Offer.offerAttributes.minimumQuantity` | `EnergyTradeOffer` | ✅ Mapped | Units: kWh |
| `Offer.attributes.maximumQuantity` | Number: 100.0 | `Offer.offerAttributes.maximumQuantity` | `EnergyTradeOffer` | ✅ Mapped | Units: kWh |
| `Offer.attributes.validityWindow.start` | ISO 8601 | `Offer.offerAttributes.validityWindow.start` | `EnergyTradeOffer` | ✅ Mapped | |
| `Offer.attributes.validityWindow.end` | ISO 8601 | `Offer.offerAttributes.validityWindow.end` | `EnergyTradeOffer` | ✅ Mapped | |
| `Offer.attributes.timeOfDayRates[]` | Array of rate objects | `Offer.offerAttributes.timeOfDayRates[]` | `EnergyTradeOffer` | ✅ Mapped | For TIME_OF_DAY pricing |

### Order Attributes (EnergyTradeContract)

| v1 Location | v1 Format/Example | v2 Location | v2 Schema | Status | Notes |
|-------------|-------------------|-------------|-----------|--------|-------|
| `Order.attributes.contractStatus` | String: "ACTIVE" | `Order.orderAttributes.contractStatus` | `EnergyTradeContract` | ✅ Mapped | Enum: PENDING, ACTIVE, COMPLETED, TERMINATED |
| `Order.attributes.sourceMeterId` | `der://pge.meter/100200300` | `Order.orderAttributes.sourceMeterId` | `EnergyTradeContract` | ✅ Mapped | **Format change**: v1 uses `der://`, v2 uses IEEE mRID |
| `Order.attributes.targetMeterId` | `der://ssf.meter/98765456` | `Order.orderAttributes.targetMeterId` | `EnergyTradeContract` | ✅ Mapped | **Format change**: v1 uses `der://`, v2 uses IEEE mRID |
| `Order.attributes.inverterId` | String: "inv-12345" | `Order.orderAttributes.inverterId` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.contractedQuantity` | Number: 10.0 | `Order.orderAttributes.contractedQuantity` | `EnergyTradeContract` | ✅ Mapped | Units: kWh |
| `Order.attributes.tradeStartTime` | ISO 8601 | `Order.orderAttributes.tradeStartTime` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.tradeEndTime` | ISO 8601 | `Order.orderAttributes.tradeEndTime` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.sourceType` | String: "SOLAR" | `Order.orderAttributes.sourceType` | `EnergyTradeContract` | ✅ Mapped | Enum: SOLAR, BATTERY, GRID, HYBRID, RENEWABLE |
| `Order.attributes.certification.status` | String | `Order.orderAttributes.certification.status` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.certification.certificates` | Array of URIs | `Order.orderAttributes.certification.certificates` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.settlementCycles[]` | Array of cycle objects | `Order.orderAttributes.settlementCycles[]` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.billingCycles[]` | Array of cycle objects | `Order.orderAttributes.billingCycles[]` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.wheelingCharges` | Object | `Order.orderAttributes.wheelingCharges` | `EnergyTradeContract` | ✅ Mapped | |
| `Order.attributes.lastUpdated` | ISO 8601 | `Order.orderAttributes.lastUpdated` | `EnergyTradeContract` | ✅ Mapped | |

### Fulfillment Attributes (EnergyTradeDelivery)

| v1 Location | v1 Format/Example | v2 Location | v2 Schema | Status | Notes |
|-------------|-------------------|-------------|-----------|--------|-------|
| `Fulfillment.attributes.deliveryStatus` | String: "IN_PROGRESS" | `Fulfillment.attributes.deliveryStatus` | `EnergyTradeDelivery` | ✅ Mapped | Enum: PENDING, IN_PROGRESS, COMPLETED, FAILED |
| `Fulfillment.attributes.deliveryMode` | String: "GRID_INJECTION" | `Fulfillment.attributes.deliveryMode` | `EnergyTradeDelivery` | ✅ Mapped | Enum: EV_CHARGING, BATTERY_SWAP, V2G, GRID_INJECTION |
| `Fulfillment.attributes.deliveredQuantity` | Number: 9.8 | `Fulfillment.attributes.deliveredQuantity` | `EnergyTradeDelivery` | ✅ Mapped | Units: kWh |
| `Fulfillment.attributes.deliveryStartTime` | ISO 8601 | `Fulfillment.attributes.deliveryStartTime` | `EnergyTradeDelivery` | ✅ Mapped | |
| `Fulfillment.attributes.deliveryEndTime` | ISO 8601 | `Fulfillment.attributes.deliveryEndTime` | `EnergyTradeDelivery` | ✅ Mapped | |
| `Fulfillment.attributes.meterReadings[]` | Array of reading objects | `Fulfillment.attributes.meterReadings[]` | `EnergyTradeDelivery` | ✅ Mapped | |
| `Fulfillment.attributes.telemetry[]` | Array of telemetry objects | `Fulfillment.attributes.telemetry[]` | `EnergyTradeDelivery` | ✅ Mapped | |
| `Fulfillment.attributes.settlementCycleId` | String: "settle-2024-10-04-001" | `Fulfillment.attributes.settlementCycleId` | `EnergyTradeDelivery` | ✅ Mapped | |
| `Fulfillment.attributes.lastUpdated` | ISO 8601 | `Fulfillment.attributes.lastUpdated` | `EnergyTradeDelivery` | ✅ Mapped | |

### Fulfillment Stops (Location-based)

| v1 Location | v1 Format/Example | v2 Location | v2 Schema | Status | Notes |
|-------------|-------------------|-------------|-----------|--------|-------|
| `Fulfillment.stops[].location.address` | `der://pge.meter/100200300` | `Fulfillment.stops[].location.address` | Core `Location` | ✅ Mapped | **Format change**: v1 uses `der://`, v2 uses IEEE mRID |
| `Fulfillment.stops[].type` | `"START"` or `"END"` | `Fulfillment.stops[].type` | Core `Stop` | ✅ Mapped | Enum: START, END |
| `Fulfillment.stops[].location` | Object with address | `Fulfillment.stops[].location` | Core `Location` | ✅ Mapped | |

### Payment Attributes (Core Schema)

| v1 Location | v1 Format/Example | v2 Location | v2 Schema | Status | Notes |
|-------------|-------------------|-------------|-----------|--------|-------|
| `Payment.type` | Enum: PRE-ORDER, ON-FULFILLMENT, POST-FULFILLMENT | `Payment.type` | Core `Payment` | ✅ Mapped | Core schema, not Energy* |
| `Payment.status` | Enum: PAID, NOT-PAID | `Payment.status` | Core `Payment` | ✅ Mapped | Core schema, not Energy* |
| `Payment.collected_by` | Enum: BAP, BPP | `Payment.collected_by` | Core `Payment` | ✅ Mapped | Core schema, not Energy* |

## Format Changes

### Meter ID Format Migration

**v1 Format**: `der://{utility}.meter/{id}` or `der://meter/{id}`
- Example: `der://pge.meter/100200300`
- Example: `der://ssf.meter/98765456`

**v2 Format**: IEEE 2030.5 mRID (plain identifier)
- Example: `100200300`
- Example: `98765456`

**Migration Rule**: Extract the numeric ID from the `der://` URI and use it directly.

### Attribute Path Changes

**v1**: `Item.attributes.*`  
**v2**: `Item.itemAttributes.*`

**v1**: `Offer.attributes.*`  
**v2**: `Offer.offerAttributes.*`

**v1**: `Order.attributes.*`  
**v2**: `Order.orderAttributes.*`

**v1**: `Fulfillment.attributes.*`  
**v2**: `Fulfillment.attributes.*` (no change)

## Tag-based Fields (v1) → Direct Attributes (v2)

In v1, some energy-specific fields may be sent as `Tag.value`:
- Energy source type: `Tag.value: "SOLAR"`
- Settlement type: `Tag.value: "DAILY"`
- Pricing model: `Tag.value: "PER_KWH"`

In v2, these are direct attributes:
- `itemAttributes.sourceType: "SOLAR"`
- `offerAttributes.settlementType: "DAILY"`
- `offerAttributes.pricingModel: "PER_KWH"`

## Summary

### ✅ All Fields Mapped

All v1 fields have been successfully mapped to v2 schemas:
- **EnergyResource**: 12 fields mapped
- **EnergyTradeOffer**: 9 fields mapped
- **EnergyTradeContract**: 15 fields mapped
- **EnergyTradeDelivery**: 9 fields mapped
- **Fulfillment Stops**: 3 fields mapped
- **Payment**: 3 fields mapped (core schema)

### ⚠️ Format Changes Required

1. **Meter ID Format**: Convert `der://meter/{id}` to `{id}` (IEEE mRID)
2. **Attribute Paths**: Change `attributes.*` to `itemAttributes.*`, `offerAttributes.*`, `orderAttributes.*`
3. **Tag Values**: Convert `Tag.value` to direct attribute fields

### 📝 Notes

1. All enums match between v1 and v2
2. All data types are compatible
3. No fields are missing in v2 schemas
4. JSON-LD context is added in v2 (not in v1)

