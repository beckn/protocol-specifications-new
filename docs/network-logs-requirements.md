# Network Logs Shipping Requirements for Beckn-ONIX

## 1. Executive Summary

This document outlines requirements for extending the Beckn-ONIX adapter to ship Network logs to a centralized logging API. The system currently supports application logging through configurable log destinations. This extension will add a new Network-focused logging layer that captures transactional events with PII masking and ships them to a remote API using OpenTelemetry principles.

## 2. Functional Requirements

### 2.1 Network Log Payload Structure

**Core Fields (Required for all logs):**
- `Context`: Beckn Context object

**Operational Fields:**
- `status`: Transaction status (success, failure, timeout, validation_error)
- `latency_ms`: Processing latency in milliseconds
- `http_status_code`: HTTP response code (if applicable)
- `error_code`: Application error code (if failure)
- `error_message`: Masked error description

**Network Context Fields (Network-specific):**
Networks can define a list of Network fields they need to capture, a sample list could look like below-

- `category`: Product/service category (for search/select)
- `provider_id`: Service provider identifier
- `item_ids`: Array of item identifiers in transaction
- `order_value`: Transaction amount (if applicable)
- `fulfillment_type`: Delivery/pickup type
- `location`: City/region (at city level only, not precise location)

**Metadata:**
- `app_version`: Beckn-ONIX adapter version
- `environment`: Deployment environment (dev, staging, production)
- `subscriber_type`: BAP or BPP

### 2.2 PII Masking Requirements

ONIX is aware of Beckn fields and can mask/obfuscate fields determined by the Network.
Below is a sample list of fields that can be masked by the ONIX adapter, before shipping to the receiver API.
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

### 2.3 Log Shipping Cadence

**Batch Processing:**
- **Default batch size**: 100 log entries
- **Default flush interval**: 60 seconds
- **Configurable max wait time**: 5 minutes (safety flush)
- **Retry on failure**: Exponential backoff (100ms → 500ms → 2s → 10s)
- **Maximum retry attempts**: 3

**Real-time Triggers:**
- Critical errors (HTTP 5xx, validation failures)
- High-value transactions (configurable threshold)
- Fraud detection triggers (configurable rules)

**Performance Considerations:**
- Asynchronous processing (non-blocking)
- In-memory buffer with overflow to disk (configurable)
- Circuit breaker pattern for API failures
- Compression of payloads before transmission (gzip)

### 2.4 Log Levels for Network Events

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
  exporter:
    protocol: otlp/http
    endpoint: https://networkanalytics.example.com/v1/network_log_push
    compression: gzip
    timeout: 10s
    headers:
      X-Service-Name: "beckn-onix"
  
  buffer:
    maxSize: 1000
    flushInterval: 60s
    flushOnShutdown: true
    overflowToDisk: true
    diskPath: /var/log/beckn-onix/buffer
  
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
```

**Resource Attributes (per OpenTelemetry conventions):**
- `service.name`: beckn-onix
- `service.version`: 2.0.0
- `service.namespace`: production
- `deployment.environment`: production
- `host.name`: node-instance-id

**Instrumentation:**
- Use `go.opentelemetry.io/otel/log` API
- Create custom LogRecordExporter implementation
- Support for multiple exporters (primary + backup)
- Integrate with existing OpenTelemetry SDK setup

### 3.2 OpenTelemetry Integration - Receiver Side

The Receiver side must implement folloing API-
`analytics_service.domain.com/api/v1/network_log_push`

The service will be operated by the Network Operator

**Log Receiver API Requirements:**

The centralized API should:
1. **Accept OTLP Protocol:**
   - Support OTLP/HTTP and OTLP/gRPC
   - Accept compressed payloads (gzip)
   - Implement standard OTLP LogService
   
2. **Authentication & Authorization:**
   - Bearer token authentication with Beckn signature header
   - API key per subscriber
   - Rate limiting per client
   - IP allowlisting (optional)

3. **Data Validation:**
   - Validate OTLP schema conformance
   - Check for required Network fields
   - Reject logs with unmasked PII patterns
   - Size limits per log record (max 256KB)

4. **Storage & Retention:**
   - High-throughput log ingestion (>10K logs/sec)
   - Indexing on: transaction_id, timestamp, action, status
   - Retention policy: 90 days for detailed logs, 1 year for aggregates
   - Support for log forwarding to long-term storage (S3, etc.)

5. **Query Interface:**
   - RESTful query API with filters
   - Support for time range queries
   - Aggregation APIs (counts, percentiles, etc.)
   - Real-time streaming for monitoring

**Sample OTLP Log Record Schema:**
```json
{
  "resourceLogs": [{
    "resource": {
      "attributes": [
        {"key": "service.name", "value": {"stringValue": "beckn-onix"}},
        {"key": "deployment.environment", "value": {"stringValue": "production"}}
      ]
    },
    "scopeLogs": [{
      "scope": {
        "name": "beckn-network-logs",
        "version": "1.0.0"
      },
      "severityLevel": "INFO",
      "traceId": "hex-encoded-trace-id",
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

### 3.4 Non-Functional Requirements

**Performance:**
- Log capture overhead: <5ms per transaction
- Memory footprint: <100MB for buffer
- CPU overhead: <2% additional load
- No blocking on log shipping failures

**Reliability:**
- 99.9% log delivery guarantee
- Disk buffering for network failures
- Automatic retry with exponential backoff
- Circuit breaker to prevent cascade failures

**Security:**
- TLS 1.3 for API communication
- Mutual TLS (mTLS) support
- Encrypted disk buffer
- No credentials in logs

**Observability:**
- Metrics: logs_shipped_total, logs_failed_total, buffer_size, api_latency
- Health check endpoint for log shipping status
- Alerts on high failure rates or buffer overflow

## 4. Implementation Approach

### 4.1 Plugin Architecture

Create a new plugin type: `NetworkLogger`

**Interface Definition:**
```go
type NetworkLogger interface {
    LogEvent(ctx context.Context, event *NetworkEvent) error
    Flush() error
    Close() error
}
```

### 4.2 Integration Points

1. **Handler Step Integration:**
   - Add `logNetworkEvent` step to handler pipeline
   - Execute after main transaction processing
   - Non-blocking execution

2. **Context Propagation:**
   - Extend context with Network event builder
   - Collect data across multiple steps
   - Final log generation at end of request

3. **Middleware Support:**
   - Pre-processing middleware to capture request details
   - Post-processing middleware to capture response details

### 4.3 Backward Compatibility

- Network logging is opt-in via configuration
- Zero impact when disabled
- Existing application logs unchanged
- Compatible with current plugin architecture

## 5. Success Criteria

1. **Functional:**
   - All Network events captured with <1% loss
   - PII masking 100% effective (validated via regex checks)
   - Configurable sampling working correctly

2. **Performance:**
   - <5ms latency overhead per transaction
   - No blocking on remote API failures
   - Handles 1000+ transactions/sec

3. **Operational:**
   - Easy configuration and deployment
   - Clear documentation and examples
   - Monitoring dashboards available
   - Alerts for anomalies

## 6. Future Enhancements (Out of Scope)

- Real-time analytics dashboards
- ML-based anomaly detection
- Automated compliance reporting
- Log encryption at rest
- Multi-region log aggregation
- Custom webhook integrations