# EV Charging API Call Examples

<style>
  table { width: 100%; border-collapse: collapse; }
  table th:nth-child(1), table td:nth-child(1) { width: 80%; }
  table th:nth-child(2), table td:nth-child(2) { width: 20%; }
</style>

This directory contains JSON examples of API calls for the EV Charging schema (v1). Examples are grouped by endpoint.

## discover
In these examples, we show how to request discovery of EV charging services under various scenarios.

| Use Case | link to example JSON |
|---|---|
| Request to discover EV charging services within a defined circular area | [EV-charging-services-within-a-circular-boundary.json](1_discover/EV-charging-services-within-a-circular-boundary.json) |
| Request to discover EV charging services within a defined circular area applying connector type filters | [EV-charging-services-within-circle-with-connector-filters.json](1_discover/EV-charging-services-within-circle-with-connector-filters.json) |
| Request to discover EV charging services within a defined circular area applying vehicle specification filters | [EV-charging-services-within-circle-with-vehicle-spec-filters.json](1_discover/EV-charging-services-within-circle-with-vehicle-spec-filters.json) |
| Request to discover EV charging services located along a specified route | [EV-charging-services-along-a-route.json](1_discover/EV-charging-services-along-a-route.json) |
| Request to discover EV charging services provided by a specific charging point operator | [EV-charging-services-by-specific-cpo.json](1_discover/EV-charging-services-by-specific-cpo.json) |
| Request to retrieve details of a specific EVSE by its EVSE identifier | [Fetch-specific-EVSE-on-site-by-EVSE-id.json](1_discover/Fetch-specific-EVSE-on-site-by-EVSE-id.json) |
| Request to retrieve details of a single charging station by its item identifier | [View-single-charging-services-station-by-Item-id.json](1_discover/View-single-charging-services-station-by-Item-id.json) |

## on_discover
In these examples, we show how the CPO responds with a catalog of available EV charging services after discovery.

| Use Case | link to example JSON |
|---|---|
| CPO response containing a catalog of EV charging services following a discover request | [CPO-sends-EV-Charging-Service-Catalog.json](2_on_discover/CPO-sends-EV-Charging-Service-Catalog.json) |

## select
In these examples, we show how an EV user selects a charging service for a specified amount or value.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user selects a charging session for a specific energy amount in kWh | [EV-user-requests-charge-for-specific-amount-in-kWh.json](3_select/EV-user-requests-charge-for-specific-amount-in-kWh.json) |
| Request where an EV user selects a charging session worth a specific monetary amount | [EV-user-requests-charge-worth-specific-amount-in-currency.json](3_select/EV-user-requests-charge-worth-specific-amount-in-currency.json) |

## on_select
In these examples, we show how the CPO responds to a selection request.

| Use Case | link to example JSON |
|---|---|
| CPO responds with dynamically calculated quote | [CPO-responds-with-dynamic-quote.json](4_on_select/CPO-responds-with-dynamic-quote.json) |
| CPO responds with confirmed slot reservation | [CPO-responds-with-confirmed-slot.json](4_on_select/CPO-responds-with-confirmed-slot.json) |

## init
In these examples, we show how an EV user requests the final quote for the charging session.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user asks for the final quote for charging session including billing details | [EV-user-requests-final-quote-with-billing.json](5_init/EV-user-requests-final-quote-with-billing.json) |

## on_init
In these examples, we show how the CPO provides the final quote including payment terms.

| Use Case | link to example JSON |
|---|---|
| CPO response containing the final charging quote along with payment terms | [CPO-sends-final-quote-with-payment-terms.json](6_on_init/CPO-sends-final-quote-with-payment-terms.json) |

## confirm
In these examples, we show how an EV user confirms the order by initiating the charging session.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user confirms reservation of a slot at a particular time | [EV-user-confirms-slot-reservation.json](7_confirm/EV-user-confirms-slot-reservation.json) |
| Request where an EV user confirms order by starting charging session | [EV-user-confirms-order-by-starting-charging-session.json](7_confirm/EV-user-confirms-order-by-starting-charging-session.json) |

