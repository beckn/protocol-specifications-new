# **Attribution Playbook for NFOs \[DRAFT\]**
### _Publishing network architecture, IG overlays, schema extensions, and examples **without** forking/copy-pasting — while giving implementers **one front door**_

# **About this Document**

## Latest published version

TODOs

- [ ] Add the link to the latest version published on the main branch if available. 

## Latest editor's draft

GitHub : 

Note: Contributors must request commenter access to access this draft. Before requesting, please read the [Community Guidelines for Contributing](#) carefully

## Implementation report

- [ ] TODO: To provide link report of how this playbook has been implemented across multiple networks

## Editors

Ravi Prakash (Beckn Labs)  
Pramod Varma (Networks for Humanity)

## Authors

Ravi Prakash (Beckn Labs)

## Feedback

### Issues
No Issues raised.

### Discussions
No Discussions open.

### Pull Requests
No open PRs on this topic.

### GitHub Labels
The following labels MUST be used whenever raising Issues, starting discussions, and submitting PRs regarding this document
- `governance`
- `attribution`
- `core-v2`

## Errata

No Errata exists as of now

# **Acknowledgements**

The author would like to thank the following persons for their valuable contributions to this document.

1. Pramod Varma
2. Sujith Nair
3. Tanmoy Adhikary

## Notice

This document is **within scope of the Governance Model of the Beckn Protocol** (“Governance Model”).

The Governance Model is the **authoritative source** for Beckn’s governing intent—its **philosophies**, **design principles**, and **policies**. Documents like this one are **derived instruments** that translate that intent into practical guidance (analogous to how *regulations* are derived from *policies*).

Accordingly:

- This document **does not redefine** Beckn’s core philosophies, design principles, or policies.
- Where interpretation is needed, the **Governance Model prevails**.
- Any conflicts, ambiguity, or gaps should be treated as **input for improving the Governance Model**, not as permission to fork governance intent.

**Lineage (recommended):**
- **Governing Source:** Governance Model of the Beckn Protocol  
- **Derived From:** Applicable policies / principles defined therein  
- **This Document:** <document name> — operational guidance / process / requirements derived from the above


# Context

Beckn Protocol v2 is built as a **three-layer ecosystem** that’s meant to scale without everyone reinventing the universe every time a new network launches:

1. **Core layer (Beckn Protocol v2):** domain-agnostic verbs and a standard vocabulary for the order lifecycle (Discovery → Ordering → Fulfillment → Post-fulfillment), with schemas that are broadly semantically aligned (e.g., via JSON-LD).
2. **Domain layer (Layer-2 specs):** domain communities (often with NFH and contributors) publish **domain-specific bindings**—schemas, vocab, and Implementation Guides (IGs)—that adapt the core to real industries like energy, mobility, etc.
3. **Network layer (Layer-3 specs):** individual networks (NFO-led) introduce **region- and network-specific requirements**—local policy constraints, regulatory identifiers, payment rails, operational rules, and network governance—while still aiming to remain compatible with core + domain foundations.

This layering is deliberate: **core stays stable**, domains evolve as industry practice matures, and networks move fastest because they’re closest to launch timelines and compliance realities.

That last point creates a very human, very predictable dynamic.

Network-level needs often show up **before** they can be fully normalized into the domain layer (and certainly before they can be absorbed into the core layer). Meanwhile, implementers building for a specific network typically want **one place to read**—a single “home” where the network’s rules and examples live—rather than stitching together guidance across multiple repositories and versions.

Under these conditions, it’s a natural operational outcome that some networks end up **republishing** domain IG material (and sometimes example payloads) inside network repositories, then extending it with network-specific details. This is usually not about intent or attribution avoidance; it’s commonly a side-effect of:

* **Asynchronous evolution** between core, domain, and network layers
* **Go-to-market pressure** (launch dates, ecosystem commitments, regulatory timelines)
* **DX pragmatism** (reducing “repo-hopping” for implementers)
* **Unclear default patterns** for “overlaying” network rules on top of pinned upstream specs

Over time, though, that republishing pattern can introduce ecosystem friction: **drift** between upstream and network material, blurred boundaries between what is core vs domain vs network, and a heavier maintenance burden for everyone involved—especially when upstream continues evolving.

This guideline exists to offer a structured way for networks to publish **network-specific architecture docs, IG overlays, schema extensions, and examples** while treating **Core + Domain** as pinned upstream dependencies and keeping implementers anchored to a single, coherent entry point. 
This playbook describes how an NFO should structure its **GitHub Organization** (not a single repo) so that:

* **Core \+ Domain specs remain upstream dependencies** (pinned, attributable, not rebranded).  
* Network-specific content is authored as **overlays/addenda** \+ **attribute packs**.  
* Implementers experience a **single “home”** (a docs portal \+ predictable repo layout), not scavenger hunts across random folders.

# 0. The North Star: one “front door,” many rooms

**Implementer experience should look like this:**

1. They land on **one URL** (docs portal) with a clean nav:  
     
   * *Architecture*  
   * *Implementation Guides*  
   * *Schemas & Contexts*  
   * *Examples*  
   * *Conformance & Policies*  
   * *Release notes / compatibility matrix*

   

2. Behind the scenes, that portal is built from:  
     
   * **Pinned upstream** (Core \+ Domain)  
   * **Your authored network overlays**  
   * **Your machine-readable extensions** (schemas, JSON-LD contexts)  
   * **Your generated examples** (built from patches)

That separation is the whole trick: **single home ≠ single repo**.


# 1. Org-level principles (non-negotiable seatbelts)

### 1.1 Core \+ Domain are dependencies, not editable content

**MUST**

* Pin upstream references (tags/commits) per network release.  
* Avoid copying upstream IG markdown and “branding” it.

**WHY**

* Copying creates drift; drift becomes technical debt with legal garnish.

### 1.2 Network IGs are overlays, not duplicates

**MUST**

* Network IG content should mostly be:  
    
  * “What’s different here?”  
  * “What’s stricter?”  
  * “What’s added?” (extensions \+ regulatory fields)  
  * “What’s forbidden/optional here?”

### 1.3 Extensions are machine-readable and semantically bindable

**MUST**

* Publish JSON Schema for your packs **and** JSON-LD contexts (`@context`, `@type`).  
* Version these packs and keep their URLs stable.

### 1.4 Examples are patches \+ generated outputs

**MUST**

* Store deltas (JSON Patch / overlays), generate full payloads in CI.  
* Avoid distributing rebranded upstream examples as hand-edited copies.


# 2. The recommended GitHub Organization blueprint

### 2.1 Repo taxonomy (what exists, and why)

A clean org typically has **7–10 repos**. Each repo has one job.

#### A) “Front door” and navigation

1. **`<network>-docs`** **Purpose:** The docs portal source (mkdocs/docusaurus/etc.), published via GitHub Pages or another host. **Contains:** Your authored docs \+ integration hooks to render pinned upstream content.  
     
2. **`.github`** (org-wide) **Purpose:** Community \+ governance wiring (issue templates, PR templates, CODEOWNERS defaults, security policy, contributing). **Contains:** The norms and guardrails, applied everywhere.

#### B) Network specification layer

3. **`<network>-profile`** **Purpose:** The network’s “profile” / manifest of compatibility \+ conformance rules. **Contains:**  
* `DEPENDENCIES.yaml` (pinned upstream refs)  
* conformance rules (MUST/SHOULD/MAY)  
* supported use cases list  
* release metadata  
4. **`<network>-schemas`** **Purpose:** The source of truth for network attribute packs. **Contains:**  
* JSON Schemas  
* JSON-LD contexts  
* mapping tables (network → beckn → schema.org)  
5. **`<network>-examples`** **Purpose:** Patch-first examples \+ generated outputs (built artifacts). **Contains:**  
* `patches/` (source)  
* `generated/` (CI output, optionally released)  
* references to upstream example anchors (pinned)

#### C) Tooling \+ automation

6. **`<network>-tooling`** **Purpose:** The scripts that make “no copy-paste” feasible. **Contains:**  
* patch applicator / example generator  
* schema validation runners  
* JSON-LD validators  
* doc build integration tools  
7. **`<network>-ci`** (optional if you prefer to centralize) **Purpose:** Reusable GitHub Actions workflows (called by other repos). **Contains:** organization-standard CI workflows, release pipelines.

#### D) Policies, legal, and operations

8. **`<network>-policy`** (optional, but recommended for regulated networks) **Purpose:** Network policy, regional policy, security posture, registry rules, onboarding rules. **Contains:** human-readable policy docs \+ machine-readable policy artifacts if any.  
     
9. **`<network>-registry`** (optional, if the network publishes registry schemas or test fixtures) **Purpose:** Registry data models, fixtures, and onboarding validation (not the live registry\!).

You can compress or expand these depending on maturity. The key is: **don’t mix everything into one repo that becomes a landfill.**

# 3. Naming conventions (so humans stop getting lost)

Use predictable names so implementers instantly understand the landscape:

* **Portal:** `<network>-docs`  
* **Compatibility/conformance manifest:** `<network>-profile`  
* **Extensions:** `<network>-schemas`  
* **Examples:** `<network>-examples`  
* **Automation:** `<network>-tooling`  
* **Policies:** `<network>-policy`  
* **Org defaults:** `.github`

Also: add short repo descriptions that begin with the verb:

* “**Builds** the documentation portal…”  
* “**Defines** network attribute packs…”  
* “**Publishes** patch-based examples…”

# 4. What goes where (repo-level information architecture)

### 4.1 `<network>-profile` (the “contract” repo)

This repo is the canonical answer to: **“What does this network support, exactly?”**

**Recommended structure**

```
<network>-profile/
  README.md
  LICENSE
  NOTICE.md
  CHANGELOG.md

  profile/
    DEPENDENCIES.yaml            # pinned upstream refs (core + domain + IG paths)
    SUPPORT_MATRIX.md            # use cases + supported versions
    CONFORMANCE/
      discovery.md
      ordering.md
      fulfillment.md
      post_fulfillment.md
    POLICY_REFERENCES.md         # links to policy repo pages (pinned)

  releases/
    v1.4.0.md                    # human-friendly release note snapshot
```

**MUST**

* Every release tags the repo and updates:  
    
  * `DEPENDENCIES.yaml`  
  * `CHANGELOG.md`  
  * compatibility matrix

### 4.2 `<network>-schemas` (attribute packs \+ contexts)

**Recommended structure**

```
<network>-schemas/
  README.md
  LICENSE
  NOTICE.md
  CHANGELOG.md

  context/
    network/
      payment.upi.v1.context.jsonld
      provider.regulatory.v1.context.jsonld

  jsonschema/
    network/
      payment.upi.v1.schema.json
      provider.regulatory.v1.schema.json

  mapping/
    mapping-matrix.csv           # network term -> beckn term -> schema.org
    notes.md
```

**MUST**

* Context URLs are stable and resolvable.  
    
* Every pack has:  
    
  * `@type` with version semantics  
  * JSON Schema  
  * mapping notes (even if partial)

---

### 4.3 `<network>-examples` (patch-first examples)

**Recommended structure**

```
<network>-examples/
  README.md
  LICENSE
  NOTICE.md
  CHANGELOG.md

  upstream-refs/
    ev-charging.yaml             # upstream example URLs + pinned refs

  patches/
    ev-charging/
      on_search.patch.json
      on_confirm.patch.json

  generated/                     # CI output; never hand-edited
    ev-charging/
      on_search.json
      on_confirm.json

  reports/
    latest-validation.json       # CI output (optional)
```

**MUST**

* Generated outputs are reproducible from:  
    
  * `upstream-refs/*` \+ `patches/*` \+ tooling version

### 4.4 `<network>-docs` (portal)

The portal makes the org feel like a single cohesive “spec.”

**Recommended structure**

```
<network>-docs/
  README.md
  LICENSE
  NOTICE.md

  docs/
    index.md                     # start here
    architecture/
      overview.md
      participants.md
      trust-registry.md
      security.md
    ig/
      ev-charging/
        overlay.md               # network deltas only
        conformance.md
        workflows/               # diagrams you authored
        faq.md
    schemas/
      packs.md                   # links + explanation of packs
    examples/
      ev-charging.md             # links to generated examples
    releases/
      index.md                   # links to profile release notes

  mkdocs.yml (or docusaurus config)
  tools/
    fetch-upstreams/             # pull pinned upstream content at build time
```

**Critical detail:** The portal should *render* upstream content **without copying it into your authored docs**. Two common patterns:

* **Build-time fetch:** CI pulls upstream repos at pinned refs and injects pages into the build (best for “no upstream code in your git history”).  
* **Submodules/subtrees:** portal repo includes upstream as submodules at pinned commits (simple, but noisier).

Both are fine if attribution is explicit and version pinning is strict.

### 4.5 `.github` (org guardrails)

**Recommended contents**

```
.github/
  CONTRIBUTING.md
  SECURITY.md
  CODE_OF_CONDUCT.md
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
  workflows/
    reusable-validate.yml
    reusable-release.yml
```

**MUST**

* Standard PR checklist includes:  
    
  * “Does this copy upstream content?” (should be “no”)  
  * “Is `DEPENDENCIES.yaml` pinned/updated if needed?”  
  * “Were examples generated via patch pipeline?”  
  * “Are NOTICE/attribution requirements met?”

# 5. “Single home” without copying: how implementers don’t bounce around

### Option A (recommended): docs portal composes upstream \+ overlay

* Portal navigation shows:  
    
  * Upstream Core/Domain sections (rendered from pinned refs)  
  * Network overlay sections (authored here)


* Every upstream-derived page displays:  
    
  * upstream source repo  
  * pinned ref  
  * license/notice pointer

### Option B: portal deep-links into upstream at pinned refs

Lower effort, less “single home” feeling, but still compliant:

* Portal pages are mostly curated indexes  
* Links go to upstream `blob/<tag-or-commit>/...` paths

# 6. Release mechanics across multiple repos (so versions don’t drift)

### 6.1 Release train: “profile” is the master version

Treat `<network>-profile` as the **release coordinator**.

A network release `v1.4.0` should correspond to:

* `<network>-profile` tag: `v1.4.0`  
* `<network>-schemas` tag: `v1.4.0` (or compatible `v1.4.x`)  
* `<network>-examples` tag: `v1.4.0`  
* `<network>-docs` tag: `v1.4.0` (optional but nice)

### 6.2 Compatibility is declared once

`DEPENDENCIES.yaml` in `<network>-profile` is canonical. Other repos may reference it or import it in CI.

# 7. Attribution: make “forgetting” structurally hard

### 7.1 Org-wide `NOTICE.md` expectations

Each repo MUST include a `NOTICE.md` that lists:

* Upstream repos used  
    
* Exact refs  
    
* Licenses and required notices  
    
* A sentence like:  
    
  * “This repository contains network-specific overlays and extensions. Upstream specifications remain authoritative.”

### 7.2 File-level attribution for overlays

At the top of every overlay IG page:

* Base reference (pinned)  
* What is authored here  
* Copyright attribution split

# 8. CI: automated enforcement of “no fork trap”

Minimum CI gates (run on PRs for relevant repos):

* **Schemas repo**  
    
  * JSON Schema validation  
  * JSON-LD context sanity checks


* **Examples repo**  
    
  * Patch applies cleanly to pinned upstream examples  
      
  * Generated outputs validate against:  
      
    * core schema  
    * domain schema(s)  
    * network pack schemas


* **Docs repo**  
    
  * Build succeeds with pinned upstream refs  
  * Link checker (optional)  
  * “Attribution banner required” check (optional but useful)


# 9. Anti-patterns (now at org scale)

* A repo named “`<network>-deg`” that is literally a fork with logos swapped.  
* A `docs/` folder inside every repo containing overlapping copies of the same IG text.  
* Hand-edited “generated” examples committed without a reproducible pipeline.  
* “Compatible with main” statements (that’s roulette, not compatibility).


# 10. The “go-live in 2 weeks” org starter kit

If you’re under launch pressure, create only these repos first:

1. `.github`  
2. `<network>-profile` (pin dependencies \+ conformance deltas)  
3. `<network>-schemas` (packs \+ contexts)  
4. `<network>-examples` (patches \+ generator)  
5. `<network>-docs` (portal that links/renders pinned upstream)

That’s enough to ship fast **without** falling into copy-paste debt.

# Conclusion

At org level, this becomes pleasantly boring in the best way: upstream specs are **libraries**, your network is a **profile \+ overlays \+ extensions**, and your portal is a **compiled reading experience**—all versioned, attributable, and validator-friendly. The universe remains strange and delightful, but your Git history doesn’t have to be.  
