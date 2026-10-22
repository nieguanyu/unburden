---
name: local-title
description: Extract the first Markdown title from a selected local file.
---

# Local title

## Contract
Read a selected local .md file. Return only its first level-one heading text.
Reject unsupported input and report unreadable or malformed content.

## Procedure
1. Reject a non-.md input and stop.
2. Read and decode the content as UTF-8; report any read or decoding failure.
3. Require a level-one heading; report an error if absent.
4. Return only the heading text.

The filename admission check and the content checks establish different conditions.
