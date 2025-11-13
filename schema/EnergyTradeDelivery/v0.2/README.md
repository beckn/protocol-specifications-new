# EnergyTradeDelivery Schema (v0.2)

## Introduction

The **EnergyTradeDelivery** schema composes with the core Beckn `Fulfillment` entity to track the physical transfer of energy between source and target in P2P energy trading systems. This schema handles recurring or continuous fulfillment scenarios tied to a single contract, tracking delivery status, meter readings, and telemetry data.

### Use Cases

- **Delivery Tracking**: Monitors the physical transfer of energy from generator to consumer
- **Meter Reading Management**: Tracks meter readings at source and target meters to calculate actual energy flow
- **Telemetry Monitoring**: Captures real-time energy flow telemetry data (energy, power, voltage, current, frequency, power quality)
- **Settlement Integration**: Links delivery data to settlement cycles for accurate billing
- **Multi-Cycle Fulfillment**: Supports multiple fulfillment cycles per contract (e.g., daily deliveries under a monthly contract)

### Key Features

- Tracks delivery status throughout the fulfillment lifecycle
- Records meter readings to calculate actual energy delivered
- Captures telemetry metrics for energy quality monitoring
- Links to settlement cycles for billing reconciliation
- Supports continuous and recurring delivery scenarios

## Attributes

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `deliveryStatus` | enum | No | Delivery status: PENDING, IN_PROGRESS, COMPLETED, FAILED | Tracks the current state of energy delivery. Handles recurring or continuous fulfillment scenarios. Used for status updates and notifications. |
| `deliveryMode` | enum | No | Mode of energy delivery: EV_CHARGING, BATTERY_SWAP, V2G, GRID_INJECTION | Specifies how energy is being delivered in this fulfillment cycle. May differ from the contract's delivery mode if multiple methods are used. |
| `deliveredQuantity` | number | No | Quantity delivered in this fulfillment cycle in kilowatt-hours (kWh) | Actual energy quantity delivered. Updated as delivery progresses. Used for billing calculations and contract fulfillment tracking. |
| `deliveryStartTime` | date-time | No | Delivery start timestamp (ISO 8601) | When energy delivery began. Used for duration calculations and billing periods. |
| `deliveryEndTime` | date-time | No | Delivery end timestamp (ISO 8601). Null if delivery is in progress | When energy delivery completed. Null indicates delivery is still ongoing. |
| `meterReadings` | array | No | Array of meter readings during delivery | Tracks energy flow from source to target. Each reading contains timestamp, sourceReading, targetReading, and energyFlow. Used for accurate billing and dispute resolution. |
| `meterReadings[].timestamp` | date-time | No | Meter reading timestamp (ISO 8601) | When this meter reading was taken. Used for time-series analysis and billing calculations. |
| `meterReadings[].sourceReading` | number | No | Source meter reading at this timestamp (kWh) | Cumulative energy reading from the generator's meter. Used to calculate energy exported from source. |
| `meterReadings[].targetReading` | number | No | Target meter reading at this timestamp (kWh) | Cumulative energy reading from the consumer's meter. Used to calculate energy imported to target. |
| `meterReadings[].energyFlow` | number | No | Calculated energy flow between readings (kWh). Positive indicates delivery to target | Net energy transferred during this period. Positive values indicate successful delivery to consumer. Used for billing and verification. |
| `telemetry` | array | No | Energy flow telemetry data during delivery | Real-time energy quality and flow metrics. Each entry contains eventTime and metrics array. Similar to charging telemetry for EV sessions. Used for quality monitoring and optimization. |
| `telemetry[].eventTime` | date-time | No | Telemetry event timestamp (UTC) | When this telemetry reading was captured. |
| `telemetry[].metrics` | array | No | Array of telemetry metrics using schema.org QuantitativeValue | Energy quality and flow measurements. Each metric contains name, value, and unitCode. |
| `telemetry[].metrics[].name` | enum | No | Telemetry metric name: ENERGY, POWER, FLOW_RATE, VOLTAGE, CURRENT, FREQUENCY, POWER_QUALITY | Type of measurement. ENERGY (kWh) = total energy, POWER (kW) = instantaneous power, FLOW_RATE (kW) = energy flow rate, VOLTAGE (V) = voltage level, CURRENT (A) = current level, FREQUENCY (Hz) = grid frequency, POWER_QUALITY = quality metrics. |
| `telemetry[].metrics[].value` | number | No | Numeric value of the metric | The measured value for this metric. |
| `telemetry[].metrics[].unitCode` | string | No | Unit code for the metric value | Standard unit code: KWH for ENERGY, KW for POWER/FLOW_RATE, VLT for VOLTAGE, AMP for CURRENT, HZ for FREQUENCY, dimensionless for POWER_QUALITY. |
| `settlementCycleId` | string | No | Associated settlement cycle identifier | Links this delivery to a specific settlement cycle in the contract. Used for billing reconciliation and payment processing. |
| `lastUpdated` | date-time | No | Last delivery update timestamp (UTC) | Timestamp of the most recent delivery update. Updated as meter readings and telemetry arrive. Used for change tracking and real-time monitoring. |

## Schema Composition Point

This schema composes with: `core/v2/core.yaml#Fulfillment.attributes`

## Example Usage

```json
{
  "@context": "./context.jsonld",
  "@type": "EnergyTradeDelivery",
  "deliveryStatus": "IN_PROGRESS",
  "deliveryMode": "GRID_INJECTION",
  "deliveredQuantity": 9.8,
  "deliveryStartTime": "2024-10-04T10:00:00Z",
  "deliveryEndTime": null,
  "meterReadings": [
    {
      "timestamp": "2024-10-04T12:00:00Z",
      "sourceReading": 1000.5,
      "targetReading": 990.3,
      "energyFlow": 10.2
    }
  ],
  "telemetry": [
    {
      "eventTime": "2024-10-04T12:00:00Z",
      "metrics": [
        {
          "name": "ENERGY",
          "value": 5.8,
          "unitCode": "KWH"
        },
        {
          "name": "POWER",
          "value": 2.5,
          "unitCode": "KW"
        },
        {
          "name": "VOLTAGE",
          "value": 240.0,
          "unitCode": "VLT"
        }
      ]
    }
  ],
  "settlementCycleId": "settle-2024-10-04-001",
  "lastUpdated": "2024-10-04T15:30:00Z"
}
```

