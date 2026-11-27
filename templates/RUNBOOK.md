# Runbook

> **Audience:** On-call engineers
> **TL;DR:** _3 lines max — what this document tells the reader._
> **Last verified:** YYYY-MM-DD · commit `abc1234` · Owner: @name

## Contacts
| Role | Name | Contact |
|---|---|---|
| On-call | | |
| Security lead | | |
| DPO / privacy | | |

## Health checks & dashboards
URLs for status, logs, metrics, error tracker, provider status pages.

## Common incidents
### Site down / 5xx spike
1. Check … 2. Roll back with … 3. Communicate via …

### Database full / slow

### Third-party outage (payments, LLM, email)

### Suspected leaked secret
1. Revoke/rotate the key at the provider **immediately** 2. Update the secret manager & redeploy 3. Review provider logs for abuse 4. Purge from git history 5. Post-mortem

## Security incident response (NIST SP 800-61 phases)
Preparation → Detection & analysis → Containment → Eradication → Recovery → Post-incident review.

## Personal-data breach procedure
| Step | Owner | Deadline |
|---|---|---|
| Contain & assess scope | | immediately |
| Notify supervisory authority (GDPR) | DPO | ≤ 72 h after becoming aware |
| Notify Data Protection Board of India & affected principals (DPDP) | DPO | as prescribed by DPDP Rules |
| Notify affected users | | without undue delay |

## Backup & restore
Exact restore commands and expected duration.
