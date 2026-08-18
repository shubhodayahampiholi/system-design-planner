---
name: native-tool-scoping-check
description: Checks whether a request to use "native tooling" is genuinely unambiguous, given the deep current integration between Databricks-native and Azure-native (Microsoft Foundry) services. Use before proposing any design that assumes one stack without confirming scope.
license: MIT
---

# Native-Tool Scoping Check

## When to use this
Any time a request says "use native tooling" or similar, without further qualification.

## The procedure
1. Check /memory/AGENTS.md for an existing scoping decision covering this
   question. If one exists, treat it as binding and stop here - do not
   re-litigate it.
2. If no decision exists, do not assume either interpretation. "Native
   tooling" is genuinely ambiguous between:
   - Databricks-native only (Mosaic AI, Unity Catalog, Genie, Agent Bricks)
   - The combined stack, now that Databricks and Microsoft Foundry are
     natively integrated (see /knowledge_base/microsoft_foundry_connector.md)
3. Surface the ambiguity explicitly as a scoping question. Do not silently
   pick one and proceed.
4. Once resolved, the decision should be persisted to /memory/AGENTS.md
   (subject to human approval) so it doesn't need re-asking.

## What NOT to do
- Do not assume "native" means Databricks-only by default.
- Do not resolve the ambiguity yourself without asking, even if one
  interpretation seems more likely.
