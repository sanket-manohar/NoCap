# Runbook — NoCap

> **Audience:** Maintainers
> **TL;DR:** How to respond to bad releases, false-positive storms and security reports.
> **Last verified:** 2026-11-27 · v1.0.0

## Bad release / broken installer
Move the `v1` tag back, pin the README to the last good tag, open a pinned issue.

## False-positive storm on a rule
Lower the severity or narrow the regex in a patch release. Add a regression test using the reported snippet.

## Security report
Acknowledge within 72 h through a private advisory, fix on a private fork, release, then publish the advisory with credit.

## Suspected repo compromise
Revoke maintainer tokens, audit recent commits and tags, re-tag from a verified commit, and notify users via README and Release.
