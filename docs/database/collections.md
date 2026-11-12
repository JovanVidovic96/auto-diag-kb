# Collections

`lang` in the Type column means a language object `{"en": "...", "sr": "..."}` with `en` required. Every document also has `_key`, `created_at` and `updated_at`, which are not repeated below.

## Catalog

### manufacturers

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | "Volkswagen" |
| `country` | string | ISO 3166 alpha-2, "DE" |
| `founded` | int | optional |

Key example: `volkswagen`.

### models

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | "Golf" |
| `generation` | string | "Mk7" |
| `year_from`, `year_to` | int | `year_to` null if still produced |
| `body_type` | string | hatchback, sedan, wagon, suv, van |

Key example: `vw-golf-7`.

### engines

| Field | Type | Notes |
| --- | --- | --- |
| `code` | string | manufacturer engine code, "CRBC" |
| `family` | string | "EA288" |
| `fuel` | string | petrol, diesel, lpg, hybrid |
| `displacement_cc` | int | |
| `power_kw` | int | |
| `aspiration` | string | na, turbo |

Key example: `vw-ea288-2-0-tdi-110kw`. Engines shared across brands are one document, which is what lets queries show reuse across the VW group.

### components

| Field | Type | Notes |
| --- | --- | --- |
| `name` | lang | |
| `system` | string | ignition, fuel, air-intake, exhaust, egr, cooling, sensors, emissions, evap |

Key example: `ignition-coil`.

## Knowledge base

### dtc_codes

| Field | Type | Notes |
| --- | --- | --- |
| `code` | string | `^[PBCU][0-3][0-9A-F]{3}$`, same as `_key` |
| `description` | lang | |
| `category` | string | P, B, C, U (first letter) |
| `system` | string | same values as `components.system` |
| `severity` | int | 1 (info) to 5 (stop driving) |
| `generic` | bool | true for SAE generic codes (P0xxx) |

```json
{
  "_key": "P0300",
  "code": "P0300",
  "description": {
    "en": "Random/multiple cylinder misfire detected",
    "sr": "Detektovano nasumično/višestruko preskakanje paljenja"
  },
  "category": "P",
  "system": "ignition",
  "severity": 4,
  "generic": true
}
```

### symptoms

| Field | Type | Notes |
| --- | --- | --- |
| `name` | lang | "Rough idle" / "Neravnomeran rad na leru" |
| `description` | lang | optional |

### causes

| Field | Type | Notes |
| --- | --- | --- |
| `title` | lang | |
| `description` | lang | optional |

### solutions

| Field | Type | Notes |
| --- | --- | --- |
| `title` | lang | |
| `steps` | list of lang | ordered repair steps |
| `difficulty` | string | easy, medium, hard |
| `cost_rsd` | object | `{"min": 3000, "max": 12000}` |
| `time_h` | float | typical labor time |

## Service history

### users

| Field | Type | Notes |
| --- | --- | --- |
| `username` | string | unique, 3 to 32 chars |
| `email` | string | unique |
| `password_hash` | string | bcrypt, never returned by the API |
| `role` | string | owner, mechanic, admin |
| `full_name` | string | |
| `is_active` | bool | false means deactivated (soft delete) |

### vehicles

| Field | Type | Notes |
| --- | --- | --- |
| `vin` | string | 17 characters, same as `_key` |
| `registration` | string | license plate, optional, unique |
| `year` | int | model year |
| `mileage_km` | int | updated from the latest service record |
| `color` | string | optional |

### service_records

| Field | Type | Notes |
| --- | --- | --- |
| `date` | string | ISO date, "2025-03-14" |
| `mileage_km` | int | not lower than the vehicle's previous record |
| `labor_rsd` | float | |
| `parts_rsd` | float | sum of `replaced` edges, computed by the service layer |
| `total_rsd` | float | `labor_rsd + parts_rsd` |
| `notes` | string | optional |

Codes read and parts replaced are the `found_code` and `replaced` edges.

### workshops

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | |
| `city` | string | |
| `address` | string | |
| `location` | [lat, lon] | used by the geo index |

## Validation

Pydantic models in `app/models/` enforce:

- DTC code format `^[PBCU][0-3][0-9A-F]{3}$`
- severity 1 to 5; `weight` and `probability` 0 to 1; `priority` 1 or more
- VIN exactly 17 characters without I, O and Q
- `mileage_km`, money and quantities 0 or more
- `role` one of owner, mechanic, admin
- language objects must contain `en`
