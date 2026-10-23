# Twenty CRM / Just For Fun - Coolify

**Purpose:** repeatable, no-AWS staging candidate for a shared Twenty multi-workspace CRM with approved local logic functions for the AppUnite Meta Lead Ads app.

**Status:** Compose/YAML and env example prepared; not deployed or production certified. Do not onboard real clients until the acceptance gates in `docs/06-VALIDACION.md` are completed.

## Decisions

- One Twenty instance per environment (not per customer).
- Twenty image pinned to `twentycrm/twenty:v2.48.0` pending staging regression tests. Latest on GitHub as of 2026-10-23 is v2.50.0; do not auto-upgrade.
- One isolated Coolify standalone PostgreSQL 16 database **per environment** to use Coolify scheduled backups.
- Redis and data volume per Compose deployment; no public ports.
- Raw Git-based Docker Compose deployment: all Traefik labels and Docker networks are defined by the repo; do not let Coolify generate duplicate domain labels.
- `IS_MULTIWORKSPACE_ENABLED=true`; namespaced subdomains of `twenty.justforfun.es` (production) or `twenty-stage.justforfun.es` (staging).
- `LOGIC_FUNCTION_TYPE=LOCAL`; `CODE_INTERPRETER_TYPE=DISABLED`. This is an explicit security exception for vetted functions only, not a sandbox. User permissions and API access must prevent customer-supplied logic functions, code nodes and app publishing.
- Local file storage is supported on a **single Docker host**. It MUST be backed up off-server; for horizontal multi-host deployments migrate to a separately hosted MinIO/S3-compatible object store before increasing server count.
- AppUnite is installed on each workspace during provisioning. Registration and installation are separate operations; automatic installation script must be validated with the target Twenty version first.

## Critical pre-deployment blocker: free self-host licensing and usage

Official Twenty v2.48 docs list **Unlimited workspaces** as an Organization (paid) feature despite documenting a multi-workspace switch. They also describe execution credits. It is NOT verified that the free self-host edition will meet the desired number of client workspaces and Meta lead events. Test three independent workspaces, application installs, multiple real webhook events, and inspect billing/limits before deploying actual customer data. Never bypass commercial feature checks or patch licensing code.

Official sources:
- https://github.com/twentyhq/twenty/blob/twenty/v2.48.0/packages/twenty-docs/user-guide/billing/capabilities/pricing-plans.mdx
- https://github.com/twentyhq/twenty/blob/twenty/v2.48.0/packages/twenty-docs/user-guide/billing/how-tos/billing-faq.mdx

## Repository files

- `docker-compose.yml` - server + worker + Redis, external PostgreSQL, private ports and Traefik labels
- `.env.example` - public placeholders only; never commit real `.env` secrets
- `scripts/host-preflight.sh` - non-destructive capacity audit
- `scripts/validate_env.py` - static config verification without printing values
- `scripts/smoke-test.sh` - basic HTTP/TLS checks
- `docs/01-INICIO.md` - exact Coolify setup instructions
- `docs/02-DNS-Y-TRAEFIK.md` - Cloudflare DNS-01 wildcard certs and proxy precautions
- `docs/03-SEGURIDAD.md` - role isolation and LOCAL code acceptance checks
- `docs/04-META-APPUNITE.md` - app installation and Meta permissions
- `docs/05-BACKUPS-Y-OPERACION.md` - backup/restore and scaling runbooks
- `docs/06-VALIDACION.md` - mandatory production go/no-go tests
- `docs/07-N8N-Y-API.md` - one workspace API key per client and automation guardrails

## First tasks

1. Run non-destructive preflight on Main Server (script in `scripts/host-preflight.sh`), share CPU/RAM/disk summaries without credentials.
2. Create private GitHub repository `infra-twenty-crm` and commit this package (not secrets).
3. Create **staging only** in Coolify, with its standalone PostgreSQL 16 and private network connection.
4. Confirm dynamic Traefik wildcard TLS on staging. The global DNS-challenge change affects all existing domains: back up and plan it.
5. Deploy and create three sandbox workspaces; verify permissions, billing, AppUnite and cross-workspace isolation.
6. Only after passing all tests create production with independent PostgreSQL/storage/keys.

## Fundamental limitations

- Each workspace is **logically** isolated; there is one shared runtime and PostgreSQL server in the environment. No hardware isolation or per-customer database backups.
- LOCAL code has no untrusted-code sandbox. Auditing and roles reduce risk, but do not eliminate it.
- AppUnite upstream supports **one Facebook Page per workspace** and does not send lead qualification feedback to Meta. n8n can provide conversion feedback.
- A single Docker host is not high availability. Worker replication, object storage, database failover and external monitoring are future scaling phases, not included here.
- Twenty code is mostly AGPLv3, with MIT packages and commercial-licensed files. Comply with Twenty's licenses, use free-edition features only, and review implications before offering modified versions as SaaS.
