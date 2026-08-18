---
name: rag-embedding-design
description: Procedure for designing a RAG retrieval pipeline - chunking strategy, embedding model selection, index sync mode, and retrieval evaluation. Use when a design includes RAG, semantic search, or a vector index as a component.
license: MIT
---

# RAG & Embedding Design

## When to use this
Any design that includes retrieval-augmented generation, semantic search, or
a vector index as a component - not for structured/tabular lookups, which
don't need embeddings at all.

## The procedure

1. **Confirm this actually needs RAG.** If the question can be answered by a
   structured query against governed tables (Unity Catalog, a UC Function),
   that's a cheaper, more accurate, more auditable path than embeddings.
   Check knowledge_base/mosaic_ai_platform.md for the structured alternative
   before defaulting to RAG.

2. **Chunking strategy - choose deliberately, don't default to fixed-size.**
   - Fixed-size chunking (e.g. 512 tokens, 10-15% overlap) is the safe
     default for unstructured prose.
   - Structure-aware chunking (by section, table, or code block) is required
     when source documents have meaningful internal structure - a fixed-size
     chunker will silently split a table mid-row.
   - State which strategy is used, and why. "We used chunking" is not a
     complete answer.

3. **Embedding model selection - state the tradeoff, not just a name.**
   - Managed (e.g. a Databricks-hosted embedding endpoint) trades control
     for zero infrastructure to run.
   - Self-hosted trades operational burden for cost control at scale.
   - State the embedding dimension and whether it's fixed for the index's
     life - switching embedding models later means a full reindex, not an
     incremental update. Flag this as a real migration cost if raised.

4. **Index sync mode - a design decision, not a default.**
   - Delta Sync (index tracks the source table automatically) fits loose
     staleness tolerance.
   - Manual sync is needed when index updates must tie to a specific
     pipeline event rather than firing on every source change.
   - State the staleness tolerance explicitly.

5. **Retrieval evaluation - name a metric, don't just say "we'll evaluate it."**
   - At minimum: recall@k against a held-out set of known query-document pairs.
   - If ranking quality matters, add MRR or NDCG, not just recall.
   - A design proposing RAG with no evaluation plan is incomplete - flag
     this explicitly rather than letting it pass silently.

## What NOT to do
- Do not propose a chunking strategy without stating what happens to tables
  or code blocks in the source documents.
- Do not treat embedding model choice as a minor detail - reindexing cost
  is real and should be priced in now.
- Do not accept "we'll evaluate it later" as a complete answer.
