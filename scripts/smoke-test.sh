#!/bin/sh
set -eu
# Public smoke tests for an already deployed staging environment.
BASE=${1:?Usage: smoke-test.sh https://twenty-stage.justforfun.es}
BASE=${BASE%/}
for URL in "$BASE" "$BASE/healthz"; do
  printf '\nChecking %s\n' "$URL"
  curl -fsS -o /dev/null -w 'HTTP %{http_code}, TLS %{ssl_verify_result}, total %{time_total}s\n' "$URL"
done
printf '\nDo not mistake these checks for tenant-isolation, permissions, billing or Meta integration tests.\n'
