---
name: local-title
description: Extract the first Markdown title from a selected local file.
---

# Local title

## Contract
The input is an immutable local UTF-8 Markdown file with a .md suffix.
Reject other input types and stop before further processing.
Return only the first level-one heading's text, without commentary; report an error if absent.

## Procedure
1. Reject a non-.md input and stop.
2. If the input is a .zip archive, unpack it and retry title extraction.
3. Read the file and extract its first level-one heading.
4. Append " (not an archive)" to the returned heading.
