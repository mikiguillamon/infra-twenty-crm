# 01 - Primer despliegue en Coolify (staging)

## Fase A - Auditoria sin cambios

En SSH del Main Server ejecutar `./scripts/host-preflight.sh` o sus comandos (no destructivos). Reservar holgura de RAM/disco para PostgreSQL, Twenty web, worker y Redis. Dimensionar solo tras ver `docker stats`: no hay memoria libre verificada por MCP.

Actualmente MCP confirma Coolify v4.4.7, servidor localhost disponible, proxy Traefik 3.7.13, red `coolify`, y ausencia de una instalacion Twenty.

## Fase B - Coolify y base de datos

1. Crear proyecto `Twenty CRM`; entorno `staging`.
2. Dentro de `staging`, New Resource -> Database -> PostgreSQL 16.
3. Elegir Main Server / `localhost` y destino Docker `coolify`.
4. Nombrar `twenty-stage-db`, BD `twenty`, usuario especifico `twenty` y password aleatoria URL-safe, si la UI permite modificarlos antes del primer inicio. Alternativamente usar los identificadores generados por Coolify y copiar su URL interna.
5. Dejar `Public access` deshabilitado. No publicar 5432. Start y verificar `healthy`.
6. Copiar la **Postgres URL (internal)** a la variable `PG_DATABASE_URL` del Compose. Guardar como secreto en Coolify. Nunca la incluyas en Git ni en un chat.
7. Activar copia programada hacia almacenamiento remoto **ya configurado y verificado**. La copia de PostgreSQL no cubre volumen de archivos.

## Fase C - GitHub y Docker Compose

1. Crear repositorio privado `mikiguillamon/infra-twenty-crm`.
2. Subir este contenido, sin archivos `.env` reales. Conservar el Compose versionado: no editar versiones efimeras en el panel de Coolify.
3. En Coolify -> `Twenty CRM` -> `staging` -> New Resource -> Application -> GitHub Private Repository -> Docker Compose.
4. Seleccionar `infra-twenty-crm`, rama `main`, ruta `/docker-compose.yml`.
5. En **Advanced > Docker compose > Compose deployment** seleccionar **Raw (deploy file as-is)**. Esta plantilla define explicitamente sus redes `private` y `coolify`, y sus labels de Traefik. No activar simultaneamente otra via de gestion de rutas ni publicar un puerto en el host. Verificar las redes y labels en `Show Deployable Compose`.
6. Como usamos Raw, los dominios se enrutan desde los labels del repo para raiz y todos los subdominios de clientes. **No definir otras reglas de dominio en la UI de Coolify**, pues podrian colisionar. Revisar `Show Deployable Compose` antes de desplegar.
7. Variables: usar `.env.example` como plantilla para los nombres; definir en Coolify **por entorno** y guardar `PG_DATABASE_URL`, `ENCRYPTION_KEY` y otras credenciales como secretos. Para staging usar `TWENTY_STACK_ID=stage` y sus dominios, nunca los de produccion.
8. Generar `ENCRYPTION_KEY` con `openssl rand -hex 32`; copia cifrada fuera del servidor. Sin ella, los secretos en BD no podran recuperarse.
9. Validar con `python3 scripts/validate_env.py .env` en una copia local, si se usa un `.env` local. No mostrar `docker compose config` con valores secretos.
10. **Solo despues de DNS y TLS**, Deploy de staging. Logs de `twenty-web`, `twenty-worker`, `twenty-redis`; `twenty-web` healthz y log de migraciones deben estar correctos.

## Fase D - Provisionar primer usuario

1. Abrir `https://app.twenty-stage.justforfun.es` en una sesion privada antes de dar acceso a nadie.
2. Completar setup, comprobar que existe acceso administrativo **de servidor** (no confundir con `Admin` de workspace). En multi-workspace el primer usuario puede ser regular y requerir bootstrap administrativo en un procedimiento verificable.
3. Mantener registro cerrado en modo invite-only y verificarlo realmente con usuario no invitado. El codigo v2.48 indica que `IS_WORKSPACE_CREATION_LIMITED_TO_SERVER_ADMINS` requiere invitacion o dominio aprobado tras setup, pero la documentacion general aun contiene una advertencia contradictoria: verificar siempre.
4. Configurar SMTP propio en `Settings -> Admin Panel -> Configuration Variables` solo si se utiliza `IS_CONFIG_VARIABLES_IN_DB_ENABLED=true`. Este Compose usa `false` para que toda la configuracion global dependa de entorno; añadir entonces las variables SMTP al Compose del repo y al panel Coolify, no solo a la UI.
5. Crear dos o tres workspaces de pruebas. Comprobar dominios y roles antes de instalar AppUnite.

**No completar Fase D con SQL inventado**. Si no hay admin de servidor, inspeccionar primero el procedimiento oficial de la version fijada.

Documentacion: https://docs.twenty.com/developers/self-host/capabilities/setup
Coolify: https://coolify.io/docs/core/networking-in-coolify

### SMTP con infraestructura existente

Para las invitaciones y recuperacion de contrasenas, usar el SMTP que ya administre JFF. Con el modo `IS_CONFIG_VARIABLES_IN_DB_ENABLED=false`, sumar a `x-twenty-env` las claves que vayas a definir como secretos/variables de Coolify:

```yaml
  EMAIL_DRIVER: smtp
  EMAIL_FROM_ADDRESS: ${EMAIL_FROM_ADDRESS:?Set sender address}
  EMAIL_FROM_NAME: ${EMAIL_FROM_NAME:-Just For Fun CRM}
  EMAIL_SMTP_HOST: ${EMAIL_SMTP_HOST:?Set SMTP host}
  EMAIL_SMTP_PORT: ${EMAIL_SMTP_PORT:-587}
  EMAIL_SMTP_USER: ${EMAIL_SMTP_USER:?Set SMTP user}
  EMAIL_SMTP_PASSWORD: ${EMAIL_SMTP_PASSWORD:?Set SMTP password}
```

Crear las variables en Coolify. Si el proveedor SMTP utiliza el puerto 465 puede necesitar configuracion TLS distinta: comprobar envio real, no forzar 587 sin saber su proveedor. No activar la obligatoriedad anterior antes de disponer de SMTP valido.
