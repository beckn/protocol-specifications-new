# EV Charging — Charging Service Attribute Pack (v1)

This pack defines **EV-specific attribute extensions only** (no Beckn core objects).

It reuses core Beckn schemas for Item, Offer, Order/Fulfillment, and Provider, and adds only **domain-specific attributes**relevant to electric-vehicle charging.

Attach these schemas as follows:

| **Attribute Schema** | **Attach To** | **Purpose** |
| --- | --- | --- |
| ChargingService | Item.attributes | Technical and contextual details of a charging connector or station - e.g., connector type, power capacity, socket count, reservation capability, and amenities. |
| --- | --- | --- |
| ChargingOffer | Offer.attributes | Tariff details beyond core price fields - e.g., per-kWh or time-based pricing, idle fee policies, buyer-finder fees, and accepted payment methods. |
| --- | --- | --- |
| ChargingSession | Order.fulfillments\[\].attributes | Real-time or completed charging session data - energy consumed, session duration, total cost, telemetry intervals, and tracking links. |
| --- | --- | --- |
| ChargingProvider | Provider.attributes | Operator identifiers, statutory registrations, and extended contact details for the charging provider. |
| --- | --- | --- |


## **🧭 Role and Design**

- **Aligned with Beckn Core  
    **Uses canonical Beckn schemas for common objects and reuses canonical components from:
  - [discover.yaml](https://raw.githubusercontent.com/abhimail/beckn/refs/heads/main/protocol-enhancements/discover.yaml) - Location, Address, GeoJSONGeometry
  - [transaction.yaml](https://raw.githubusercontent.com/abhimail/beckn/refs/heads/main/protocol-enhancements/transaction.yaml) - Order, Offer, Fulfillment, Payment, Context
- **Adds EV semantics only  
    **Introduces domain-specific elements such as connectors, power ratings, roaming networks, charging periods, and session telemetry.
- **Designed for interoperability  
    **Enables charging-point operators, aggregators, and mobility apps to exchange structured data seamlessly across Beckn networks.

## **🗺️ Local Namespace Mapping**

The ev namespace is mapped **locally**:

{ "ev": "./vacab/ev#" }

Vocabulary files live in v1/vocab/ and use this same local mapping.

When publishing, replace ./ev# with an absolute URL, e.g.:

<https://schemas.example.org/ev#>

This supports both local development and public hosting.

## **📂 Files and Folders**

| **File / Folder** | **Purpose** |
| --- | --- |
| **context.jsonld** | Maps all properties to schema.org and local ev: IRIs. Defines semantic equivalences (e.g., serviceLocation ≡ beckn:availableAt). |
| --- | --- |
| **attributes.yaml** | OpenAPI 3.1.1 attribute schemas for ChargingService, ChargingOffer, ChargingSession, and ChargingProvider, each annotated with x-jsonld. Reuses canonical Beckn components (e.g., Locationvia \$ref). |
| --- | --- |
| **profile.json** | Lists included schemas, operational/index hints, minimal attributes for discovery, and privacy guidance for implementers. |
| --- | --- |
| **renderer.json** | Defines rendering templates (HTML + JSON data paths) for discovery cards, offer chips, and session status views used in UI implementations. |
| --- | --- |
| **rules/** | **TBD** - will contain Spectral rules and JSON Schema (AJV) shims for automated validation. |
| --- | --- |
| **tools/** | **TBD** - jq and helper scripts for transformations or legacy migrations. |
| --- | --- |
| **examples/** | Contains working examples showing each attribute type in the context of Beckn discover and transaction flows. |
| --- | --- |
| **vocab/** | Local vocabulary for EV domain terms (connectorType, chargingSpeed, ocppId, etc.) in YAML and JSON-LD formats. |
| --- | --- |


## 🏷️ Tags
`ev-charging, mobility, energy, transport, electric-vehicle, sustainability, item, offer, order, fulfillment, provider, location, geo, discovery, reservation, session, connector, power, ocpp, ocpi, open-standards, beckn, json-ld, schema.org, openapi, ocpi, ocpp, iso-15118, schema-geoshape, iso4217`

These tags help implementers and schema registries discover and classify this attribute pack quickly.