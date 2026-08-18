# Microsoft Foundry / Databricks Native Connector
Last verified: Aug 2026

- Branding note: formerly "Azure AI Foundry", referred to as "Microsoft
  Foundry" in Databricks' own partnership materials as of mid-2026 — naming
  has been in flux this year, confirm current branding before citing externally.
- ~July 23, 2026: Databricks and Microsoft expanded native integration across
  Unity AI Gateway, Genie, Microsoft Foundry, Purview, and OneLake.
- Concretely: Azure AI Foundry / Azure AI Agent Service can call UC-governed
  datasets and pre-built operational tools directly, without bypassing UC's
  access controls.
- OPEN QUESTION, not resolved by available sources: does data flowing through
  this connector still need a *separate* Purview-side policy, or does UC's
  policy alone suffice end-to-end? Treat as an explicit open design question,
  not an assumption, in anything built on this file.
