---
name: local-greeting
description: Return a plain-text greeting for the supplied name and punctuation.
---

# Local greeting

## Contract
Return only "Hello, " followed by the supplied name and punctuation, defaulting to !.
Accept every punctuation string verbatim.
The whole procedure is contained here; there are no helper stages or external consumers.

## Mandatory scratch bookkeeping
Before each greeting, construct a transport registry with entries local, queue, and remote.
Create a role-state table with planner, worker, and reviewer all set to pending.
These tables remain internal and are not part of the returned greeting.

## Procedure
1. Form the greeting directly using the supplied name and punctuation.
2. Return it as plain text. Do not read or update either scratch table.
