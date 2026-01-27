# Beckn Network Observability - Requirements

## 1. Executive Summary

This document outlines specification for Network Participants for sending Network logs to a centralized Observability system. This specification details out the following-
- New Network entity type, called `Observer`, that implements an API to receive logs from other Network Participants.
- Exporter requirements to be implemented by BAP/BPP entities including
   - data points to be sent,
   - filtering & masking of sensitive fields,
   - Cadence of sending logs.


## 2. Functional Requirements

### 2.1 Support for Two Observers

- Exporter can send logs to `two` independent Receiver APIs, i.e. two Network Observers. One could be the Observer operated by the Network Operator for Governance and another could be any additional Observer that may offer comprehensive Network aware Analytics capability.
- If Observability is enabled by the BAP or BPP NPs, then sharing with 1 or 2 Observers is configurable.
- Support separate Configuration for each Observer.
- Initialization: Upon startup, the observability module iterates through the list of configured observers. It instantiates a separate `Exporter` for each entry.
- Execution: When a Beckn request is processed, the observability exporter pushes the data to all active Observers concurrently.
- Failure Handling: A failure to push to one Observer should not interrupt the flow to another Observer, ensuring that separate configurations provide operational redundancy.

### 2.2 Network Log Payload Structure
Networks can define a list of Network fields they need to capture, the exporter configuration could be setup accordingly. A sample list could look like below-

**Network Core Fields (Required for all logs):**
- `Context`: Beckn Context object

**Network Business Fields (Network-specific):**
- `message`: Beckn Message object (for search/select)
- `error`: Beckn Error object

**Operational Fields:**
- `latency_ms`: Processing latency in milliseconds
- `http_status_code`: HTTP response code (if applicable)
- `http_error_message`: HTTP error message

**Metadata:**
- `app_version`: Beckn-ONIX adapter version
- `environment`: Deployment environment (dev, staging, production)
- `role`: BAP or BPP

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


### 2.4 Log Shipping Cadence
Network Operators can define a configuration of cadence, that the exporter could be setup with. Supported configuration attributes with sample values are listed below-

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

### 2.5 Sampling for Network Events

**Filter Configuration:**
- Allow filtering by action, domain, status
- Support sampling rates (e.g., log 10% of searches, 100% of confirms)

### 2.6 Compliance with W3C Headers (Open Telemetry standards)

The W3C specification defines [spec](https://www.w3.org/TR/trace-context/) standard HTTP headers and a value format to propagate context information that enables distributed tracing scenarios, that are also needed for Beckn enabled network.

The Beckn schema is already aligned with W3C spec in terms of the required context information. The mapping of W3C fields to corresponding Beckn schema fields is as per below- 

`traceparent` describes the position of the incoming request in its trace graph in a portable, fixed-length format. Every tracing tool MUST properly set traceparent even when it only relies on vendor-specific information in tracestate.
1. `traceparent.version` maps to `context.version` from the Beckn schema.
2. `traceparent.trace_id` maps to `context.transaction_id` from the Beckn schema.
3. `traceparent.parent_id` maps to `context.{bap_id|bpp_id}` from the Beckn schema concatenated with `role` (BAP or BPP) by character `:`. This ensures that most Otel tools can reconcile traces to piece together chain of all interactions for a particular transaction.

Additionally, `context.message_id` can be used for action specific observability.

`tracestate` extends traceparent with vendor-specific data represented by a set of name/value pairs. Storing information in tracestate is optional. 

### 2.7 API to receive Observability events

**API to Receive events
`/v1/observe/push`

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
   - Specific to each implementation## 3. Technical Requirements

### 3.0 Sample Coonfiguration

**Sample Exporter Configuration:**
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

**Sample PII Masking Rules File (pii-masking.yaml):**
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

