# Beckn Network Observability - Requirements

## 1. Executive Summary

This document outlines specification for Network Participants for sending Network logs to a centralized Observability system. This specification details out the follwing-
- New Network Participating entity type, called Observer, that implements an API to receive logs from other Network Participants.
- Exporter requirements to be implemented by BAP/BPP entities including Data points to be sent, filtering & masking of sensitive fields, Cadence of sending logs.


## 2. Functional Requirements

### 2.1 Support for pushing payload to Two observability systems

- Exporter can send logs to two independent Receiver APIs, i.e. two Network Observers. One could be the Observer operated by the Network Operator for Governance and another could be any additional Observer that may offer comprehensive Network aware Analytics capability.
- If Observability is enabled by the BAP or BPP NPs, then sharing with 1 or 2 Observers is configurable.
- Support separate Configuration for each Observer.
- Initialization: Upon startup, the observability module iterates through the list of configured observers. It instantiates a separate "Exporter" for each entry.
- Execution: When a Beckn request is processed, the observability exporter "fans out" the data. It pushes the same (or filtered) log to all active observers concurrently.
- Failure Handling: The spec should define that a failure to push to one Observer should not interrupt the flow to another Observer, ensuring that separate configurations provide operational redundancy.

### 2.2 Network Log Payload Structure

**Network Core Fields (Required for all logs):**

- `Context`: Beckn Context object

**Network Business Fields (Network-specific):**

Networks can define a list of Network fields they need to capture, a sample list could look like below-
- `message`: Beckn Message object (for search/select)
- `error`: Beckn Error object

**Operational Fields:**
- `latency_ms`: Processing latency in milliseconds
- `http_status_code`: HTTP response code (if applicable)
- `http_error_message`: HTTP error message

**Metadata:**
- `app_version`: Beckn-ONIX adapter version
- `environment`: Deployment environment (dev, staging, production)
- `subscriber_type`: BAP or BPP

### 2.3 PII Masking Requirements

Beckn protocol fields can be masked/obfuscated as determined by the Network.
Below is a sample list of fields that can be masked.

**Fields Requiring Masking:**

1. **Personal Identifiers:**
   - `contact.phone`: Mask to show only country code + first 2 digits (e.g., +91-98******00)
   - `contact.email`: Mask domain keeping first 2 chars + domain (e.g., ab****@example.com)
   - `customer.name`: Mask to show only initials (e.g., John Doe → J*** D***)
   
2. **Location Data:**
   - `fulfillment.end.location.gps`: Round to city-level precision (2 decimal places max)
   - `fulfillment.start.location.gps`: Round to city-level precision
   - `billing.address`: Include only city, state, postal code prefix (first 3 digits)
   
3. **Payment Information:**
   - `payment.params.bank_account`: Never log
   - `payment.params.virtual_payment_address`: Never log
   - `payment.params.transaction_id`: Hash using SHA-256
   
4. **Sensitive Network Data:**
   - `quote.breakup`: Log only total amounts, not itemized breakup with pricing details
   - `authorization tokens`: Never log
   - `signing keys`: Never log

**Masking Implementation Approach:**
- Create a configurable PII field registry
- Support field path patterns (e.g., `**.contact.phone`)
- Allow custom masking rules per field type
- Log masked field count in metadata for audit

### 2.4 Log Shipping Cadence

**Batch Processing:**
- **Default batch size**: 100 log entries
- **Default flush interval**: 60 seconds
- **Configurable max wait time**: 5 minutes (safety flush)
- **Retry on failure**: Exponential backoff (100ms → 500ms → 2s → 10s)
- **Maximum retry attempts**: 3

**Real-time Triggers:**
- Critical errors (HTTP 5xx, validation failures, specific Beckn Error codes)
- High-value transactions (configurable threshold)
- Fraud detection triggers (configurable rules)

