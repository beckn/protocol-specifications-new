# EnergyEnrollment Schema (v0.2)

## Introduction

The **EnergyEnrollment** schema composes with the core Beckn `Fulfillment` and `Order` entities to support program enrollment flows for Digital Energy Programs (VPPs, demand response, P2P trading, etc.). This schema enables credential-based enrollment where the BPP verifies provided credentials, checks for conflicts, and issues enrollment credentials without needing to perform initial eligibility or ownership checks.

### Use Cases

- **Program Enrollment**: Enables users to enroll in digital energy programs (VPPs, demand response, P2P trading, community solar, special tariffs)
- **Credential Verification**: Supports verification of meter ownership, program eligibility, and DER certification credentials
- **Conflict Detection**: Identifies conflicts with existing enrollments (overlapping dates, duplicate meter/DER enrollments)
- **Enrollment Management**: Tracks enrollment lifecycle from initiation through confirmation, active status, and unenrollment
- **Consent Management**: Supports consent credential issuance and revocation for data collection and DER control
- **Audit Trail**: Maintains enrollment logs and references for compliance and record-keeping

### Key Features

- **Credential-Based**: Uses W3C Verifiable Credentials (v2.0) for proof of ownership, eligibility, and enrollment
- **Narrow BPP Role**: BPP verifies credentials and checks conflicts; initial checks handled by calling entity (Portal/BAP)
- **Conflict Prevention**: Detects overlapping enrollments and program conflicts before confirmation
- **Type Coercion**: Context includes type coercion rules for shorter, cleaner examples
- **Status List Integration**: Supports W3C VC Status Lists for credential revocation (consent and enrollment)
- **Lifecycle Management**: Tracks enrollment from pending through active, cancelled, or suspended states
- **Multi-Asset Support**: Handles enrollments with multiple meters and DERs

## Schema Composition Points

This schema composes with:
- `core/v2/attributes.yaml#Fulfillment.fulfillmentAttributes` - For credentials and existing enrollments in `init` requests
- `core/v2/attributes.yaml#Order.orderAttributes` - For enrollment details, verification results, and enrollment credentials in responses

## Context and Type Coercion

The schema provides a context file (`context.jsonld`) that includes type coercion rules, enabling shorter examples by automatically inferring `@type` values from property names:

- `fulfillments` array → `beckn:Fulfillment`
- `items` array → `beckn:Item`
- `provider` property → `beckn:Provider`
- `customer` property → `beckn:Customer`
- `instrument` property → `beckn:Instrument`
- `meters` array → `beckn:Meter`
- `ders` array → `beckn:DER`
- `credentials` array → `VerifiableCredential`
- `credentialVerification` property → `CredentialVerification`
- `conflictCheck` property → `ConflictCheck`
- And more...

Explicit `@type` declarations are still supported and work correctly with type coercion enabled.

## Attributes

### Used in `fulfillmentAttributes` (init request)

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `credentials` | array&lt;VerifiableCredential&gt; | No | Array of W3C Verifiable Credentials provided by calling entity | Contains meter ownership, program eligibility, and DER certification credentials. BPP verifies these credentials without needing to check with utilities or evaluate eligibility criteria. |
| `existingEnrollments` | array&lt;VerifiableCredential&gt; | No | Array of existing enrollment credentials for conflict checking | Provided by calling entity to help BPP identify conflicts. Contains existing ProgramEnrollmentCredential VCs showing current enrollments. |

### Used in `orderAttributes` (on_init response)

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `credentialVerification` | CredentialVerification | No | Results of credential verification performed by BPP | Returned after BPP verifies provided credentials. Contains overall status and list of verified credentials with verification timestamps. |
| `credentialVerification.status` | enum | No | Overall verification status: VERIFIED, FAILED, PARTIAL | Indicates if all, some, or no credentials were successfully verified. |
| `credentialVerification.verifiedCredentials` | array&lt;VerifiedCredential&gt; | No | Array of credentials that were successfully verified | Details of each verified credential including credentialId, status, and verifiedAt timestamp. |
| `conflictCheck` | ConflictCheck | No | Results of conflict checking with existing enrollments | Returned after BPP checks for conflicts. Indicates if conflicts exist and provides details of conflicting enrollments. |
| `conflictCheck.hasConflict` | boolean | No | Boolean indicating if a conflict exists | True if meter/DER is already enrolled in another program with overlapping dates, false otherwise. |
| `conflictCheck.conflictingEnrollments` | array&lt;ConflictingEnrollment&gt; | No | Array of conflicting enrollments (only when hasConflict is true) | Details of each conflict including enrollmentId, programId, conflictReason, and conflictType. |
| `conflictCheck.checkedAt` | date-time | No | Timestamp when conflict check was performed (ISO 8601 UTC) | Used for audit trail and tracking when the check occurred. |
| `conflictCheck.message` | string | No | Human-readable message explaining conflict check results | Provides user-friendly explanation of the conflict check outcome. |

