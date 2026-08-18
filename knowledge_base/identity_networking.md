# Identity & Networking
Last verified: Aug 2026

## Identity
- Entra ID is the shared identity provider across Databricks and Azure-native
  services; service principals and managed identities are issued here.

## Workspace deployment models
- Standard (Databricks-managed network) vs. VNet-injected (customer-managed
  VNet, more control over egress and connectivity).
- Dated, platform-level: after March 31, 2026, new Azure VNets default to
  private configurations with NO outbound internet access. New Databricks
  workspaces now require an explicit outbound method (e.g. a NAT Gateway) -
  this is a default change affecting all new deployments, not an edge case.

## Serverless compute + VNet - previously unresolved here, now answered
- Serverless compute runs in a Databricks-managed VNet by default and does
  NOT have built-in access to private customer VNet resources out of the
  box - confirmed, this genuinely is a real constraint.
- Solvable via a separate mechanism: outbound Private Link from serverless
  to customer VNet resources, configured through a Network Connectivity
  Configuration (NCC) - an account-level construct routing through an Azure
  Load Balancer. Limits: up to 10 NCCs per region per account, 100 private
  endpoints per region, an NCC can attach to up to 50 workspaces. Billed
  separately as cross-VNet networking cost.
- Serverless + Unity Catalog has built-in data exfiltration protection as a
  baseline; Private Link is an additional layer, not a replacement for it.

## Private Link connection types (three, independently configurable)
- Front-end (user-to-workspace): browser/REST API/JDBC-ODBC/Power BI over a
  private endpoint.
- Back-end/classic (classic compute-to-control-plane): requires Premium
  plan, VNet injection, and secure cluster connectivity (no public IP).
- Outbound/serverless: as described above, via NCC.
- A workspace can enforce private-only connectivity, auto-rejecting all
  public network access.
