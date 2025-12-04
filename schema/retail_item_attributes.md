### Retail Item & Fulfillment Attribute Breakdown (ONDC Examples)

This document summarizes **item-level attributes** from the four ONDC retail example payloads, to help design `beckn:itemAttributes` that can be composed with the core `Item` (`attributes.yaml` lines 66–117). It focuses only on the main sellable item under `message.catalog."bpp/providers"[].items[]`, excluding provider-, catalog-, or fulfillment-level data.

It also provides a brief view of **fulfillment-related attributes** (delivery/pickup capabilities and timing/serviceability policies) so they can be modeled separately from item attributes, similar to how EV Charging splits Item vs Order/Fulfillment vs Offer attributes.

---

### Food & Beverage (`ondc_food_and_beverage.json`)

Item reference: `message.catalog."bpp/providers"[0].items[0]` (e.g., "Farmhouse Pizza").

- **Core identity & classification**
  - `id`
  - `category_id`
  - `category_ids[]` (fine-grained category path)
  - `fulfillment_id`
  - `location_id`
  - `related` (boolean – whether this is a related item)
  - `recommended` (boolean – recommendation flag)
- **Lifecycle & rating**
  - `time.label`
  - `time.timestamp`
  - `rating`
- **Descriptor**
  - `descriptor.name`
  - `descriptor.symbol`
  - `descriptor.short_desc`
  - `descriptor.long_desc`
  - `descriptor.images[]`
- **Quantity**
  - `quantity.unitized.measure.unit`
  - `quantity.unitized.measure.value`
  - `quantity.available.count`
  - `quantity.maximum.count`
- **Price & price ranges**
  - `price.currency`
  - `price.value`
  - `price.maximum_value`
  - `price.tags`:
    - `code = "range"` → `list[].code = "lower" | "upper"`, `list[].value`
    - `code = "default_selection"` → `list[].code = "value" | "maximum_value"`, `list[].value`
- **Returns, cancellation, and shipping**
  - `@ondc/org/returnable`
  - `@ondc/org/cancellable`
  - `@ondc/org/return_window`
  - `@ondc/org/seller_pickup_return`
  - `@ondc/org/time_to_ship`
  - `@ondc/org/available_on_cod`
- **Consumer care**
  - `@ondc/org/contact_details_consumer_care`
- **Tags (configuration & dietary)**
  - `tags[]`:
    - `code = "type"` → `list[].code = "type"`, `list[].value = "item"`
    - `code = "custom_group"` → `list[].code = "id"`, `list[].value` (customization group id)
    - `code = "config"` → `list[].code = "id" | "min" | "max" | "seq"`, `list[].value`
    - `code = "veg_nonveg"` → `list[].code = "veg"`, `list[].value`

_(Note: the same file also contains customization items `C1`, `C2`, `C3` under `items[]`; their structure can be treated as variant/customization attributes if needed, but are not repeated here.)_

---

### Grocery Catalog (`ondc_grocery_catalog.json`)

Item reference: `message.catalog."bpp/providers"[0].items[0]` (e.g., "Atta").

- **Core identity & classification**
  - `id`
  - `category_id`
  - `fulfillment_id`
  - `location_id`
- **Descriptor**
  - `descriptor.name`
  - `descriptor.code`
  - `descriptor.symbol`
  - `descriptor.short_desc`
  - `descriptor.long_desc`
  - `descriptor.images[]`
- **Quantity**
  - `quantity.available.count`
  - `quantity.maximum.count`
- **Price**
  - `price.currency`
  - `price.value`
  - `price.maximum_value`
- **Returns, cancellation, and shipping**
  - `@ondc/org/returnable`
  - `@ondc/org/cancellable`
  - `@ondc/org/return_window`
  - `@ondc/org/seller_pickup_return`
  - `@ondc/org/time_to_ship`
  - `@ondc/org/available_on_cod`
- **Consumer care**
  - `@ondc/org/contact_details_consumer_care`
- **Statutory – packaged commodities**
  - `@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_name`
  - `@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_address`
  - `@ondc/org/statutory_reqs_packaged_commodities.common_or_generic_name_of_commodity`
  - `@ondc/org/statutory_reqs_packaged_commodities.net_quantity_or_measure_of_commodity_in_pkg`
  - `@ondc/org/statutory_reqs_packaged_commodities.month_year_of_manufacture_packing_import`