## on_confirm
In these examples, we show how the CPO confirms the order by starting the charging session.

| Use Case | link to example JSON |
|---|---|
| CPO response confirming the order by initiating the charging session | [CPO-confirms-order-by-starting-charging-session.json](8_on_confirm/CPO-confirms-order-by-starting-charging-session.json) |

## status
In these examples, we show how an EV user requests the status of the charging session.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user checks the status of an ongoing or completed charging session | [EV-user-requests-status-of-charging-session.json](9_status/EV-user-requests-status-of-charging-session.json) |

## on_status
In these examples, we show how the CPO responds with the current status of the charging session.

| Use Case | link to example JSON |
|---|---|
| CPO response indicating the charging session is currently active | [on_status-active.json](10_on_status/on_status-active.json) |
| CPO response indicating the charging session has been completed | [on_status-completed.json](10_on_status/on_status-completed.json) |

## update
In these examples, we show how an EV user manages a live charging session.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user starts a charging session | [EV-user-starts-charging-session.json](11_update/EV-user-starts-charging-session.json) |
| Request where an EV user stops a charging session | [EV-user-stops-charging-session.json](11_update/EV-user-stops-charging-session.json) |

## on_update
In these examples, we show how the CPO responds to live session management.

| Use Case | link to example JSON |
|---|---|
| CPO response when starting a charging session | [CPO-starts-charging-session.json](12_on_update/CPO-starts-charging-session.json) |
| CPO response when stopping the charging session | [CPO-stops-charging-session.json](12_on_update/CPO-stops-charging-session.json) |

## cancel
In these examples, we show how an EV user cancels reservations or sessions.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user cancels a charging session | [EV-user-cancels-charging-session.json](13_cancel/EV-user-cancels-charging-session.json) |
| Request where an EV user cancels a charging slot reservation | [EV-user-cancels-charging-slot-reservation.json](13_cancel/EV-user-cancels-charging-slot-reservation.json) |

## on_cancel
In these examples, we show how the CPO responds to cancellation requests.

| Use Case | link to example JSON |
|---|---|
| CPO response cancelling a charging session reservation | [CPO-cancels-charging-session-reservation.json](14_on_cancel/CPO-cancels-charging-session-reservation.json) |

## track
In these examples, we show how an EV user tracks a live charging session in real-time.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user tracks a live charging session | [EV-user-tracks-charging-session.json](15_track/EV-user-tracks-charging-session.json) |

## on_track
In these examples, we show how the CPO returns live charging tracking info.

| Use Case | link to example JSON |
|---|---|
| CPO returns live charging tracking info | [CPO-returns-live-charging-tracking-info.json](16_on_track/CPO-returns-live-charging-tracking-info.json) |

## rating
In these examples, we show how an EV user provides feedback after fulfillment.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user rates charging service experience | [EV-user-rates-charging-experience.json](17_rating/EV-user-rates-charging-experience.json) |

## on_rating
In these examples, we show how the CPO responds to rating submissions.

| Use Case | link to example JSON |
|---|---|
| CPO response accepting rating | [CPO-accepts-rating.json](18_on_rating/CPO-accepts-rating.json) |
| CPO response requesting feedback after rating | [CPO-requests-feedback.json](18_on_rating/CPO-requests-feedback.json) |

## support
In these examples, we show how an EV user reaches out for assistance.

| Use Case | link to example JSON |
|---|---|
| Request where an EV user contacts support | [EV-user-contacts-support.json](19_support/EV-user-contacts-support.json) |

## on_support
In these examples, we show how the CPO provides support information.

| Use Case | link to example JSON |
|---|---|
| CPO response returning support information | [CPO-returns-support-information.json](20_on_support/CPO-returns-support-information.json) |
