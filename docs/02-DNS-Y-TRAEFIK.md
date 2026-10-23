# 02 - DNS wildcard y certificados HTTPS

## DNS propuesto

Zona: `justforfun.es` (en Cloudflare). Registro A para `twenty-stage` y A wildcard para `*.twenty-stage` apuntando a la IP publica de Main Server. Mas adelante A `twenty` y `*.twenty` para produccion. Usar **DNS only** inicialmente si Cloudflare Universal SSL no cubre subdominios de segundo nivel; no asumir que la nube orange resuelve automaticamente `cliente.twenty.justforfun.es`.

Un certificado `*.twenty-stage.justforfun.es` NO cubre `twenty-stage.justforfun.es`. Emitir certificado para ambos SAN.

## Traefik DNS-01

Traefik actual en Main Server: 3.7.13. La configuracion es GLOBAL; reiniciarlo puede afectar Frappe y el resto de recursos.

1. Guardar copia de la configuracion actual de proxy desde Coolify antes de editar.
2. Obtener en Cloudflare un API Token limitado a la zona DNS de `justforfun.es` y escritura DNS; guardarlo como secreto.
3. Coolify -> Servers -> localhost -> Proxy -> Configuration. Conservar el resto de la configuracion y seguir la guia oficial para pasar el resolver letsencrypt de HTTP-01 a DNS-01 con Cloudflare. Guardar cambios en Coolify, no solo en el archivo del servidor.
4. Reiniciar Traefik en ventana controlada; verificar inmediatamente dominios existentes y logs ACME.
5. En Proxy -> Dynamic Configurations crear el archivo de wildcard para staging (ver ejemplo mas abajo), verificar que el certificado se emite y se renueva.
6. No desplegar produccion hasta probar ambos certificados y hostname routing de tres clientes.

Ejemplo dinamico para STAGING (revisar antes de aplicar):

```yaml
http:
  routers:
    twenty-stage-cert:
      rule: 'HostRegexp(`[a-z0-9-]+\.twenty-stage\.justforfun\.es`)'
      entryPoints:
        - https
      priority: 1
      service: twenty-cert-placeholder
      tls:
        certResolver: letsencrypt
        domains:
          - main: twenty-stage.justforfun.es
            sans:
              - '*.twenty-stage.justforfun.es'
  services:
    twenty-cert-placeholder:
      loadBalancer:
        servers: []
```

Nota: el ejemplo de Coolify usa prioridad baja para solicitar wildcard; los routers reales del Compose tienen prioridad 10.

Documentacion oficial:
- https://coolify.io/docs/core/networking/proxy/traefik/dns-challenge
- https://coolify.io/docs/core/networking/proxy/traefik/wildcard-certs

No introducir credenciales de Cloudflare en este repositorio.