- **Statutory – prepackaged food**
  - `@ondc/org/statutory_reqs_prepackaged_food.nutritional_info`
  - `@ondc/org/statutory_reqs_prepackaged_food.additives_info`
  - `@ondc/org/statutory_reqs_prepackaged_food.brand_owner_FSSAI_license_no`
  - `@ondc/org/statutory_reqs_prepackaged_food.other_FSSAI_license_no`
  - `@ondc/org/statutory_reqs_prepackaged_food.importer_FSSAI_license_no`
- **Mandatory – fruits & vegetables**
  - `@ondc/org/mandatory_reqs_veggies_fruits.net_quantity`
- **Dietary tags**
  - `tags.veg`
  - `tags.non_veg`

---

### Health & Wellness (`ondc_health_and_wellness.json`)

Item reference: `message.catalog."bpp/providers"[0].items[0]` (e.g., "Calcium and Vitamin D3 tablets").

- **Core identity & classification**
  - `id`
  - `category_id`
  - `fulfillment_id`
  - `location_id`
- **Lifecycle & rating**
  - `time.label`
  - `time.timestamp`
  - `rating`
- **Descriptor**
  - `descriptor.name`
  - `descriptor.code`
  - `descriptor.symbol`
  - `descriptor.short_desc`
  - `descriptor.long_desc`
  - `descriptor.images[]`
- **Quantity**
  - `quantity.unitized.measure.unit`
  - `quantity.unitized.measure.value`
  - `quantity.available.count`
  - `quantity.maximum.count`
- **Price**
  - `price.currency`
  - `price.value`
  - `price.maximum_value`
- **Returns, cancellation, and shipping**
  - `@ondc/org/returnable`
  - `@ondc/org/cancellable`
  - `@ondc/org/return_window`
  - `@ondc/org/seller_pickup_return`
  - `@ondc/org/time_to_ship`
  - `@ondc/org/available_on_cod`
- **Consumer care**
  - `@ondc/org/contact_details_consumer_care`
- **Statutory – packaged commodities**
  - `@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_name`
  - `@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_address`
  - `@ondc/org/statutory_reqs_packaged_commodities.mfg_license_no`
  - `@ondc/org/statutory_reqs_packaged_commodities.common_or_generic_name_of_commodity`
  - `@ondc/org/statutory_reqs_packaged_commodities.multiple_products_name_number_or_qty`
  - `@ondc/org/statutory_reqs_packaged_commodities.month_year_of_manufacture_packing_import`
  - `@ondc/org/statutory_reqs_packaged_commodities.expiry_date`
- **Statutory – prepackaged food**
  - `@ondc/org/statutory_reqs_prepackaged_food.ingredients_info`
- **Tags – origin, imagery, attributes**
  - `tags[]`:
    - `code = "origin"` → `list[].code = "country"`, `list[].value`
    - `code = "image"` → `list[].code = "type" | "url"`, `list[].value`
    - `code = "attribute"` → `list[].code = "brand" | "prescription_required"`, `list[].value`

---

### Home & Kitchen (`ondc_home_and_kitchen.json`)

Item reference: `message.catalog."bpp/providers"[0].items[0]` (e.g., "Satin Double Bedsheet with Two Pillow Covers").

- **Core identity & classification**
  - `id`
  - `category_id`
  - `fulfillment_id`
  - `location_id`
- **Lifecycle & rating**
  - `time.label`
  - `time.timestamp`
  - `rating`
- **Descriptor**
  - `descriptor.name`
  - `descriptor.code`
  - `descriptor.symbol`
  - `descriptor.short_desc`
  - `descriptor.long_desc`
  - `descriptor.images[]`
- **Quantity**
  - `quantity.unitized.measure.unit`
  - `quantity.unitized.measure.value`
  - `quantity.available.count`
  - `quantity.maximum.count`
- **Price**
  - `price.currency`
  - `price.value`
  - `price.maximum_value`
- **Returns, cancellation, and shipping**
  - `@ondc/org/returnable`
  - `@ondc/org/cancellable`
  - `@ondc/org/return_window`
  - `@ondc/org/seller_pickup_return`
  - `@ondc/org/time_to_ship`
  - `@ondc/org/available_on_cod`
