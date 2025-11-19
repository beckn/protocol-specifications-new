# EnergyTradeContract Schema (v0.2)

## Introduction

The **EnergyTradeContract** schema composes with the core Beckn `Order` entity to represent commercial agreements for energy transactions in P2P energy trading systems. This schema decouples trade from fulfillment, allowing generator, transmitter, and consumer to operate independently of the contract.

### Use Cases

- **Contract Management**: Tracks commercial agreements between energy generators and consumers
- **Multi-Cycle Support**: Supports single contracts with multiple billing or fulfillment cycles (e.g., ongoing connections billed periodically)
- **Settlement Tracking**: Manages settlement cycles for recurring contracts
- **Billing Management**: Tracks billing cycles with detailed line items including energy costs and wheeling charges
- **Lifecycle Tracking**: Monitors contract status from pending through active, completed, or terminated states

### Key Features

- Decouples trade from fulfillment - parties operate independently
- Supports multiple settlement and billing cycles per contract
- Tracks meter identifiers for source and target
- Maintains inverter as consistent interface
- Records certification details at contract time
- Tracks utility wheeling charges

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `contractStatus` | enum | No | Contract lifecycle status: PENDING, ACTIVE, COMPLETED, TERMINATED | Tracks the current state of the contract. Decouples trade from fulfillment - generator, transmitter, and consumer operate independently. |
| `sourceMeterId` | string | No | Source meter identifier using IEEE 2030.5 mRID (meter Resource ID) | Identifies the energy generator's meter. Used for tracking energy flow and settlement calculations. Format: plain identifier (e.g., `"100200300"`), not `der://` format. |
| `targetMeterId` | string | No | Target/consumer meter identifier using IEEE 2030.5 mRID (meter Resource ID) | Identifies the energy consumer's meter. Used for tracking energy delivery and billing. Format: plain identifier (e.g., `"98765456"`), not `der://` format. |
| `inverterId` | string | No | Inverter identifier serving as consistent interface between source and grid | Provides stable reference point. Remains constant even if source changes. The inverter serves as the consistent interface between source and grid infrastructure. |
| `contractedQuantity` | number | No | Contracted energy quantity in kilowatt-hours (kWh) | The agreed-upon energy quantity for the contract. Used for tracking fulfillment against contract terms. |
| `tradeStartTime` | date-time | No | Contract start time (ISO 8601) | When the contract becomes effective. Used for billing and settlement period calculations. |
| `tradeEndTime` | date-time | No | Contract end time (ISO 8601). Null for ongoing contracts | When the contract expires. Null indicates an ongoing contract without a fixed end date. |
| `sourceType` | enum | No | Energy source type at contract time: SOLAR, BATTERY, GRID, HYBRID, RENEWABLE | Records the source type when the contract was created. May differ from current source type if source changes post-onboarding. |
| `certification` | object | No | Energy certification details at contract time | Snapshot of certification status when contract was created. Contains status and certificates array. |
| `certification.status` | string | No | Certification status (e.g., "Carbon Offset Certified", "Green Energy Certified") | Text description of certification at contract time. |
| `certification.certificates` | array&lt;uri&gt; | No | Array of certificate references (URLs or identifiers) | Links to certification documents valid at contract time. |
| `settlementCycles` | array | No | Array of settlement cycles for recurring contracts | Supports single order with multiple billing or fulfillment cycles. Each cycle contains cycleId, startTime, endTime, status, amount, and currency. Used for tracking payment processing. |
| `settlementCycles[].cycleId` | string | No | Unique settlement cycle identifier | Unique ID for referencing this settlement cycle (e.g., settle-2024-10-04-001). |
| `settlementCycles[].startTime` | date-time | No | Settlement cycle start time (ISO 8601) | Beginning of the settlement period. |
| `settlementCycles[].endTime` | date-time | No | Settlement cycle end time (ISO 8601) | End of the settlement period. |
| `settlementCycles[].status` | enum | No | Settlement cycle status: PENDING, SETTLED, FAILED | Current state of the settlement. PENDING = not yet processed, SETTLED = payment completed, FAILED = processing error. |
| `settlementCycles[].amount` | number | No | Settlement amount for this cycle | Total amount to be settled for this period. |
| `settlementCycles[].currency` | string | No | Currency code (ISO 4217) | Currency for the settlement amount. |
| `billingCycles` | array | No | Array of billing periods for the contract | Supports ongoing connections billed periodically. Each cycle contains cycleId, startTime, endTime, status, totalAmount, currency, and lineItems. |
| `billingCycles[].cycleId` | string | No | Unique billing cycle identifier | Unique ID for referencing this billing cycle (e.g., bill-2024-10-001). |
| `billingCycles[].startTime` | date-time | No | Billing cycle start time (ISO 8601) | Beginning of the billing period. |
| `billingCycles[].endTime` | date-time | No | Billing cycle end time (ISO 8601) | End of the billing period. |
| `billingCycles[].status` | enum | No | Billing cycle payment status: PENDING, PAID, OVERDUE | Payment status for this billing cycle. Used for accounts receivable management. |
| `billingCycles[].totalAmount` | number | No | Total billing amount for this cycle | Sum of all line items for this billing period. |
| `billingCycles[].currency` | string | No | Currency code (ISO 4217) | Currency for the billing amount. |
| `billingCycles[].lineItems` | array | No | Billing line items including energy cost and wheeling charges | Detailed breakdown of charges. Each item contains title, amount, and currency. Used for invoice generation and cost transparency. |
| `billingCycles[].lineItems[].title` | string | No | Line item title | Description of the charge (e.g., Energy Cost, Wheeling Charges). |
| `billingCycles[].lineItems[].amount` | number | No | Line item amount | Monetary value of this line item. |
| `billingCycles[].lineItems[].currency` | string | No | Currency code (ISO 4217) | Currency for this line item. |
| `wheelingCharges` | object | No | Utility wheeling charges breakdown (e.g., PG&E fixed charges) | Details of utility transmission charges. Contains utilityName, amount, currency, and description. |
| `wheelingCharges.utilityName` | string | No | Name of the utility providing wheeling services | Identifies the utility company (e.g., PG&E Grid Services). |
| `wheelingCharges.amount` | number | No | Total wheeling charge amount | Total charges from the utility for transmission services. |
| `wheelingCharges.currency` | string | No | Currency code (ISO 4217) | Currency for wheeling charges. |
| `wheelingCharges.description` | string | No | Description of wheeling charges | Human-readable description (e.g., Fixed wheeling charges for grid transmission). |
| `lastUpdated` | date-time | No | Last contract update timestamp (UTC) | Timestamp of the most recent contract modification. Used for change tracking and audit purposes. |

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Order.orderAttributes`

## Example Usage

See complete examples in:
- **Schema Example**: `../../EnergyResource/v0.2/examples/schema/order-example.json`
- **Transaction Flow Examples**: `../../EnergyResource/v0.2/examples/flows/` (init, confirm, status)
- **Implementation Guide**: `../../../docs/EnergyTrading_implementation_guide.md`

### Quick Example

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyTradeContract",
  "contractStatus": "ACTIVE",
  "sourceMeterId": "100200300",
  "targetMeterId": "98765456",
  "inverterId": "inv-12345",
  "contractedQuantity": 10.0,
  "tradeStartTime": "2024-10-04T10:00:00Z",
  "tradeEndTime": "2024-10-04T18:00:00Z",
  "sourceType": "SOLAR",
  "certification": {
    "status": "Carbon Offset Certified",
    "certificates": ["https://example.com/certs/solar-panel-cert.pdf"]
  },
  "settlementCycles": [
    {
      "cycleId": "settle-2024-10-04-001",
      "startTime": "2024-10-04T00:00:00Z",
      "endTime": "2024-10-04T23:59:59Z",
      "status": "SETTLED",
      "amount": 50.0,
      "currency": "USD"
    }
  ],
  "billingCycles": [
    {
      "cycleId": "bill-2024-10-001",
      "startTime": "2024-10-01T00:00:00Z",
      "endTime": "2024-10-31T23:59:59Z",
      "status": "PAID",
      "totalAmount": 150.0,
      "currency": "USD",
      "lineItems": [
        {
          "title": "Energy Cost",
          "amount": 100.0,
          "currency": "USD"
        }
      ]
    }
  ],
  "wheelingCharges": {
    "utilityName": "PG&E Grid Services",
    "amount": 2.5,
    "currency": "USD",
    "description": "Fixed wheeling charges for grid transmission"
  },
  "lastUpdated": "2024-10-04T15:30:00Z"
}
```

**Note**: Meter IDs use IEEE 2030.5 mRID format (`100200300`, `98765456`), not the legacy `der://` format.

