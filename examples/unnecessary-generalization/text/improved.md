---
name: local-greeting
description: Return a plain-text greeting for the supplied name and punctuation.
---

# Local greeting

## Contract
Return only "Hello, " followed by the supplied name and punctuation, defaulting to !.
Accept every punctuation string verbatim.
The whole procedure is contained here; there are no helper stages or external consumers.

## Procedure
1. Form the greeting directly using the supplied name and punctuation.
2. Return it as plain text.
