# Cloud, Containers, Kubernetes & IaC Checklist

## Containers (Docker)
- [ ] Base image pinned by version and ideally digest. Minimal base (distroless/alpine/slim)
- [ ] Multi-stage build. No compilers or secrets in the final image
- [ ] `USER` non-root. `HEALTHCHECK` defined
- [ ] No secrets in `ENV`/`ARG`/layers. Use BuildKit `--mount=type=secret`
- [ ] `.dockerignore` excludes `.git`, `.env`, `node_modules` and keys
- [ ] Images scanned (Trivy/Grype) in CI and rebuilt regularly

## Kubernetes
- [ ] `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`
- [ ] No `privileged`, `hostNetwork`, `hostPID` or docker.sock mounts
- [ ] Resource requests and limits set. Liveness/readiness probes
- [ ] NetworkPolicies default-deny. RBAC least privilege. No default service account tokens where unneeded
- [ ] Secrets come from an external secrets manager (ESO, Sealed Secrets, CSI driver). Encryption at rest enabled in etcd
- [ ] Pod Security Admission set to `restricted`

## Cloud (AWS / GCP / Azure / Vercel / Netlify / Cloudflare)
- [ ] Root/owner account has MFA and isn't used day-to-day. SSO for humans
- [ ] IAM least privilege. No long-lived access keys (OIDC for CI)
- [ ] Storage buckets private. Public assets served through a CDN with origin access control
- [ ] Databases private. No 0.0.0.0/0 on SSH/RDP/DB ports
- [ ] Encryption at rest with KMS. TLS in transit everywhere
- [ ] Audit logging (CloudTrail / Cloud Audit Logs / Activity Log) on and retained
- [ ] Billing alerts and budgets set
- [ ] Backups automated, cross-region, restore-tested
- [ ] WAF / DDoS protection on public endpoints
- [ ] Preview deployments don't expose production data or secrets

## Infrastructure as Code (Terraform / Pulumi / CloudFormation / Bicep)
- [ ] State stored remotely, encrypted, with locking. No secrets in state outputs
- [ ] Modules and providers pinned
- [ ] Scanned in CI (Checkov / tfsec / Trivy config / KICS)
- [ ] `plan` reviewed in PRs. Drift detection

## CI/CD (GitHub Actions / GitLab / others)
- [ ] `permissions: contents: read` by default. Write access granted per job
- [ ] Third-party actions pinned to a full commit SHA
- [ ] No `${{ github.event.* }}` interpolation inside `run:` (use env vars)
- [ ] `pull_request_target` avoided, or never checks out untrusted code
- [ ] Secrets scoped to environments with required reviewers for production
- [ ] Branch protection: reviews, status checks, no force-push

**Tools:** Trivy, Grype, Checkov, tfsec, kube-bench, kube-linter, Prowler, ScoutSuite, zizmor (GitHub Actions), OpenSSF Scorecard.
