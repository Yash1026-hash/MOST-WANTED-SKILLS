# OKF concept templates (v0.2)

Replace placeholders. Use real timestamps with offset. Omit any field you cannot honestly fill (especially `verified`).

## Table / data asset
```markdown
---
type: BigQuery Table
title: Customer Orders
description: One row per completed customer order across all channels.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, orders]
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
---

# Schema

| Column | Type | Description |
|---|---|---|
| `order_id` | STRING | Globally unique order identifier. |
| `customer_id` | STRING | FK into [customers](/tables/customers.md). |

# Examples

    SELECT COUNT(*) FROM sales.orders WHERE placed_at >= '2026-01-01'
```

## Metric
```markdown
---
type: Metric
title: Monthly Active Users
description: Distinct users with at least one qualifying event in a calendar month.
tags: [product]
status: stable
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
stale_after: 2027-01-26T00:00:00Z
---

# Definition
...computed by [the MAU computation](/computations/mau.md).
```

## Playbook (no resource)
```markdown
---
type: Playbook
title: "Incident response: data freshness alert"
description: Steps to triage a freshness alert on the orders pipeline.
tags: [oncall]
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
---

# Trigger
# Steps
1. ...
```

## Reference / decision / glossary term
```markdown
---
type: Reference
title: Fiscal year definition
description: Acme's fiscal year runs Feb 1 - Jan 31.
sources:
  - { id: policy, resource: https://wiki.example/finance/calendar, title: Finance calendar }
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
---
Fiscal year starts 1 February.[^policy]

[^policy]: Finance calendar
```

## Attested Computation
```markdown
---
type: Attested Computation
title: Revenue for fiscal year
description: Recognized revenue for a fiscal year, per Finance's definition.
status: stable
runtime: bigquery
parameters:
  - { name: year, type: integer, required: true }
executor:
  resource: references/skills/run-on-bq.md
  receipt: [job_id, executed_sql, result]
attester:
  resource: references/attesters/sql-equality.py
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
verified: { by: human:<id>, at: 2026-10-26T09:00:00Z }   # ONLY if that human confirmed it
stale_after: 2027-01-26T00:00:00Z
sources:
  - { id: rev-policy, resource: https://wiki.example/finance/revenue-recognition, title: Revenue recognition policy }
---

# Computation

    SELECT SUM(amount) AS revenue
    FROM finance.recognized_revenue
    WHERE fiscal_year = @year

Per the recognition policy.[^rev-policy]

[^rev-policy]: Revenue recognition policy
```

## Root index.md
```markdown
---
okf_version: "0.2"
---

# Metrics

* [Monthly Active Users](metrics/mau.md) - Distinct users with a qualifying event in a month.

# Subdirectories

* [tables](tables/)
```

## log.md
```markdown
# Directory Update Log

## 2026-10-26
* **Creation**: Added [Customer Orders](/tables/orders.md).
```
