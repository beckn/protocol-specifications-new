# OCPI to OCPP Connector Type Mapping

This document provides a mapping between OCPI 2.2 `connector_standard` enum values and OCPP 2.0.1 `ConnectorEnumType` values.

## Overview

- **OCPI connector types**: 27 values
- **OCPP connector types**: 22 values
- **Mapped OCPI types**: 27 (100%)
- **Unmapped OCPP types**: 7 (these are OCPP-specific categories)

## OCPI → OCPP Mapping

### DC Fast Charging Connectors

| OCPI | OCPP | Notes |
|------|------|-------|
| `IEC_62196_T1_COMBO` | `cCCS1` | CCS1 (Combined Charging System Type 1) |
| `IEC_62196_T2_COMBO` | `cCCS2` | CCS2 (Combined Charging System Type 2) |
| `CHADEMO` | `cG105` | CHAdeMO (CHAdeMO Association standard) |
| `TESLA_S` | `cTesla` | Tesla Supercharger |
| `TESLA_R` | `cTesla` | Tesla Roadster (also maps to cTesla) |

### AC Connectors (IEC 62196)

| OCPI | OCPP | Notes |
|------|------|-------|
| `IEC_62196_T1` | `cType1` | Type 1 (J1772) - North America/Japan |
| `IEC_62196_T2` | `cType2` | Type 2 (Mennekes) - Europe |
| `IEC_62196_T3A` | `sType3` | Type 3A socket |
| `IEC_62196_T3C` | `sType3` | Type 3C socket |

### Industrial Connectors (IEC 60309)

| OCPI | OCPP | Notes |
|------|------|-------|
| `IEC_60309_2_single_16` | `s309-1P-16A` | Single phase 16A industrial connector |
| `IEC_60309_2_three_16` | `s309-3P-16A` | Three phase 16A industrial connector |
| `IEC_60309_2_three_32` | `s309-3P-32A` | Three phase 32A industrial connector |
| `IEC_60309_2_three_64` | `s309-3P-32A` | Three phase 64A (closest match is 32A) |

### Pantograph Connectors

| OCPI | OCPP | Notes |
|------|------|-------|
| `PANTOGRAPH_BOTTOM_UP` | `Pan` | Pantograph bottom-up (bus/truck charging) |
| `PANTOGRAPH_TOP_DOWN` | `Pan` | Pantograph top-down (bus/truck charging) |

### Domestic Plug Types

| OCPI | OCPP | Notes |
|------|------|-------|
| `DOMESTIC_A` | `Other1PhMax16A` | US Type A (2-pin) |
| `DOMESTIC_B` | `Other1PhOver16A` | US Type B (3-pin, grounded) |
| `DOMESTIC_C` | `sCEE-7-7` | Europlug (CEE 7/7) |
| `DOMESTIC_D` | `Other1PhMax16A` | Indian Type D (BS 546) |
| `DOMESTIC_E` | `sCEE-7-7` | French Type E (similar to Schuko) |
| `DOMESTIC_F` | `sCEE-7-7` | Schuko (CEE 7/7) - Germany/Austria |
| `DOMESTIC_G` | `sBS1361` | UK Type G (BS 1361) |
| `DOMESTIC_H` | `Other1PhMax16A` | Israeli Type H |
| `DOMESTIC_I` | `Other1PhMax16A` | Australian Type I |
| `DOMESTIC_J` | `Other1PhMax16A` | Swiss Type J |
| `DOMESTIC_K` | `Other1PhMax16A` | Danish Type K |
| `DOMESTIC_L` | `Other1PhMax16A` | Italian Type L |

## OCPP → OCPI Mapping (Reverse)

### Direct Mappings

| OCPP | OCPI | Notes |
|------|------|-------|
| `cCCS1` | `IEC_62196_T1_COMBO` | CCS1 |
| `cCCS2` | `IEC_62196_T2_COMBO` | CCS2 |
| `cType1` | `IEC_62196_T1` | Type 1 (J1772) |
| `cType2` | `IEC_62196_T2` | Type 2 (Mennekes) |
| `cG105` | `CHADEMO` | CHAdeMO |
| `cTesla` | `TESLA_S`, `TESLA_R` | Tesla connectors |
| `sType3` | `IEC_62196_T3A`, `IEC_62196_T3C` | Type 3 sockets |
| `s309-1P-16A` | `IEC_60309_2_single_16` | Single phase 16A |
| `s309-3P-16A` | `IEC_60309_2_three_16` | Three phase 16A |
| `s309-3P-32A` | `IEC_60309_2_three_32`, `IEC_60309_2_three_64` | Three phase 32A/64A |
| `sBS1361` | `DOMESTIC_G` | UK Type G |
| `sCEE-7-7` | `DOMESTIC_C`, `DOMESTIC_E`, `DOMESTIC_F` | European plugs |
| `Pan` | `PANTOGRAPH_BOTTOM_UP`, `PANTOGRAPH_TOP_DOWN` | Pantograph connectors |
| `Other1PhMax16A` | `DOMESTIC_A`, `DOMESTIC_D`, `DOMESTIC_H`, `DOMESTIC_I`, `DOMESTIC_J`, `DOMESTIC_K`, `DOMESTIC_L` | Various domestic plugs ≤16A |
| `Other1PhOver16A` | `DOMESTIC_B` | US Type B (>16A) |

### OCPP Types Without Direct OCPI Equivalents

These OCPP connector types don't have direct mappings in OCPI:

| OCPP | Description |
|------|-------------|
| `s309-1P-32A` | Single phase 32A IEC 60309 (OCPI only has 16A variant) |
| `sType2` | Type 2 socket (OCPI uses `IEC_62196_T2` for connector, not socket) |
| `Other3Ph` | Generic 3-phase connector (OCPI uses specific IEC 60309 types) |
| `wInductive` | Wireless inductive charging |
| `wResonant` | Wireless resonant charging |
| `Undetermined` | Connector type not determined |
| `Unknown` | Unknown connector type |

## Notes

1. **Many-to-One Mappings**: Some OCPP types map to multiple OCPI types (e.g., `cTesla` maps to both `TESLA_S` and `TESLA_R`).

2. **One-to-Many Mappings**: Some OCPI types map to the same OCPP type (e.g., multiple domestic plugs map to `Other1PhMax16A`).

3. **Wireless Charging**: OCPP includes wireless charging types (`wInductive`, `wResonant`) that OCPI doesn't currently support.

4. **Socket vs Connector**: OCPP distinguishes between connectors (`c*`) and sockets (`s*`), while OCPI uses a single `connector_standard` field.

5. **Generic Categories**: OCPP uses generic categories like `Other1PhMax16A` and `Other3Ph` for connectors that don't fit standard categories, while OCPI uses specific domestic plug types.

## Usage Recommendations

- When converting from OCPI to OCPP, use the direct mapping table above.
- When converting from OCPP to OCPI:
  - For specific types (cCCS1, cCCS2, etc.), use the direct mapping.
  - For generic types (Other1PhMax16A, etc.), you may need additional context to determine the exact OCPI type.
  - For OCPP-only types (wInductive, wResonant, etc.), consider using a fallback or leaving unmapped.