### Used in `orderAttributes` (confirm request)

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `startDate` | date-time | No | Date and time when enrollment becomes active (ISO 8601 UTC) | Specified by calling entity. Enrollment becomes active at this time. May be in the future for scheduled enrollments. |
| `endDate` | date-time | No | Date and time when enrollment expires or ends (ISO 8601 UTC) | Specified by calling entity. Enrollment expires at this time. Used for time-limited program enrollments. |

### Used in `orderAttributes` (on_confirm response)

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `enrollmentId` | string | No | Unique identifier for the enrollment assigned by BPP | Used for tracking, audit, enrollment management, and referencing in unenrollment requests. |
| `status` | enum | No | Enrollment status: ACTIVE, PENDING, CANCELLED, SUSPENDED | Current lifecycle state of the enrollment. ACTIVE when active, PENDING when awaiting activation, CANCELLED when unenrolled, SUSPENDED when temporarily suspended. |
| `programId` | string | No | Identifier of the digital energy program | Matches the program ID from the init request. Identifies which program the user is enrolled in. |
| `startDate` | date-time | No | Date and time when enrollment becomes active (ISO 8601 UTC) | Echoed from confirm request. When the enrollment period begins. |
| `endDate` | date-time | No | Date and time when enrollment expires or ends (ISO 8601 UTC) | Echoed from confirm request. When the enrollment period ends. |
| `enrolledAt` | date-time | No | Timestamp when enrollment was confirmed and logged by BPP (ISO 8601 UTC) | When the enrollment was actually processed. May differ from startDate if enrollment is scheduled for future activation. |
| `credential` | VerifiableCredential | No | Signed enrollment credential issued by BPP | W3C Verifiable Credential (v2.0) proving enrollment. Contains credentialId, type (ProgramEnrollmentCredential), format, credentialData (JWT or JSON-LD), credentialUrl, verificationUrl, issuedAt, and expiresAt. |
| `loggedAt` | date-time | No | Timestamp when enrollment was logged in BPP's audit system (ISO 8601 UTC) | Used for audit trail and compliance. May be same as enrolledAt or slightly later. |
| `logReference` | string | No | Reference identifier for the enrollment log entry | Used for audit trail, record keeping, and log retrieval. Enables tracking and retrieval of enrollment records. |

### Used in `orderAttributes` (update request/response - consent revocation)

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `updateType` | enum | No | Type of update: CONSENT_REVOCATION, UNENROLLMENT | Indicates what type of update is being performed. Used to route the request to appropriate handling logic. |
| `consentRevocation` | ConsentRevocation | No | Consent revocation details | Used in update request to revoke a consent credential, and in on_update response to confirm revocation with status list information. |
| `consentRevocation.consentCredentialId` | uri | No | Identifier of the consent credential being revoked | References the Verifiable Credential ID of the consent being revoked. |
| `consentRevocation.consentType` | enum | No | Type of consent: DATA_COLLECTION, DER_CONTROL, CROSS_UTILITY_SHARING | Identifies which type of consent is being revoked. DATA_COLLECTION for data sharing, DER_CONTROL for device control, CROSS_UTILITY_SHARING for cross-utility data sharing. |
| `consentRevocation.reason` | string | No | Reason for revocation | Values: USER_REQUESTED, PROGRAM_TERMINATED, COMPLIANCE_REQUIREMENT, etc. |
| `consentRevocation.revokedAt` | date-time | No | Timestamp when consent was revoked (ISO 8601 UTC) | In request, when user initiated revocation. In response, when BPP processed it. |
| `consentRevocation.effectiveDate` | date-time | No | Date and time when revocation becomes effective (ISO 8601 UTC) | May be in the future for scheduled revocations. |
| `consentRevocation.status` | enum | No | Revocation status: REVOKED, PENDING (only in response) | REVOKED when processed, PENDING when scheduled for future. Only present in on_update response. |
| `consentRevocation.statusListUrl` | uri | No | URL of W3C VC status list (only in response) | URL where the revoked credential's status is recorded. Used for verification. Only present in on_update response after revocation is processed. |
| `consentRevocation.statusListIndex` | string | No | Index in status list (only in response) | Index in the status list where this credential's revocation status is recorded. Only present in on_update response. |
| `consentRevocation.message` | string | No | Human-readable message about revocation status (only in response) | Provides user-friendly explanation of the revocation outcome. Only present in on_update response. |