- **Consumer care**
  - `@ondc/org/contact_details_consumer_care`
- **Statutory – packaged commodities**
  - `@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_name`
  - `@ondc/org/statutory_reqs_packaged_commodities.manufacturer_or_packer_address`
  - `@ondc/org/statutory_reqs_packaged_commodities.common_or_generic_name_of_commodity`
  - `@ondc/org/statutory_reqs_packaged_commodities.month_year_of_manufacture_packing_import`
- **Tags – origin, imagery, attributes**
  - `tags[]`:
    - `code = "origin"` → `list[].code = "country"`, `list[].value` (e.g., "IND")
    - `code = "image"` → `list[].code = "type" | "url"`, `list[].value` (e.g., type="back_image", url="https://...")
    - `code = "attribute"` → `list[].code = "brand" | "colour" | "colour_name" | "material"`, `list[].value` (e.g., brand="Hiyanshi", colour="#000000", colour_name="Black", material="cotton")

---

### Attributes Common to All Four Item Examples (Candidate Parent Item)

Across the four retail examples, the following **item-level attributes are present in all** and are good candidates for a shared parent item (to then specialize via domain-specific `beckn:itemAttributes`):

- **Core identity & linkage**
  - `id`
  - `category_id`
  - `fulfillment_id`
  - `location_id`
- **Descriptor (presentation)**
  - `descriptor.name`
  - `descriptor.symbol`
  - `descriptor.short_desc`
  - `descriptor.long_desc`
  - `descriptor.images[]`
- **Quantity (availability caps)**
  - `quantity.available.count`
  - `quantity.maximum.count`
- **Price (basic commercial terms)**
  - `price.currency`
  - `price.value`
  - `price.maximum_value`
- **Returns, cancellation, and shipping**
  - `@ondc/org/returnable`
  - `@ondc/org/cancellable`
  - `@ondc/org/return_window`
  - `@ondc/org/seller_pickup_return`
  - `@ondc/org/time_to_ship`
  - `@ondc/org/available_on_cod`
- **Consumer care**
  - `@ondc/org/contact_details_consumer_care`

You can treat these as **parent item attributes**, and then plug in **domain-specific item attributes** (e.g., statutory blocks, dietary flags, customization configuration, material/colour, prescription flags) via `beckn:itemAttributes` for each retail domain.

---

### Fulfillment Attribute Breakdown (ONDC Examples)

This section captures **fulfillment-related attributes** that should live on **Fulfillment / provider-level attributes**, not on `beckn:itemAttributes`.

#### Common Fulfillment Attributes (across examples)

- **Fulfillment types supported by the BPP**
  - `catalog."bpp/fulfillments"[].id`
  - `catalog."bpp/fulfillments"[].type` (e.g., `Delivery`, `Self-Pickup`, `Delivery and Self-Pickup`)
- **Provider-level fulfillment channels**
  - `catalog."bpp/providers"[].fulfillments[].id`
  - `catalog."bpp/providers"[].fulfillments[].type`
  - `catalog."bpp/providers"[].fulfillments[].contact.phone`
  - `catalog."bpp/providers"[].fulfillments[].contact.email`
- **Serviceability (where & for which categories the provider can fulfill)**
  - `catalog."bpp/providers"[].tags[]` with `code = "serviceability"`:
    - `list[].code = "location"`, `list[].value` (e.g., `L1`)
    - `list[].code = "category"`, `list[].value` (e.g., category name or code)
    - `list[].code = "type"`, `list[].value` (e.g., distance or serviceability type code)
    - `list[].code = "val"`, `list[].value` (e.g., numeric radius or country code)
    - `list[].code = "unit"`, `list[].value` (e.g., `km`, `country`)

These are **good candidates for a shared Fulfillment attributes pack** (per provider/channel), with domain-specific extensions if required.

#### Food & Beverage (`ondc_food_and_beverage.json`) – Fulfillment Attributes

- **Fulfillment types**
  - `catalog."bpp/fulfillments"[].id` and `.type` (Delivery, Self-Pickup, Delivery and Self-Pickup)
- **Provider fulfillment contacts**
  - `catalog."bpp/providers"[].fulfillments[].id`
  - `catalog."bpp/providers"[].fulfillments[].type`
  - `catalog."bpp/providers"[].fulfillments[].contact.phone`
  - `catalog."bpp/providers"[].fulfillments[].contact.email`
