# OCPI to OCPP Connector Type Mapping

This document provides a mapping between **OCPI 2.2** `connector_standard` enum values and **OCPP 2.1.0** `ConnectorEnumType` values.

## Overview

- **OCPI 2.2 connector types**: 38 values
- **OCPP 2.1.0 connector types**: 31 values
- **Mapped OCPI types**: 38 (100%)
- **Unmapped OCPP types**: 9 (these are OCPP-specific categories or new in 2.1.0)

## OCPI → OCPP Mapping

### DC Fast Charging Connectors

| OCPI 2.2 | OCPP 2.1.0 | Notes |
|----------|------------|-------|
| `IEC_62196_T1_COMBO` | `cCCS1` | CCS1 (Combined Charging System Type 1) |
| `IEC_62196_T2_COMBO` | `cCCS2` | CCS2 (Combined Charging System Type 2) |
| `CHADEMO` | `cG105` | CHAdeMO (CHAdeMO Association standard) |
| `CHAOJI` | `cChaoJi` | ChaoJi connector (CHAdeMO 3.0) - **New in OCPP 2.1.0** |
| `GBT_DC` | `cGBT-DC` | GB/T DC connector - **New in OCPP 2.1.0** |
| `TESLA_S` | `cTesla` | Tesla Supercharger |
| `TESLA_R` | `cTesla` | Tesla Roadster (also maps to cTesla) |
| - | `cLECCS` | Light Equipment Combined Charging System - **OCPP 2.1.0 only** |
| - | `cMCS` | Megawatt Charging System - **OCPP 2.1.0 only** |
| - | `cNACS` | North American Charging Standard J3400 - **OCPP 2.1.0 only** |
| - | `cNACS-CCS1` | Tesla MagicDock with built-in NACS to CCS1 adapter - **OCPP 2.1.0 only** |
| - | `cCCS1-NACS` | Omni Port with built-in CCS1 to NACS adapter - **OCPP 2.1.0 only** |
| - | `cUltraChaoJi` | Ultra-ChaoJi for megawatt charging - **OCPP 2.1.0 only** |

### AC Connectors (IEC 62196)

| OCPI 2.2 | OCPP 2.1.0 | Notes |
|----------|------------|-------|
| `IEC_62196_T1` | `cType1` | Type 1 (J1772) - North America/Japan |
| `IEC_62196_T1` | `sType1` | Type 1 socket - **New in OCPP 2.1.0** |
| `IEC_62196_T2` | `cType2` | Type 2 (Mennekes) - Europe |
| `IEC_62196_T2` | `sType2` | Type 2 socket |
| `IEC_62196_T3A` | `sType3` | Type 3A socket |
| `IEC_62196_T3C` | `sType3` | Type 3C socket |

### Industrial Connectors (IEC 60309)

| OCPI 2.2 | OCPP 2.1.0 | Notes |
|----------|------------|-------|
| `IEC_60309_2_single_16` | `s309-1P-16A` | Single phase 16A industrial connector |
| - | `s309-1P-32A` | Single phase 32A industrial connector - **OCPP only** |
| `IEC_60309_2_three_16` | `s309-3P-16A` | Three phase 16A industrial connector |
| `IEC_60309_2_three_32` | `s309-3P-32A` | Three phase 32A industrial connector |
| `IEC_60309_2_three_64` | `s309-3P-32A` | Three phase 64A (closest match is 32A) |

### Pantograph Connectors

| OCPI 2.2 | OCPP 2.1.0 | Notes |
|----------|------------|-------|
| `PANTOGRAPH_BOTTOM_UP` | `Pan` | Pantograph bottom-up (bus/truck charging) |
| `PANTOGRAPH_TOP_DOWN` | `Pan` | Pantograph top-down (bus/truck charging) |

### Domestic Plug Types

| OCPI 2.2 | OCPP 2.1.0 | Notes |
|----------|------------|-------|
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

### GB/T Connectors (Chinese Standard)

| OCPI 2.2 | OCPP 2.1.0 | Notes |
|----------|------------|-------|
| `GBT_AC` | - | GB/T AC connector (not in OCPP 2.1.0) |
| `GBT_DC` | `cGBT-DC` | GB/T DC connector - **New in OCPP 2.1.0** |

### NEMA Connectors (North America)

| OCPI 2.2 | OCPP 2.1.0 | Notes |
|----------|------------|-------|
| `NEMA_5_20` | `Other1PhMax16A` | NEMA 5-20 (closest match) |
| `NEMA_6_30` | `Other1PhOver16A` | NEMA 6-30 (closest match) |
| `NEMA_6_50` | `Other1PhOver16A` | NEMA 6-50 (closest match) |
| `NEMA_10_30` | `Other3Ph` | NEMA 10-30 (closest match) |
| `NEMA_10_50` | `Other3Ph` | NEMA 10-50 (closest match) |
| `NEMA_14_30` | `Other3Ph` | NEMA 14-30 (closest match) |
| `NEMA_14_50` | `Other3Ph` | NEMA 14-50 (closest match) |

## OCPP 2.1.0 → OCPI 2.2 Mapping (Reverse)

### Direct Mappings

