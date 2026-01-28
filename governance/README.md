# Beckn Protocol Governance Documentation

## 📋 Overview

This directory contains the **governance framework** for the Beckn Protocol v2.x, including constitutional principles, operational guidelines, contribution standards, and authoring conventions that govern the evolution and implementation of the protocol across its three-layer ecosystem:

- **Layer 1 (Core)**: Domain-agnostic protocol specification
- **Layer 2 (Domain)**: Domain-specific bindings and implementation guides
- **Layer 3 (Network)**: Network-specific profiles, policies, and constraints

These documents establish the rules, processes, and expectations for maintaining protocol coherence, ensuring interoperability, and supporting sustainable ecosystem growth—from core specification changes to domain extensions and network deployments.

---

## 🎯 Purpose

The governance framework exists to protect:

- **Interoperability** across implementations and networks
- **Security, privacy, and user consent** by design
- **Predictable evolution** through clear versioning and compatibility rules
- **Long-term protocol coherence** while supporting innovation
- **Attribution and transparency** in a multi-layer specification ecosystem

---

## 📚 Folder Structure

```
governance/
├── README.md                    # This file - navigation guide
├── GOVERNANCE.md                # Constitutional governance model
├── ATTRIBUTION.md               # Attribution playbook for NFOs
├── CONTRIBUTING.md              # Contribution guidelines for schemas
├── STYLE_GUIDE.md              # Specification authoring standards
└── CORE_WORKING_GROUP.md       # Core working group documentation
```

---

## 📖 Table of Contents

### 🏛️ [**GOVERNANCE.md**](./GOVERNANCE.md)
**Status:** Constitutional Document  
**Precedence:** Highest

The **Beckn Protocol Governance Model** is the authoritative source for all governance matters. This document defines:

- Constitutional principles and design philosophies
- Roles and responsibilities (Core Stewardship Council, Editors, Domain Stewards)
- Decision-making processes and dispute resolution
- Specification change lifecycle and approval gates
- Versioning, compatibility, and deprecation policies
- Core → Domain → Network interaction rules
- Enforcement mechanisms and transparency requirements

**📌 Key Sections:**
- Section 2: The Beckn Credo (Constitutional Intent)
- Section 3: Constitutional Principles
- Section 6: Roles (CSC, Editors, Release Captain, Domain Stewards)
- Section 9: Specification Change Lifecycle
- Section 10: Versioning & Compatibility
- Section 11: Core–Domain–Network Interaction Rules

> ⚠️ **Important:** This document has the highest precedence. All other governance documents are derived from and subordinate to this model.

---

### 🏗️ [**ATTRIBUTION.md**](./ATTRIBUTION.md)
**Status:** Operational Playbook  
**Derived From:** GOVERNANCE.md Section 11 & 12

The **Attribution Playbook for Network Facilitator Organizations (NFOs)** provides structured guidance for publishing network-specific specifications while treating Core + Domain as upstream dependencies.

**Covers:**
- GitHub organization structure for network specifications
- Repository taxonomy and naming conventions
- Managing network profiles, schemas, examples, and documentation
- Attribution requirements and anti-patterns
- Release mechanics across multiple repositories
- CI/CD automation for maintaining consistency

**📌 Key Sections:**
- Section 1: Org-level Principles (Non-negotiable Seatbelts)
- Section 2: GitHub Organization Blueprint
- Section 4: Repository-level Information Architecture
- Section 7: Attribution Requirements
- Section 8: Automated Enforcement

> 🎯 **For:** NFOs, network architects, domain spec authors

---

### 🤝 [**CONTRIBUTING.md**](./CONTRIBUTING.md)
**Status:** Contribution Guidelines  
**Derived From:** GOVERNANCE.md Section 9

Guidelines for **contributing domain-specific schema bundles** to the Beckn Protocol specification repository.

**Covers:**
- Schema bundle folder structure and organization
- When to add a new schema bundle vs. extending existing ones
- Schema extension patterns and requirements
- File descriptions (attributes.yaml, context.jsonld, vocab.jsonld, etc.)
- Naming conventions and versioning
- Migration, validation, and testing requirements

**📌 Key Topics:**
- Adding New Schema Bundles
- Schema Extension Guidelines
- Regional Variations and Regulatory Compliance
- Backward Compatibility Requirements

> 🎯 **For:** Domain contributors, schema authors, developers

---

### ✍️ [**STYLE_GUIDE.md**](./STYLE_GUIDE.md)
**Status:** Authoring Standards  
**Derived From:** GOVERNANCE.md Section 3 & 9

The **Specification Authoring Style Guide** for Beckn Protocol v2.x ensures consistency across API definitions, schemas, JSON-LD contexts, and documentation.