- **Timing policies per fulfillment/location**
  - `catalog."bpp/providers"[].tags[]` with `code = "timing"`:
    - `list[].code = "type"` → `value` (e.g., `Order`, `Delivery`, `Self-Pickup`)
    - `list[].code = "location"` → `value` (e.g., `L1`)
    - `list[].code = "day_from" | "day_to"` → `value` (operating days)
    - `list[].code = "time_from" | "time_to"` → `value` (operating hours)
- **Closure / downtime windows**
  - `catalog."bpp/providers"[].tags[]` with `code = "close_timing"`:
    - `list[].code = "location"` → `value`
    - `list[].code = "start"` → `value` (ISO timestamp)
    - `list[].code = "end"` → `value` (ISO timestamp)
- **Serviceability radius by category**
  - `catalog."bpp/providers"[].tags[]` with `code = "serviceability"` (see common section).

#### Grocery Catalog (`ondc_grocery_catalog.json`) – Fulfillment Attributes

- **Fulfillment types**
  - `catalog."bpp/fulfillments"[].id` and `.type`
- **Provider fulfillment contacts**
  - `catalog."bpp/providers"[].fulfillments[].contact.phone`
  - `catalog."bpp/providers"[].fulfillments[].contact.email`
- **Serviceability**
  - `catalog."bpp/providers"[].tags[]` with `code = "serviceability"` (category/location/type/val/unit as above).

_(This example does not add new fulfillment attributes beyond the common pattern.)_

#### Health & Wellness (`ondc_health_and_wellness.json`) – Fulfillment Attributes

- **Fulfillment types**
  - `catalog."bpp/fulfillments"[].id` and `.type`
- **Provider fulfillment contacts**
  - `catalog."bpp/providers"[].fulfillments[].id`
  - `catalog."bpp/providers"[].fulfillments[].type`
  - `catalog."bpp/providers"[].fulfillments[].contact.phone`
  - `catalog."bpp/providers"[].fulfillments[].contact.email`
- **Timing policies**
  - `catalog."bpp/providers"[].tags[]` with `code = "timing"`:
    - `list[].code = "type"` (Order / Delivery / Self-Pickup)
    - `list[].code = "location"`
    - `list[].code = "day_from" | "day_to"`
    - `list[].code = "time_from" | "time_to"`
- **Serviceability**
  - `catalog."bpp/providers"[].tags[]` with `code = "serviceability"` (F&B or other categories).

#### Home & Kitchen (`ondc_home_and_kitchen.json`) – Fulfillment Attributes

- **Fulfillment types**
  - `catalog."bpp/fulfillments"[].id` and `.type` (Delivery, Self-Pickup, Delivery and Self-Pickup)
- **Provider fulfillment contacts**
  - `catalog."bpp/providers"[].fulfillments[].id`
  - `catalog."bpp/providers"[].fulfillments[].type`
  - `catalog."bpp/providers"[].fulfillments[].contact.phone`
  - `catalog."bpp/providers"[].fulfillments[].contact.email`
- **Timing policies**
  - `catalog."bpp/providers"[].tags[]` with `code = "timing"`:
    - `list[].code = "type"` → `value` (Order / Delivery / Self-Pickup)
    - `list[].code = "location"` → `value` (e.g., "L1")
    - `list[].code = "day_from" | "day_to"` → `value` (1-7, where 1=Monday, 7=Sunday)
    - `list[].code = "time_from" | "time_to"` → `value` (HHMM format, e.g., "1100", "2200")
- **Serviceability**
  - `catalog."bpp/providers"[].tags[]` with `code = "serviceability"`:
    - `list[].code = "location"` → `value` (e.g., "L1")
    - `list[].code = "category"` → `value` (e.g., "Home Furnishings")
    - `list[].code = "type"` → `value` (e.g., "12" for country-wide)
    - `list[].code = "val"` → `value` (e.g., "IND" for country code)
    - `list[].code = "unit"` → `value` (e.g., "country")

Taken together, these give you a **fulfillment attribute surface** (types, contacts, timing, serviceability, closures) that can be modeled analogously to `EvChargingSession` but tailored for retail delivery/pickup flows.


