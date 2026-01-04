# EnergyCustomer Attributes Schema (v0.1)

This schema defines attributes for energy customers in the Beckn Protocol, supporting consumers, producers, and prosumers (both consumers and producers) in P2P energy trading and program enrollment flows.

## Schema Overview

The `EnergyCustomer` schema provides essential customer identification and capacity information for energy market participants.

### Properties

#### Required Properties

- **`meterId`** (string): Meter identifier in DER address format (`der://meter/{id}`). Used for customer identification and energy delivery tracking in P2P trading flows.

#### Optional Properties

- **`sanctionedLoad`** (number): Sanctioned load capacity in kilowatts (kW). Represents the approved electrical load capacity for the customer's connection. Used for load management and regulatory compliance.

## Usage

This schema is used in:

1. **`orderItemAttributes`** (init request): Contains `targetMeterId` for delivery destination
2. **`orderItemAttributes`** (responses): Contains `targetMeterId` for delivery destination
3. **`buyerAttributes`** (enrollment): Contains `meterId` and `sanctionedLoad` for customer identification

## Example

```json
{
  "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/main/schema/EnergyCustomer/v0.1/context.jsonld",
  "@type": "EnergyCustomer",
  "meterId": "der://meter/98765456",
  "sanctionedLoad": 15.0
}
```

## Usage in Order Items

In order item attributes, the `meterId` is required along with `@context` and `@type`:

```json
"beckn:orderItemAttributes": {
  "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/main/schema/EnergyCustomer/v0.1/context.jsonld",
  "@type": "EnergyCustomer",
  "meterId": "der://meter/98765456"
}
```

## Version History

- **v0.1**: Initial release with basic customer identification and capacity attributes
