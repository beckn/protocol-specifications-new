# P2P Energy Trade: v1 to v2 Migration Plan

## Executive Summary

This document provides a comprehensive step-by-step plan to migrate the Beckn v1 P2P Energy Trading implementation to v2 using composable schemas. The migration maintains all external interfaces and parameters while leveraging v2's modular architecture.

## Table of Contents

1. [Phase 1: Analysis & Mapping](#phase-1-analysis--mapping)
2. [Phase 2: Schema Updates & Enhancements](#phase-2-schema-updates--enhancements)
3. [Phase 3: Example Creation](#phase-3-example-creation)
4. [Phase 4: Implementation Guide](#phase-4-implementation-guide)
5. [Phase 5: Testing & Validation](#phase-5-testing--validation)
6. [Phase 6: Documentation & Deployment](#phase-6-documentation--deployment)

---

## Phase 1: Analysis & Mapping

### 1.1 Analyze v1 Layer2 Configuration

**Tasks:**
- [ ] Extract all v1 schema constraints from `trade_1.1.0.yaml`
- [ ] Document all required fields, enums, and validation rules
- [ ] Map v1 `allOf` constraints to v2 attribute schemas
- [ ] Identify v1-specific field formats (e.g., `der://` addresses)

**Deliverables:**
- `v1_constraints_analysis.md` - Complete mapping of v1 constraints
- `v1_to_v2_field_mapping.csv` - Field-by-field mapping table

**Key Areas to Analyze:**
1. **Context Constraints**: Location requirements, domain codes, action enums
2. **Intent Constraints**: Fulfillment stop requirements, meter address formats
3. **Order Constraints**: Payment types, settlement types, energy source types
4. **Fulfillment Constraints**: Stop types (START/END), address requirements
5. **Tag/Attribute Constraints**: Energy source types, settlement types, payment types

### 1.2 Map v1 Parameters to v2 Schemas

**Mapping Table:**

| v1 Location | v2 Location | Schema Bundle |
|-------------|------------|---------------|
| `Item.attributes.*` | `Item.itemAttributes.*` | `EnergyResource` |
| `Offer.attributes.*` | `Offer.offerAttributes.*` | `EnergyTradeOffer` |
| `Order.attributes.*` | `Order.orderAttributes.*` | `EnergyTradeContract` |
| `Fulfillment.attributes.*` | `Fulfillment.attributes.*` | `EnergyTradeDelivery` |
| `Fulfillment.stops[].location.address` | `Fulfillment.stops[].location.address` | Core + `EnergyResource.meterId` |
| `Tag.value` (energy source) | `EnergyResource.sourceType` | `EnergyResource` |
| `Tag.value` (settlement) | `EnergyTradeOffer.settlementType` | `EnergyTradeOffer` |

### 1.3 Identify Missing Attributes

**Review existing Energy* schemas and identify gaps:**

- [ ] Compare v1 layer2 constraints with existing `EnergyResource/v0.2/attributes.yaml`
- [ ] Compare v1 layer2 constraints with existing `EnergyTradeOffer/v0.2/attributes.yaml`
- [ ] Compare v1 layer2 constraints with existing `EnergyTradeContract/v0.2/attributes.yaml`
- [ ] Compare v1 layer2 constraints with existing `EnergyTradeDelivery/v0.2/attributes.yaml`
- [ ] Document any missing fields or constraints

**Potential Gaps to Check:**
- Provider-level attributes (if needed)
- Additional payment-related fields
- Settlement cycle details
- Meter reading formats
- Telemetry data structures

---

## Phase 2: Schema Updates & Enhancements

### 2.1 Update EnergyResource Schema

**File**: `schema/EnergyResource/v0.2/attributes.yaml`

**Tasks:**
- [ ] Verify `meterId` uses IEEE mRID format (already done ✓)
- [ ] Ensure all v1 energy source types are in enum: `[SOLAR, BATTERY, GRID, HYBRID, RENEWABLE]`
- [ ] Verify delivery modes match v1: `[EV_CHARGING, BATTERY_SWAP, V2G, GRID_INJECTION]`
- [ ] Add any missing fields from v1 layer2 constraints
- [ ] Update descriptions to reference v2 architecture

**Potential Additions:**
- Provider-level energy resource attributes (if needed)
- Additional certification fields
- Grid connection details

### 2.2 Update EnergyTradeOffer Schema

**File**: `schema/EnergyTradeOffer/v0.2/attributes.yaml`

**Tasks:**
- [ ] Verify settlement types match v1: `[REAL_TIME, HOURLY, DAILY, WEEKLY, MONTHLY]`
- [ ] Verify pricing models: `[PER_KWH, TIME_OF_DAY, SUBSCRIPTION, FIXED]`
- [ ] Ensure wheeling charges structure matches v1 requirements
- [ ] Add any missing offer-specific fields

**Potential Additions:**
- Minimum/maximum quantity constraints (already present ✓)
- Validity window details (already present ✓)
- Time-of-day rate structures (already present ✓)

### 2.3 Update EnergyTradeContract Schema

**File**: `schema/EnergyTradeContract/v0.2/attributes.yaml`

**Tasks:**
- [ ] Verify contract status enum: `[PENDING, ACTIVE, COMPLETED, TERMINATED]`
- [ ] Ensure `sourceMeterId` and `targetMeterId` use IEEE mRID (already done ✓)
- [ ] Verify settlement cycles structure matches v1 requirements
- [ ] Verify billing cycles structure matches v1 requirements
- [ ] Ensure wheeling charges breakdown matches v1

**Potential Additions:**
- Contract terms and conditions
- Dispute resolution fields
- Renewal/extension fields

### 2.4 Update EnergyTradeDelivery Schema

**File**: `schema/EnergyTradeDelivery/v0.2/attributes.yaml`

**Tasks:**
- [ ] Verify delivery status enum: `[PENDING, IN_PROGRESS, COMPLETED, FAILED]`
- [ ] Ensure delivery modes match: `[EV_CHARGING, BATTERY_SWAP, V2G, GRID_INJECTION]`
- [ ] Verify meter readings structure (currently uses `meterReadings` array)
- [ ] Ensure telemetry structure matches v1 requirements
- [ ] Verify settlement cycle linkage

**Potential Additions:**
- Delivery confirmation fields
- Quality metrics
- Failure reason codes

### 2.5 Create Profile.json (if missing)

**File**: `schema/EnergyResource/v0.2/profile.json` (or similar)

**Tasks:**
- [ ] Create profile.json following EvCharging pattern
- [ ] Define operational hints (index hints, PII hints)
- [ ] Configure API response field sets
- [ ] Define discovery filters and sorting

**Template Structure:**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.example.org/profiles/energy-trade/energy_trade/v0.2/profile.json",
  "title": "Energy Trade — Attribute Pack (v0.2)",
  "description": "Bundle of attribute schemas for P2P energy trading",
  "properties": {
    "EnergyResource": { "$ref": "./attributes.yaml#/components/schemas/EnergyResource" },
    "EnergyTradeOffer": { "$ref": "../EnergyTradeOffer/v0.2/attributes.yaml#/components/schemas/EnergyTradeOffer" },
    "EnergyTradeContract": { "$ref": "../EnergyTradeContract/v0.2/attributes.yaml#/components/schemas/EnergyTradeContract" },
    "EnergyTradeDelivery": { "$ref": "../EnergyTradeDelivery/v0.2/attributes.yaml#/components/schemas/EnergyTradeDelivery" }
  },
  "operational_hints": {
    "indexHints": [...],
    "piiHints": {...},
    "api_response_config": {...},
    "discover": {...}
  }
}
```

### 2.6 Update Context.jsonld Files

**Tasks:**
- [ ] Verify all context.jsonld files include IEEE namespace (already done ✓)
- [ ] Ensure all property mappings are correct
- [ ] Verify JSON-LD context URIs are absolute

---

## Phase 3: Example Creation

### 3.1 Create Examples Directory Structure

**Structure:**
```
schema/EnergyResource/v0.2/examples/
├── schema/
│   ├── item-example.json          # EnergyResource as Item.itemAttributes
│   ├── offer-example.json         # EnergyTradeOffer as Offer.offerAttributes
│   ├── order-example.json         # EnergyTradeContract as Order.orderAttributes
│   ├── fulfillment-example.json  # EnergyTradeDelivery as Fulfillment.attributes
│   └── provider-example.json     # Provider attributes (if needed)
└── flows/
    ├── discover-request.json      # /beckn/discover request
    ├── discover-response.json     # /beckn/on_discover response
    ├── select-request.json        # /beckn/select request
    ├── select-response.json       # /beckn/on_select response
    ├── init-request.json          # /beckn/init request
    ├── init-response.json        # /beckn/on_init response
    ├── confirm-request.json       # /beckn/confirm request
    ├── confirm-response.json     # /beckn/on_confirm response
    ├── status-request.json        # /beckn/status request
    └── status-response.json      # /beckn/on_status response
```

### 3.2 Create Item Example (EnergyResource)

**File**: `schema/EnergyResource/v0.2/examples/schema/item-example.json`

**Content Requirements:**
- [ ] Include all EnergyResource attributes
- [ ] Use IEEE mRID format for `meterId`
- [ ] Include production window
- [ ] Include source verification
- [ ] Match v1 layer2 constraints

**Example Structure:**
```json
{
  "sourceType": "SOLAR",
  "deliveryMode": "GRID_INJECTION",
  "certificationStatus": "Carbon Offset Certified",
  "meterId": "100200300",
  "inverterId": "inv-12345",
  "availableQuantity": 30.5,
  "productionWindow": {
    "start": "2024-10-04T10:00:00Z",
    "end": "2024-10-04T18:00:00Z"
  },
  "sourceVerification": {
    "verified": true,
    "verificationDate": "2024-09-01T00:00:00Z",
    "certificates": ["https://example.com/certs/solar-panel-cert.pdf"]
  },
  "productionAsynchronous": true
}
```

### 3.3 Create Offer Example (EnergyTradeOffer)

**File**: `schema/EnergyTradeOffer/v0.2/examples/schema/offer-example.json`

**Content Requirements:**
- [ ] Include pricing model
- [ ] Include settlement type
- [ ] Include wheeling charges
- [ ] Include time-of-day rates (if applicable)
- [ ] Include validity window

### 3.4 Create Order Example (EnergyTradeContract)

**File**: `schema/EnergyTradeContract/v0.2/examples/schema/order-example.json`

**Content Requirements:**
- [ ] Include contract status
- [ ] Include source and target meter IDs (IEEE mRID)
- [ ] Include settlement cycles
- [ ] Include billing cycles
- [ ] Include wheeling charges breakdown

### 3.5 Create Fulfillment Example (EnergyTradeDelivery)

**File**: `schema/EnergyTradeDelivery/v0.2/examples/schema/fulfillment-example.json`

**Content Requirements:**
- [ ] Include delivery status
- [ ] Include meter readings array
- [ ] Include telemetry data
- [ ] Include settlement cycle linkage

### 3.6 Create Transaction Flow Examples

**For each flow, create request and response examples:**

#### 3.6.1 Discover Flow

**Files:**
- `schema/EnergyResource/v0.2/examples/flows/discover-request.json`
- `schema/EnergyResource/v0.2/examples/flows/discover-response.json`

**Requirements:**
- [ ] Show search by energy source type
- [ ] Show search by delivery mode
- [ ] Show search by location (meter-based)
- [ ] Show search by availability window
- [ ] Include full catalog response with EnergyResource attributes

#### 3.6.2 Select Flow

**Files:**
- `schema/EnergyResource/v0.2/examples/flows/select-request.json`
- `schema/EnergyResource/v0.2/examples/flows/select-response.json`

**Requirements:**
- [ ] Show item selection
- [ ] Show offer selection
- [ ] Include EnergyTradeOffer attributes in response
- [ ] Show priced order structure

#### 3.6.3 Init Flow

**Files:**
- `schema/EnergyResource/v0.2/examples/flows/init-request.json`
- `schema/EnergyResource/v0.2/examples/flows/init-response.json`

**Requirements:**
- [ ] Show fulfillment stops (START and END)
- [ ] Show meter addresses in stops
- [ ] Show payment details
- [ ] Include EnergyTradeContract attributes in response
- [ ] Show settlement cycle initialization

#### 3.6.4 Confirm Flow

**Files:**
- `schema/EnergyResource/v0.2/examples/flows/confirm-request.json`
- `schema/EnergyResource/v0.2/examples/flows/confirm-response.json`

**Requirements:**
- [ ] Show final order confirmation
- [ ] Show contract activation
- [ ] Include full EnergyTradeContract attributes
- [ ] Show payment confirmation

#### 3.6.5 Status Flow

**Files:**
- `schema/EnergyResource/v0.2/examples/flows/status-request.json`
- `schema/EnergyResource/v0.2/examples/flows/status-response.json`

**Requirements:**
- [ ] Show order status query
- [ ] Show fulfillment status with EnergyTradeDelivery attributes
- [ ] Show meter readings updates
- [ ] Show telemetry data
- [ ] Show settlement cycle status

---

## Phase 4: Implementation Guide

### 4.1 Create Implementation Guide Document

**File**: `schema/EnergyResource/v0.2/IMPLEMENTATION_GUIDE.md`

**Sections:**

1. **Introduction**
   - Overview of P2P Energy Trading on Beckn v2
   - Architecture differences from v1
   - Key concepts: composable schemas, attribute bundles

2. **Schema Overview**
   - EnergyResource (Item.itemAttributes)
   - EnergyTradeOffer (Offer.offerAttributes)
   - EnergyTradeContract (Order.orderAttributes)
   - EnergyTradeDelivery (Fulfillment.attributes)

3. **Transaction Flows**
   - Discover flow with examples
   - Select flow with examples
   - Init flow with examples
   - Confirm flow with examples
   - Status flow with examples

4. **Field Mapping Reference**
   - v1 to v2 field mapping table
   - Parameter mapping guide
   - Format changes (e.g., `der://` to IEEE mRID)

5. **Integration Patterns**
   - How to attach attributes to core objects
   - JSON-LD context usage
   - Validation requirements

6. **Best Practices**
   - Discovery optimization
   - Settlement cycle management
   - Meter reading handling
   - Error handling

7. **Migration Checklist**
   - Step-by-step migration guide
   - Testing checklist
   - Rollback procedures

### 4.2 Create Taxonomy Reference

**File**: `schema/EnergyResource/v0.2/TAXONOMY.md`

**Content:**
- [ ] Energy source types enum
- [ ] Delivery modes enum
- [ ] Settlement types enum
- [ ] Pricing models enum
- [ ] Contract status enum
- [ ] Delivery status enum
- [ ] Payment types enum
- [ ] Telemetry metric names enum

### 4.3 Create API Reference

**File**: `schema/EnergyResource/v0.2/API_REFERENCE.md`

**Content:**
- [ ] Endpoint specifications
- [ ] Request/response schemas
- [ ] Error codes
- [ ] Rate limiting
- [ ] Authentication

---

## Phase 5: Testing & Validation

### 5.1 Schema Validation

**Tasks:**
- [ ] Validate all attribute schemas against OpenAPI 3.1.1
- [ ] Validate JSON-LD contexts
- [ ] Validate SHACL shapes (if applicable)
- [ ] Cross-reference with core v2 schemas

**Tools:**
- OpenAPI validator
- JSON-LD playground
- SHACL validator

### 5.2 Example Validation

**Tasks:**
- [ ] Validate all examples against their schemas
- [ ] Validate JSON-LD contexts in examples
- [ ] Ensure examples match v1 layer2 constraints
- [ ] Test example parsing in common libraries

### 5.3 Flow Validation

**Tasks:**
- [ ] Validate complete transaction flows
- [ ] Test discover → select → init → confirm → status flow
- [ ] Verify all required fields are present
- [ ] Test error scenarios

### 5.4 Compatibility Testing

**Tasks:**
- [ ] Compare v1 and v2 payloads side-by-side
- [ ] Verify all v1 parameters are mapped
- [ ] Test backward compatibility (if needed)
- [ ] Document breaking changes (if any)

---

## Phase 6: Documentation & Deployment

### 6.1 Update README Files

**Files to Update:**
- [ ] `schema/EnergyResource/v0.2/README.md`
- [ ] `schema/EnergyTradeOffer/v0.2/README.md`
- [ ] `schema/EnergyTradeContract/v0.2/README.md`
- [ ] `schema/EnergyTradeDelivery/v0.2/README.md`

**Content:**
- [ ] Add v2 migration notes
- [ ] Update examples references
- [ ] Add implementation guide links
- [ ] Update use case descriptions

### 6.2 Create Migration Guide

**File**: `schema/ENERGY_V1_TO_V2_MIGRATION_GUIDE.md`

**Content:**
- [ ] Executive summary
- [ ] Key differences between v1 and v2
- [ ] Step-by-step migration instructions
- [ ] Code examples
- [ ] Common pitfalls
- [ ] FAQ

### 6.3 Create Changelog

**File**: `schema/ENERGY_V2_CHANGELOG.md`

**Content:**
- [ ] List of all changes from v1
- [ ] Breaking changes (if any)
- [ ] New features
- [ ] Deprecated fields
- [ ] Migration notes

### 6.4 Final Review

**Tasks:**
- [ ] Review all documentation
- [ ] Verify all examples work
- [ ] Check all links
- [ ] Ensure consistency across documents
- [ ] Get peer review

---

## Implementation Timeline

### Week 1: Analysis & Planning
- Phase 1: Complete analysis and mapping
- Review existing schemas
- Document gaps

### Week 2: Schema Updates
- Phase 2: Update all schemas
- Create profile.json
- Update context files

### Week 3: Examples & Flows
- Phase 3: Create all examples
- Create transaction flow examples
- Validate examples

### Week 4: Documentation
- Phase 4: Create implementation guide
- Create taxonomy reference
- Create API reference

### Week 5: Testing & Validation
- Phase 5: Complete all validation
- Test all flows
- Compatibility testing

### Week 6: Final Documentation
- Phase 6: Update all READMEs
- Create migration guide
- Final review

---

## Success Criteria

- [ ] All v1 parameters mapped to v2 schemas
- [ ] All transaction flows have complete examples
- [ ] Implementation guide covers all use cases
- [ ] All schemas validated
- [ ] All examples validated
- [ ] Documentation complete and reviewed
- [ ] Migration guide available
- [ ] Backward compatibility verified (if applicable)

---

## Notes

1. **IEEE mRID Format**: Already migrated from `der://` format to IEEE 2030.5 mRID format ✓
2. **Schema Structure**: Energy* schemas already follow v2 composable pattern ✓
3. **JSON-LD Context**: All context files include IEEE namespace ✓
4. **Examples Pattern**: Follow EvCharging examples structure

---

## Next Steps

1. Review this plan with stakeholders
2. Assign tasks to team members
3. Set up project tracking
4. Begin Phase 1: Analysis & Mapping

