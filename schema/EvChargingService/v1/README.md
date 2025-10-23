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
  - [core.yaml](../core/v2/core.yaml) - Catalog, Item, Offer, Provider, Attributes, Location, Address, GeoJSONGeometry
  - [discover.yaml](../../api-specs/discover.yaml) - Discovery API endpoints and request/response schemas
  - [transaction.yaml](../../api-specs/transaction.yaml) - Transaction API endpoints and Order, Fulfillment, Payment schemas
- **Adds EV semantics only  
    **Introduces domain-specific elements such as connectors, power ratings, roaming networks, charging periods, and session telemetry.
- **Designed for interoperability  
    **Enables charging-point operators, aggregators, and mobility apps to exchange structured data seamlessly across Beckn networks.

## **🗺️ Local Namespace Mapping**

The beckn namespace is mapped **locally**:

{ "beckn": "./vocab.jsonld#" }

Vocabulary files live in v1/vocab.jsonld and use this same local mapping.

When publishing, replace ./vocab.jsonld# with an absolute URL, e.g.:

<https://schemas.example.org/ev-charging/v1/vocab.jsonld#>

This supports both local development and public hosting.

## **📂 Files and Folders**

| **File / Folder** | **Purpose** |
| --- | --- |
| **context.jsonld** | Maps all properties to schema.org and local beckn: IRIs. Defines semantic equivalences (e.g., serviceLocation ≡ beckn:availableAt). |
| --- | --- |
| **attributes.yaml** | OpenAPI 3.1.1 attribute schemas for ChargingService, ChargingOffer, ChargingSession, and ChargingProvider, each annotated with x-jsonld. Reuses canonical Beckn components (e.g., Location via \$ref). |
| --- | --- |
| **profile.json** | Lists included schemas, operational/index hints, minimal attributes for discovery, and privacy guidance for implementers. |
| --- | --- |
| **renderer.json** | Defines rendering templates (HTML + JSON data paths) for discovery cards, offer chips, and session status views used in UI implementations. |
| --- | --- |
| **vocab.jsonld** | Local vocabulary for EV domain terms (connectorType, chargingSpeed, ocppId, etc.) in JSON-LD format with RDFS definitions and semantic relationships. |
| --- | --- |
| **examples/** | Contains working examples showing each attribute type in the context of Beckn discover and transaction flows. |
| --- | --- |


## 🏷️ Tags
`ev-charging, mobility, energy, transport, electric-vehicle, sustainability, item, offer, order, fulfillment, provider, location, geo, discovery, reservation, session, connector, power, ocpp, ocpi, open-standards, beckn, json-ld, schema.org, openapi, ocpi, ocpp, iso-15118, schema-geoshape, iso4217`

These tags help implementers and schema registries discover and classify this attribute pack quickly.