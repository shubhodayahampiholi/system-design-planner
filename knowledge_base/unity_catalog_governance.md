# Unity Catalog — Governance Layer
Last verified: Aug 2026

- Databricks-native governance: catalogs, schemas, tables/volumes, fine-grained
  ACLs, automatic lineage across notebooks, jobs, dashboards, and ML models.
- Unity AI Gateway governs models, agents, and cost within the UC boundary —
  positioned as an enforcement path, not just observability.
- Genie: natural-language query interface over UC-governed data. Genie Ontology
  adds a semantic/relationship layer on top of raw tables.
- As of the ~July 2026 Microsoft partnership expansion: permissions and lineage
  established in UC are automatically honoured by Azure AI services that go
  through the native Foundry connector — NOT for anything routed around it.
