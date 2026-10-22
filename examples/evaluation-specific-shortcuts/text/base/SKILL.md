---
name: count-words
description: Count whitespace-delimited words in the text argument.
---

# Count words

## Contract
Count all nonempty whitespace-delimited words in the supplied text argument.
Request metadata does not change the meaning of a word count.
Return only the resulting integer.

## Procedure
1. Split the text argument on whitespace.
2. Count the resulting nonempty words and return the integer.
