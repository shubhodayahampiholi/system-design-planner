# Agent Runtime Hosting - Where the Orchestration Layer Actually Runs
Last verified: Aug 2026

## Databricks-native path
- Databricks Apps: secure, serverless hosting for the app/agent front-end
  and custom agent code within the Databricks environment.
- As of an April 2026 update, Agent Bricks' Supervisor Agent explicitly
  supports custom MCP servers and custom agents running on Databricks Apps
  - not just front-ends, actual agent orchestration code.
- Recommended stack pairing: Agent Bricks (build/evaluate agents) + Model
  Serving (host agent endpoints) + Databricks Apps (serverless hosting of
  the app layer calling those endpoints) + Unity Catalog (governance) +
  Lakebase (operational/app state) + AI Gateway (model access/routing).
- Starting ~September 2026, Databricks Apps is set to be automatically
  enabled for workspaces with the compliance security profile on.

## Azure-native path (Microsoft Foundry)
- Foundry Agent Service's hosted runtime has historically run on Azure
  Container Apps; a newer version (announced ~April 2026) may run on
  per-session MicroVMs instead - the exact current runtime isn't fully
  cl  cl  cl  cl  cl  cl  cl  cl  cl  cl  cl  clrmed.
- Foundry Hosted Agents reached general availability in July 2026. Agent
  code ships as a container image (or deployed from source); Foundry
  provisions compute, assigns a dedicated Entra ID identity, exposes a
  dedicated endpoint.
- Other Azure hosting options outside Foundry specifically: Azure Functions
  (short, event-driven), Container Apps / App Service (PaaS/serverless
  containers), AKS (max control).
- CONFIRMED cross-platform link: Foundry-hosted agents can connect directly
  to Azure Databricks to access workflows and Genie Spaces at runtime - a
  live example of the native-tool boundary being blurred at the runtime
  layer, not just the governance layer the other files describe.

## Open question this file doesn't resolve
Both paths can host a working agent runtime. Nothing in available sources
states a clear preference when the data/governance layer is already
Unity Catalog-centric - that's a real design tradeoff, not a solved one.
