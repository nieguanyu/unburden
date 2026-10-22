---
name: container-repository-summary
description: Summarize the selected repository in the documented container environment.
---

# Container repository summary

## Contract
This skill runs in a container whose default repository mount is /workspace.
An explicitly selected accessible repository overrides that default.

## Procedure
1. Use the explicitly selected root when present; otherwise use /workspace.
2. Read README.md under that root and summarize it.
3. Report an error if that repository or README is inaccessible; do not substitute a personal checkout.