### Used in `orderAttributes` (update request/response - unenrollment)

| Attribute | Type | Required | Description | Use Case |
|-----------|------|----------|-------------|----------|
| `unenrollment` | Unenrollment | No | Unenrollment details | Used in update request to cancel enrollment, and in on_update response to confirm cancellation with status list information. |
| `unenrollment.enrollmentId` | string | No | Identifier of the enrollment being cancelled | References the enrollment to be cancelled. Must match an active enrollment. |
| `unenrollment.reason` | string | No | Reason for unenrollment | Values: USER_REQUESTED, PROGRAM_TERMINATED, COMPLIANCE_REQUIREMENT, etc. |
| `unenrollment.effectiveDate` | date-time | No | Date and time when unenrollment becomes effective (ISO 8601 UTC) | May be in the future for scheduled unenrollment. |
| `unenrollment.revokeAllConsents` | boolean | No | Whether all associated consents should be revoked | If true, all consent credentials associated with this enrollment will be revoked during unenrollment. |
| `unenrollment.status` | enum | No | Unenrollment status: CANCELLED, PENDING (only in response) | CANCELLED when processed, PENDING when scheduled for future. Only present in on_update response. |
| `unenrollment.cancelledAt` | date-time | No | Timestamp when enrollment was cancelled (ISO 8601 UTC) (only in response) | When the BPP processed the unenrollment. Only present in on_update response. |
| `unenrollment.enrollmentCredentialStatus` | object | No | Status information for enrollment credential after revocation (only in response) | Contains statusListUrl, statusListIndex, and revoked flag. Only present in on_update response. |
| `unenrollment.consentsRevoked` | array | No | Array of consent credentials revoked during unenrollment (only in response) | Details of each revoked consent credential including consentCredentialId, statusListUrl, statusListIndex, and revoked flag. Only present when revokeAllConsents was true. |
| `unenrollment.message` | string | No | Human-readable message about unenrollment status (only in response) | Provides user-friendly explanation of the unenrollment outcome. Only present in on_update response. |

## VerifiableCredential Structure

The schema uses W3C Verifiable Credentials Data Model v2.0 (`https://www.w3.org/TR/vc-data-model-2.0/`). Each credential object contains:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `credentialId` | string | Yes | Unique identifier for the credential |
| `type` | enum | Yes | Credential type: MeterOwnershipCredential, ProgramEligibilityCredential, DERCertificationCredential, ProgramEnrollmentCredential |
| `format` | enum | Yes | Credential format: VC-JWT, VC-JSON-LD |
| `credentialData` | string | Yes | The credential data itself (JWT or JSON-LD string) |
| `credentialUrl` | uri | No | URL where the credential can be accessed |
| `verificationUrl` | uri | No | URL for verifying the credential |
| `issuedAt` | date-time | No | Timestamp when credential was issued (maps to W3C VC issuanceDate) |
| `expiresAt` | date-time | No | Timestamp when credential expires (maps to W3C VC expirationDate) |
| `derId` | string | No | DER identifier (only for DERCertificationCredential) |

## Example Usage

### Init Request (fulfillmentAttributes)

```json
{
  "beckn:fulfillmentAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/EnergyEnrollment/v0.2/context.jsonld",
    "@type": "EnergyEnrollment",
    "credentials": [
      {
        "credentialId": "vc-meter-ownership-001",
        "type": "MeterOwnershipCredential",
        "format": "VC-JWT",
        "credentialData": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
        "verificationUrl": "https://utility-example-001.com/verify/vc-meter-ownership-001"
      }
    ],
    "existingEnrollments": [
      {
        "credentialId": "vc:enrollment:existing-001",
        "type": "ProgramEnrollmentCredential",
        "format": "VC-JWT",
        "credentialData": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
      }
    ]
  }
}
```

