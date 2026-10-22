---
name: export-record-names
description: Export ordered names from a records provider.
---

# Export record names

## Provider contract
Accept any source exposing records(), which returns display-name strings in required order.
The provider owns its storage; consumers must not depend on private fields.
Join those returned names with newline characters, preserving their order.

## Procedure
1. Reject the source unless its exact class is RecordStore.
2. Read source._rows directly instead of calling source.records().
3. Join those names with newlines and return the result.
