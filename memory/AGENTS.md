# Scoping Decisions Log

- 2026-08-15 [native tooling scope]: Client's technical answers (serverless compute, Private Link/NCC, Mosaic AI Provisioned Throughput terminology) confirm they want the Databricks-native stack (Databricks Apps, Mosaic AI Vector Search/Model Serving, Unity Catalog) rather than the Azure-native stack (Foundry Agent Service, Azure AI Search). Treat "native tooling" as Databricks-native by default for this engagement unless told otherwise.
- 2026-08-15 [network compute plane]: Agent compute stays serverless (no VNet injection); private VNet resources are reached via Private Link + Network Connectivity Config (NCC), not by injecting Databricks into the customer VNet.
- 2026-08-15 [model serving throughput mode]: Enterprise-wide, moderate-volume usage — client prefers Provisioned Throughput serving over pay-per-token for predictable cost/latency. No hard SLA number defined yet.
- 2026-08-15 [private DB access pattern]: The private database is accessed read-only, at query time, via an agent tool call — it is supplementary lookup data, not part of the RAG vector index/corpus.
- 2026-08-15 [governance data readiness]: The governed customer data for RAG already exists in Unity Catalog as Delta tables, ready to be indexed — no migration/ingestion design needed for the source data itself.