| OCPP 2.1.0 | OCPI 2.2 | Notes |
|------------|----------|-------|
| `cCCS1` | `IEC_62196_T1_COMBO` | CCS1 |
| `cCCS2` | `IEC_62196_T2_COMBO` | CCS2 |
| `cChaoJi` | `CHAOJI` | ChaoJi connector - **New in OCPP 2.1.0** |
| `cGBT-DC` | `GBT_DC` | GB/T DC connector - **New in OCPP 2.1.0** |
| `cType1` | `IEC_62196_T1` | Type 1 (J1772) |
| `sType1` | `IEC_62196_T1` | Type 1 socket - **New in OCPP 2.1.0** |
| `cType2` | `IEC_62196_T2` | Type 2 (Mennekes) |
| `sType2` | `IEC_62196_T2` | Type 2 socket |
| `cG105` | `CHADEMO` | CHAdeMO |
| `cTesla` | `TESLA_S`, `TESLA_R` | Tesla connectors |
| `sType3` | `IEC_62196_T3A`, `IEC_62196_T3C` | Type 3 sockets |
| `s309-1P-16A` | `IEC_60309_2_single_16` | Single phase 16A |
| `s309-3P-16A` | `IEC_60309_2_three_16` | Three phase 16A |
| `s309-3P-32A` | `IEC_60309_2_three_32`, `IEC_60309_2_three_64` | Three phase 32A/64A |
| `sBS1361` | `DOMESTIC_G` | UK Type G |
| `sCEE-7-7` | `DOMESTIC_C`, `DOMESTIC_E`, `DOMESTIC_F` | European plugs |
| `Pan` | `PANTOGRAPH_BOTTOM_UP`, `PANTOGRAPH_TOP_DOWN` | Pantograph connectors |
| `Other1PhMax16A` | `DOMESTIC_A`, `DOMESTIC_D`, `DOMESTIC_H`, `DOMESTIC_I`, `DOMESTIC_J`, `DOMESTIC_K`, `DOMESTIC_L`, `NEMA_5_20` | Various domestic plugs ≤16A |
| `Other1PhOver16A` | `DOMESTIC_B`, `NEMA_6_30`, `NEMA_6_50` | Single phase >16A |
| `Other3Ph` | `NEMA_10_30`, `NEMA_10_50`, `NEMA_14_30`, `NEMA_14_50` | Three phase sockets |

### OCPP 2.1.0 Types Without Direct OCPI 2.2 Equivalents

These OCPP 2.1.0 connector types don't have direct mappings in OCPI 2.2:

| OCPP 2.1.0 | Description |
|------------|-------------|
| `s309-1P-32A` | Single phase 32A IEC 60309 (OCPI only has 16A variant) |
| `cLECCS` | Light Equipment Combined Charging System IS17017 - **New in OCPP 2.1.0** |
| `cMCS` | Megawatt Charging System - **New in OCPP 2.1.0** |
| `cNACS` | North American Charging Standard J3400 - **New in OCPP 2.1.0** |
| `cNACS-CCS1` | Tesla MagicDock with built-in NACS to CCS1 adapter - **New in OCPP 2.1.0** |
| `cCCS1-NACS` | Omni Port with built-in CCS1 to NACS adapter - **New in OCPP 2.1.0** |
| `cUltraChaoJi` | Ultra-ChaoJi for megawatt charging - **New in OCPP 2.1.0** |
| `wInductive` | Wireless inductive charging |
| `wResonant` | Wireless resonant charging |
| `Undetermined` | Connector type not determined |
| `Unknown` | Unknown connector type |

## Notes

1. **Version Information**: 
   - **OCPI 2.2**: 38 connector types
   - **OCPP 2.1.0**: 31 connector types (up from 22 in OCPP 2.0.1)

2. **Many-to-One Mappings**: Some OCPP types map to multiple OCPI types (e.g., `cTesla` maps to both `TESLA_S` and `TESLA_R`).

3. **One-to-Many Mappings**: Some OCPI types map to the same OCPP type (e.g., multiple domestic plugs map to `Other1PhMax16A`).

4. **New in OCPP 2.1.0**: 
   - `cChaoJi` - Maps to OCPI `CHAOJI`
   - `cGBT-DC` - Maps to OCPI `GBT_DC`
   - `cLECCS`, `cMCS`, `cNACS`, `cNACS-CCS1`, `cCCS1-NACS`, `cUltraChaoJi` - OCPP 2.1.0 only
   - `sType1` - Type 1 socket (new in 2.1.0)

5. **Wireless Charging**: OCPP includes wireless charging types (`wInductive`, `wResonant`) that OCPI doesn't currently support.

6. **Socket vs Connector**: OCPP distinguishes between connectors (`c*`) and sockets (`s*`), while OCPI uses a single `connector_standard` field.

7. **Generic Categories**: OCPP uses generic categories like `Other1PhMax16A` and `Other3Ph` for connectors that don't fit standard categories, while OCPI uses specific domestic plug types.

8. **GB/T Support**: OCPP 2.1.0 adds `cGBT-DC` for GB/T DC connectors, matching OCPI's `GBT_DC`. OCPI also has `GBT_AC` which has no direct OCPP equivalent.

## Usage Recommendations

- When converting from **OCPI 2.2** to **OCPP 2.1.0**, use the direct mapping table above.
- When converting from **OCPP 2.1.0** to **OCPI 2.2**:
  - For specific types (cCCS1, cCCS2, cChaoJi, cGBT-DC, etc.), use the direct mapping.
  - For generic types (Other1PhMax16A, etc.), you may need additional context to determine the exact OCPI type.
  - For OCPP 2.1.0-only types (cLECCS, cMCS, cNACS, cUltraChaoJi, wInductive, wResonant, etc.), consider using a fallback or leaving unmapped.
  - For new OCPP 2.1.0 types that have OCPI equivalents (cChaoJi → CHAOJI, cGBT-DC → GBT_DC), use the direct mapping.

## Version History

- **OCPP 2.0.1**: 22 connector types
- **OCPP 2.1.0**: 31 connector types (+9 new types)
- **OCPI 2.2**: 38 connector types