### On_Init Response (orderAttributes)

```json
{
  "beckn:orderAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/EnergyEnrollment/v0.2/context.jsonld",
    "@type": "EnergyEnrollment",
    "credentialVerification": {
      "status": "VERIFIED",
      "verifiedCredentials": [
        {
          "credentialId": "vc-meter-ownership-001",
          "status": "VERIFIED",
          "verifiedAt": "2024-10-15T10:30:05Z"
        }
      ]
    },
    "conflictCheck": {
      "hasConflict": false,
      "checkedAt": "2024-10-15T10:30:05Z",
      "message": "No conflicts found with existing enrollments"
    }
  }
}
```

### On_Confirm Response (orderAttributes)

```json
{
  "beckn:orderAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/EnergyEnrollment/v0.2/context.jsonld",
    "@type": "EnergyEnrollment",
    "enrollmentId": "enrollment-consumer-001",
    "status": "ACTIVE",
    "programId": "program-flex-demand-response-001",
    "startDate": "2024-11-01T00:00:00Z",
    "endDate": "2025-10-31T23:59:59Z",
    "enrolledAt": "2024-10-15T10:35:05Z",
    "credential": {
      "credentialId": "vc:enrollment:consumer-001",
      "type": "ProgramEnrollmentCredential",
      "format": "VC-JWT",
      "credentialUrl": "https://vpp-program-owner.example.com/credentials/vc:enrollment:consumer-001",
      "verificationUrl": "https://vpp-program-owner.example.com/verify/vc:enrollment:consumer-001",
      "issuedAt": "2024-10-15T10:35:05Z",
      "credentialData": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
    },
    "loggedAt": "2024-10-15T10:35:05Z",
    "logReference": "log-enrollment-consumer-001"
  }
}
```

### Update Request - Consent Revocation (orderAttributes)

```json
{
  "beckn:orderAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/EnergyEnrollment/v0.2/context.jsonld",
    "@type": "EnergyEnrollment",
    "updateType": "CONSENT_REVOCATION",
    "consentRevocation": {
      "consentCredentialId": "https://vpp-program-owner.example.com/credentials/vc:consent:consumer-001",
      "consentType": "DATA_COLLECTION",
      "reason": "USER_REQUESTED",
      "revokedAt": "2024-11-20T14:30:00Z",
      "effectiveDate": "2024-11-20T14:30:00Z"
    }
  }
}
```

### Update Request - Unenrollment (orderAttributes)

```json
{
  "beckn:orderAttributes": {
    "@context": "https://raw.githubusercontent.com/beckn/protocol-specifications-new/refs/heads/p2p-trading/schema/EnergyEnrollment/v0.2/context.jsonld",
    "@type": "EnergyEnrollment",
    "updateType": "UNENROLLMENT",
    "unenrollment": {
      "enrollmentId": "enrollment-consumer-001",
      "reason": "USER_REQUESTED",
      "effectiveDate": "2024-11-20T15:00:00Z",
      "revokeAllConsents": true
    }
  }
}
```

## Design Principles

1. **Narrow BPP Role**: BPP only verifies credentials and checks conflicts; initial eligibility and ownership checks are handled by calling entity
2. **Credential-Based**: Uses W3C Verifiable Credentials v2.0 for all proofs and enrollments
3. **Frugal Schema**: Only essential nouns added; reuses existing Beckn structures where possible
4. **Proper Slotting**: Uses standard Beckn slotting (`fulfillmentAttributes`, `orderAttributes`)
5. **Type Coercion**: Context includes type coercion for shorter, cleaner examples
6. **Status List Integration**: Supports W3C VC Status Lists for verifiable credential revocation
7. **Lifecycle Management**: Tracks enrollment from initiation through active status to unenrollment

## Schema Files

- **context.jsonld**: JSON-LD context with type coercion rules
- **vocab.jsonld**: Vocabulary definitions for all EnergyEnrollment terms
- **attributes.yaml**: OpenAPI 3.1.1 schema for grammar and semantics validation

## Related Schemas

- **Core v2**: Base Beckn protocol schemas (`Fulfillment`, `Order`)
- **W3C VC v2.0**: Verifiable Credentials Data Model (`https://www.w3.org/TR/vc-data-model-2.0/`)
- **EnergyResource**: For energy source characteristics in discovery
- **EnergyProsumer**: For prosumer attributes including meters, DERs, credentials, source information, and certification

