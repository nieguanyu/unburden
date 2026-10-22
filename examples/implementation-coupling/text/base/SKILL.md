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
1. Obtain the names using source.records().
2. Join the names with newlines and return the result.