**Covers:**
- Naming conventions (TitleCase types, lowerCamelCase properties, SCREAMING_SNAKE_CASE enums)
- API endpoint and action naming rules
- Schema authoring standards (OpenAPI/JSON Schema)
- JSON-LD conventions and semantic bindings
- Cross-artifact consistency requirements
- Change management and backward compatibility
- Domain and network specification rules

**📌 Key Sections:**
- Section 5: Naming Conventions
- Section 6: API Endpoint Naming
- Section 8: Property Naming
- Section 9: Enum Value Conventions
- Section 10: JSON-LD Conventions
- Section 13: Change Management
- Section 17: Cross-Artifact Consistency Checklist

> 🎯 **For:** Core maintainers, domain authors, network authors, specification editors

---

### 👥 [**CORE_WORKING_GROUP.md**](./CORE_WORKING_GROUP.md)
**Status:** Informational (Draft)

Documentation for the Core Working Group structure, membership, and processes.

> 📝 **Note:** This document is currently empty and under development.

---

## ⚖️ Legal Notice

### Precedence and Authority

This governance folder contains documents with **different levels of authority**:

1. **GOVERNANCE.md** — Constitutional document with highest precedence
2. **Derived documents** (ATTRIBUTION.md, CONTRIBUTING.md, STYLE_GUIDE.md) — Operational guidance derived from GOVERNANCE.md
3. **Informational documents** (CORE_WORKING_GROUP.md) — Supplementary information

When any derived artifact conflicts with GOVERNANCE.md, **GOVERNANCE.md prevails**.

### Governance Intent

These documents are **within scope of the Governance Model of the Beckn Protocol**. They translate governing intent into practical guidance and do not redefine core philosophies, design principles, or policies.

Any conflicts, ambiguity, or gaps should be treated as **input for improving the Governance Model**, not as permission to fork governance intent.

### Lineage

- **Governing Source:** Governance Model of the Beckn Protocol (GOVERNANCE.md)
- **Derived Documents:** Attribution, Contributing, Style Guide
- **Purpose:** Operational guidance, processes, and requirements derived from constitutional principles

---

## 🚀 Getting Started

### For Core Contributors
1. Start with **[GOVERNANCE.md](./GOVERNANCE.md)** to understand the constitutional framework
2. Review **[STYLE_GUIDE.md](./STYLE_GUIDE.md)** for authoring standards
3. Follow **[CONTRIBUTING.md](./CONTRIBUTING.md)** for schema contributions

### For Domain Specification Authors
1. Read **[GOVERNANCE.md](./GOVERNANCE.md)** Section 11 (Core–Domain–Network Rules)
2. Follow **[STYLE_GUIDE.md](./STYLE_GUIDE.md)** Section 14 (Domain-specific Rules)
3. Use **[CONTRIBUTING.md](./CONTRIBUTING.md)** for schema bundle structure

### For Network Facilitator Organizations (NFOs)
1. Review **[GOVERNANCE.md](./GOVERNANCE.md)** Section 11 (Layer-3 Constraints)
2. Implement **[ATTRIBUTION.md](./ATTRIBUTION.md)** for organization structure
3. Follow **[STYLE_GUIDE.md](./STYLE_GUIDE.md)** Section 15 (Network-specific Rules)

### For Implementers
1. Understand the governance framework via **[GOVERNANCE.md](./GOVERNANCE.md)** Section 4 (Scope and Layering)
2. Reference **[STYLE_GUIDE.md](./STYLE_GUIDE.md)** for understanding naming conventions
3. Check domain/network specific guidelines in their respective repositories

---

## 🔄 Document Maintenance

These governance documents are maintained by the **Core Stewardship Council (CSC)** and **Editors** as defined in GOVERNANCE.md Section 6.

### Amendment Process

Amendments to governance documents require:
- Written proposal with rationale tied to constitutional principles
- Time-boxed public review window
- CSC approval (2/3 minimum for GOVERNANCE.md amendments)
- Documentation of changes in version history

### Feedback and Issues

To provide feedback or raise issues about governance:
1. Open an issue in the [protocol-specifications-v2](https://github.com/beckn/protocol-specifications-v2) repository
2. Use appropriate labels: `governance`, `process`, or specific document tags
3. Reference relevant sections and provide clear rationale
4. Allow for community discussion and CSC review

---

## 📞 Questions?

For questions about:
- **Governance processes:** Review GOVERNANCE.md or raise an issue with the `governance` label
- **Contribution guidelines:** See CONTRIBUTING.md or contact the Editors
- **Specification style:** Reference STYLE_GUIDE.md or review recent PRs for examples
- **Network publishing:** Follow ATTRIBUTION.md or reach out to the community

---

## 📄 License

All governance documents in this folder are part of the Beckn Protocol specification and are governed by the repository's LICENSE terms.

---

**Last Updated:** January 2026  
**Maintained By:** Beckn Protocol Core Stewardship Council & Editors
