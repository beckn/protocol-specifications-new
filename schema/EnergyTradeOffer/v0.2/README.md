# EnergyTradeOffer Schema (v0.2)

## Introduction

The **EnergyTradeOffer** schema composes with the core Beckn `Offer` entity to represent available trade offers for energy resources in P2P energy trading systems. This schema defines pricing models, settlement types, wheeling charges, and availability details for energy trading offers.

### Use Cases

- **Offer Discovery**: Enables consumers to discover available energy trade offers with specific pricing and terms
- **Pricing Models**: Supports multiple pricing structures (per-kWh, time-of-day, subscription, fixed)
- **Settlement Configuration**: Defines when and how payments are processed (real-time, hourly, daily, weekly, monthly)
- **Utility Integration**: Tracks wheeling charges from utility intermediaries (e.g., PG&E) as billing line items
- **Quantity Limits**: Defines minimum and maximum tradable quantities for each offer

### Key Features

- Multiple pricing models including time-of-day rates
- Flexible settlement frequencies
- Utility wheeling charge tracking
- Offer validity windows
- Quantity constraints

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `pricingModel` | enum | Yes | Pricing model classification: PER_KWH, TIME_OF_DAY, SUBSCRIPTION, FIXED | Determines how the energy price is calculated. PER_KWH charges per unit, TIME_OF_DAY varies by time, SUBSCRIPTION is recurring, FIXED is a flat rate. |
| `settlementType` | enum | No | Settlement frequency: REAL_TIME, HOURLY, DAILY, WEEKLY, MONTHLY | Defines when payments are processed. REAL_TIME processes immediately, others batch at specified intervals. Used for cash flow management and reconciliation. |
| `wheelingCharges` | object | No | Utility wheeling charges (fixed charges for delivery intermediaries like PG&E) | Tracks charges from utility companies that facilitate energy transmission. Reflected as billing line item. Contains amount, currency, and description. |
| `wheelingCharges.amount` | number | No | Wheeling charge amount | The monetary value of utility transmission charges. |
| `wheelingCharges.currency` | string | No | Currency code (ISO 4217) | Currency for the wheeling charge (e.g., USD, EUR). |
| `wheelingCharges.description` | string | No | Description of the wheeling charge | Human-readable description (e.g., PG&E Grid Services wheeling charge). |
| `minimumQuantity` | number | No | Minimum tradable energy quantity in kilowatt-hours (kWh) | Minimum energy quantity required for this offer. Prevents micro-transactions and ensures cost-effective trades. |
| `maximumQuantity` | number | No | Maximum tradable energy quantity in kilowatt-hours (kWh) | Maximum energy quantity available in this offer. Used to limit large single transactions. |
| `validityWindow` | object | No | Time window when the offer is valid | Defines when the offer can be accepted. Contains start and end timestamps (ISO 8601). Used for time-limited promotions or availability windows. |
| `validityWindow.start` | date-time | No | Offer validity start time (ISO 8601) | When the offer becomes available for acceptance. |
| `validityWindow.end` | date-time | No | Offer validity end time (ISO 8601) | When the offer expires and can no longer be accepted. |
| `timeOfDayRates` | array | No | Time-of-day pricing rates (applicable when pricingModel is TIME_OF_DAY) | Array of rate structures for different time periods. Each entry contains timeRange (start/end times) and rate (price per kWh) with currency. Used for dynamic pricing based on demand or production costs. |
| `timeOfDayRates[].timeRange` | object | No | Time range for this rate | Defines the time period when this rate applies. Contains start and end times in HH:MM format. |
| `timeOfDayRates[].timeRange.start` | time | No | Start time (HH:MM format) | Beginning of the time range (e.g., 09:00). |
| `timeOfDayRates[].timeRange.end` | time | No | End time (HH:MM format) | End of the time range (e.g., 17:00). |
| `timeOfDayRates[].rate` | number | No | Price per kWh for this time range | The energy price during this time period. |
| `timeOfDayRates[].currency` | string | No | Currency code (ISO 4217) | Currency for the rate (e.g., USD). |

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Offer.offerAttributes`

## Example Usage

See complete examples in:
- **Schema Example**: `../../EnergyResource/v0.2/examples/schema/offer-example.json`
- **Transaction Flow Examples**: `../../EnergyResource/v0.2/examples/flows/` (discover, select, init, confirm, status)
- **Implementation Guide**: `../../../docs/EnergyTrading_implementation_guide.md`

### Quick Example

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyTradeOffer",
  "pricingModel": "TIME_OF_DAY",
  "settlementType": "DAILY",
  "wheelingCharges": {
    "amount": 2.5,
    "currency": "USD",
    "description": "PG&E Grid Services wheeling charge"
  },
  "minimumQuantity": 1.0,
  "maximumQuantity": 100.0,
  "validityWindow": {
    "start": "2024-10-04T00:00:00Z",
    "end": "2024-10-04T23:59:59Z"
  },
  "timeOfDayRates": [
    {
      "timeRange": {
        "start": "09:00",
        "end": "17:00"
      },
      "rate": 0.15,
      "currency": "USD"
    }
  ]
}
```

