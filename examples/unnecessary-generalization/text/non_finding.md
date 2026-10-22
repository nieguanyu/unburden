---
name: delivery-greeting
description: Prepare a greeting for a caller-selected local or queued delivery mode.
---

# Delivery greeting

## Contract
Support local output or an existing queue adapter selected by the caller.
Queued delivery uses a receipt to avoid duplicate delivery on a retry.

## Procedure
1. Form the greeting using the supplied name and punctuation, defaulting to !.
2. For local mode, return it directly.
3. For queue mode, check the existing delivery receipt before submitting through the queue adapter.
4. Return the existing or newly obtained receipt in queue mode.
Do not invent another transport or remove the receipt check from the supported queue path.