**Performance Considerations:**
- Asynchronous processing (non-blocking)
- In-memory buffer with overflow to disk (configurable)
- Circuit breaker pattern for API failures
- Compression of payloads before transmission (gzip)

### 2.5 Log Levels for Network Events

**Structured Event Types:**
1. `NETWORK_INFO`: Successful transaction events
2. `NETWORK_WARN`: Partial failures, retries
3. `NETWORK_ERROR`: Transaction failures, validation errors
4. `NETWORK_AUDIT`: High-value or sensitive operations

**Filter Configuration:**
- Allow filtering by action, domain, status
- Support sampling rates (e.g., log 10% of searches, 100% of confirms)


## 3. Technical Requirements

### 3.1 OpenTelemetry Integration - Exporter Side

**Log Exporter Configuration:**
```yaml
NetworkLogs:
  enabled: true
  # The new 'observers' array allows for 2 separate destinations
  observers:
    - id: "network-monitoring"
      enabled: true
      endpoint: https://observer.networkoperator.com/v1/observe/push
      timeout: 10s
      buffer:
        maxSize: 1000
        flushInterval: 60s
      sampling:
        rules:
          - action: search
            rate: 0.5  # 50% sampling
          - action: confirm
            rate: 1.0  # 100% sampling
          - default: 0.5
      piiMasking:
        enabled: true
        configFile: ./config/pii-rules.yaml
    - id: "np1-analytics"
      enabled: true
      endpoint: https://analytics.np1.com/v1/observe/push
      timeout: 10s
      buffer:
        maxSize: 1000
        flushInterval: 60s
      piiMasking:
        enabled: true
        configFile: ./config/pii-rules.yaml
```

**Resource Attributes (per OpenTelemetry conventions):**
- `service.name`: beckn-onix
- `service.version`: 2.0.0
- `service.namespace`: production
- `deployment.environment`: production
- `host.name`: node-instance-id


### 3.2 OpenTelemetry Integration - Receiver Side

The Receiver side must implement folloing API-
`/observe/push`

The service will be operated by the Network Operator and/or Beckn Infra. 

**Log Receiver API Requirements:**

The centralized API should:
1. **Accept OTLP Protocol:**
   - Support OTLP/HTTP
   - Accept compressed payloads (gzip)
   - Implement standard OTLP LogService
   
2. **Authentication & Authorization:**
   - Beckn signature header
   - Rate limiting per client

3. **Data Validation:**
   - Validate OTLP schema conformance
   - Check for required Network fields
   - Reject logs with unmasked PII patterns
   - Size limits per log record (max 256KB)

4. **Storage & Retention:**
   - High-throughput log ingestion (>10K logs/sec)
   - Indexing on: transaction_id, timestamp, action, status
   - Retention policy: Specific to each implementation

5. **Query Interface:**
   - Specific to each implementation

