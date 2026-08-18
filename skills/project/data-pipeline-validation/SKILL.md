---
name: data-pipeline-validation
description: Checklist for validating a data ingestion or transformation pipeline design before it's approved - idempotency, schema handling, late data, and failure recovery. Use whenever a design includes a data ingestion, ETL, or transformation pipeline.
license: MIT
---

# Data Pipeline Validation

## When to use this
Any design that includes data ingestion, ETL/ELT, or a transformation
pipeline as a component - before the design is finalized, not after.

## The procedure

1. **Idempotency - can this pipeline be safely re-run?**
   - If a job fails halfway and re-runs, does it duplicate rows or cleanly
     resume/overwrite?
   - Merge/upsert on a natural or surrogate key is generally required for
     anything that isn't strictly append-only, immutable event data.
   - Flag "this job only runs once a day so it's fine" as a reliability
     assumption, not a g     assumption, not a g     assumption, nndling - explicit, not implicit.**
   - State what happens on a new column (should not break the pipeline), a
     removed column (should fail loudly, not silently drop data), or a type
     change (should fail loudly - silent coercion corrupts downstream data).
   - "Schema-on-read" is not a substitute for a stated evolution policy.

3. **Late-arriving and out-of-order data.**
   - State the watermark/lateness tolerance for any time-windowed
     aggregation. Data arriving after the watermark either gets dropped
     (state this explicitly) or triggers reprocessing.
   - If the pipeline assumes in-order arrival, state that assumption -
     it's often false in practice.

4. **Incremental vs. full refresh - state which, and why.**
   - Incremental is cheaper but needs a reliable "what's new" mechanism -
     name it (timestamp column, CDC feed, file-arrival marker).
   - Full refresh is self-healing but doesn't scale past some volume - state
     the threshold where it stops being viable.

5. **Failure recovery.**
   - Can the pipeline resume from the failure point, or restart from scratch?
   - Is there alerting on failure, or does a silent failure just mean stale
     data with no signal to anyone?

## What NOT to do
- Do not approve a design that doesn't state its idempotency behavior.
- Do not let schema evolution be an unstated assumption.
- Do not treat failure recovery as a detail to figure out later - it
  changes the pipeline's actual architecture and needs deciding up front.
