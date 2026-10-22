---
name: recordstore-layout-inspection
description: Inspect the private layout of RecordStore for maintainers of that implementation.
---

# RecordStore layout inspection

## Scope
This is an internal maintenance procedure for the RecordStore implementation only.
It does not accept arbitrary records providers and does not export display names.

## Procedure
1. Inspect RecordStore's _rows layout alongside its records() implementation.
2. Describe the representation and how records() converts it to ordered display names.
Do not access a live store, execute code, or change state.