**Sample OTLP Log Record Schema:**
```json
{
  "resource": {
    "attributes": [
      {"key": "subscriber_id", "value": {"stringValue": "bap.example1.com"}},
      {"key": "subscriber_role", "value": {"stringValue": "bap"}},
      {"key": "service_name", "value": {"stringValue": "beckn-onix"}},
      {"key": "environment", "value": {"stringValue": "production"}}        
    ]
  },
  "resource": {
    "attributes": [
      {"key": "latency_ms", "value": 100},
      {"key": "http_status_code", "value": 200},
      {"key": "http_error_message", "value": ""}
    ]
  },
  "logs": [{
    "severityLevel": "INFO",
    "logRecords": [{
        "context": {
          "version": "2.0.0",
          "action": "select",
          "domain": "beckn.one:deg:ev-charging:*",
          "timestamp": "2024-01-15T10:30:00Z",
          "message_id": "bb9f86db-9a3d-4e9c-8c11-81c8f1a7b901",
          "transaction_id": "2b4d69aa-22e4-4c78-9f56-5a7b9e2b2002",
          "bap_id": "example-bap.com",
          "bap_uri": "https://api.example-bap.com/pilot/bap/energy/v2",
          "bpp_id": "example-bpp.com",
          "bpp_uri": "https://example-bpp.com/pilot/bap/energy/v2",
          "ttl": "PT30S"
        },
        "message": {
          "order": {
            "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/main/schema/core/v2/context.jsonld",
            "@type": "beckn:Order",
            "beckn:id": "order-ev-charging-001",
            "beckn:orderStatus": "CREATED",
            "beckn:seller": "ecopower-charging",
            "beckn:buyer": {
              "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/draft/schema/core/v2/context.jsonld",
              "@type": "beckn:Buyer",
              "beckn:id": "user-123",
              "beckn:role": "BUYER",
              "beckn:displayName": "Ravi Kumar",
              "beckn:taxID": "GSTIN29ABCDE1234F1Z5"
            },
            "beckn:orderValue": {
              "currency": "INR",
              "value": 100.0
            },
            "beckn:orderItems": [
              {
                "beckn:lineId": "line-001",
                "beckn:orderedItem": "ev-charger-ccs2-001",
                "beckn:quantity": {
                  "unitText": "Kilowatt Hour",
                  "unitCode": "KWH",
                  "unitQuantity": 2.5
                },
                "beckn:acceptedOffer": {
                  "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/main/schema/core/v2/context.jsonld",
                  "@type": "beckn:Offer",
                  "beckn:id": "offer-ccs2-60kw-kwh",
                  "beckn:descriptor": {
                    "@type": "beckn:Descriptor",
                    "schema:name": "Per-kWh Tariff - CCS2 60kW"
                  },
                  "beckn:items": [
                    "ev-charger-ccs2-001"
                  ],
                  "beckn:provider": "ecopower-charging",
                  "beckn:price": {
                    "currency": "INR",
                    "value": 18.0,
                    "applicableQuantity": {
                      "unitText": "Kilowatt Hour",
                      "unitCode": "KWH",
                      "unitQuantity": 1
                    }
                  },
                  "beckn:validity": {
                    "@type": "beckn:TimePeriod",
                    "schema:startDate": "2024-10-01T00:00:00Z",
                    "schema:endDate": "2025-01-15T23:59:59Z"
                  },
                  "beckn:acceptedPaymentMethod": [
                    "UPI",
                    "CREDIT_CARD",
                    "WALLET"
                  ],
                  "beckn:offerAttributes": {
                    "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/main/schema/EvChargingOffer/v1/context.jsonld",
                    "@type": "ChargingOffer",
                    "buyerFinderFee": {
                      "feeType": "PERCENTAGE",
                      "feeValue": 2.5
                    },
                    "idleFeePolicy": "₹2/min after 10 min post-charge"
                  }
                }
              }
            ]
          }
        }
      }
    }]
  }]
}
```

### 3.3 Configuration Structure

**Extended Module Configuration:**
```yaml
modules:
  - name: bapTxnReceiver
    handler:
      plugins:
        NetworkLogger:
          id: Networklogger
          config:
            enabled: true
            logActions: [search, select, init, confirm, cancel, status]
            piiMaskingRules: ./config/pii-masking.yaml
      steps:
        - validateSchema
        - addRoute
        - logNetworkEvent  # New step
```

**PII Masking Rules File (pii-masking.yaml):**
```yaml
masking_rules:
  - field: "**.contact.phone"
    type: phone
    strategy: mask_middle
    preserve: 
      prefix: 5  # +91-98
      suffix: 2  # last 2 digits
  
  - field: "**.contact.email"
    type: email
    strategy: mask_username
    preserve:
      prefix: 2
  
  - field: "**.location.gps"
    type: gps
    strategy: round
    precision: 2  # decimal places
  
  - field: "**.payment.params.bank_account"
    type: sensitive
    strategy: remove  # Never log
  
  - field: "**.name"
    type: name
    strategy: initials
```

