#!/usr/bin/env python3
"""Local configuration preflight, intentionally never prints secret values."""
import argparse
import re
from pathlib import Path
from urllib.parse import urlsplit


def load(path):
    values = {}
    for number, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        row = raw.strip()
        if not row or row.startswith('#'):
            continue
        if '=' not in row:
            raise ValueError(f'Expected KEY=VALUE at line {number}')
        k, v = row.split('=', 1)
        values[k.strip()] = v.strip().strip('"').strip("'")
    return values


def check(values, production):
    errors = []
    required = ['TWENTY_IMAGE_TAG', 'TWENTY_STACK_ID', 'TWENTY_ROOT_DOMAIN',
                'TWENTY_ROUTER_HOST_REGEX', 'SERVER_URL', 'PG_DATABASE_URL',
                'ENCRYPTION_KEY']
    for key in required:
        val = values.get(key, '')
        if not val or 'REPLACE_' in val or 'postgres-on-coolify' in val:
            errors.append(f'{key}: unset or placeholder')
    if values.get('TWENTY_IMAGE_TAG') in ('latest', 'main', 'v2'):
        errors.append('TWENTY_IMAGE_TAG: must be pinned to an exact release')
    root = values.get('TWENTY_ROOT_DOMAIN', '')
    if root and not re.fullmatch(r'[a-z0-9-]+(?:\.[a-z0-9-]+)+', root):
        errors.append('TWENTY_ROOT_DOMAIN: invalid hostname')
    if values.get('SERVER_URL') != f'https://{root}':
        errors.append('SERVER_URL: expected https:// plus TWENTY_ROOT_DOMAIN')
    expected = '[a-z0-9-]+\\.' + root.replace('.', '\\.')
    if root and values.get('TWENTY_ROUTER_HOST_REGEX') != expected:
        errors.append('TWENTY_ROUTER_HOST_REGEX: mismatches the root hostname')
    db = urlsplit(values.get('PG_DATABASE_URL', ''))
    if db.scheme not in ('postgres', 'postgresql') or not db.username or not db.hostname or not db.path or db.path == '/':
        errors.append('PG_DATABASE_URL: expected complete internal PostgreSQL URL')
    if db.hostname in ('localhost', '127.0.0.1'):
        errors.append('PG_DATABASE_URL: must target private Coolify database hostname')
    if len(values.get('ENCRYPTION_KEY', '')) < 43:
        errors.append('ENCRYPTION_KEY: must be at least 256 bits (openssl rand -hex 32)')
    if production and values.get('TWENTY_STACK_ID') == 'stage':
        errors.append('TWENTY_STACK_ID: production must not use stage ID')
    return errors


def main():
    a = argparse.ArgumentParser()
    a.add_argument('env', type=Path)
    a.add_argument('--production', action='store_true')
    opts = a.parse_args()
    if not opts.env.is_file():
        raise SystemExit('Configuration not found')
    issues = check(load(opts.env), opts.production)
    print('Preflight: ' + ('PASS' if not issues else 'FAIL'))
    for issue in issues:
        print(' - ' + issue)
    print('No connection, authentication, licensing, security, or backup claims are made by this preflight.')
    raise SystemExit(1 if issues else 0)


if __name__ == '__main__':
    main()
