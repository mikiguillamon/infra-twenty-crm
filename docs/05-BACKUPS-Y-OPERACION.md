# 05 - Backups, recuperacion, mantenimiento y escalabilidad

## Backups

- PostgreSQL 16 standalone: activar Scheduled Backups nativos de Coolify en cada entorno, idealmente diario y dirigido a destino offsite cifrado. Verificar que destino no sea el mismo disco del VPS. Retencion inicial 30 dias (ajustar por RGPD y contrato).
- Volumen `twenty-files`: los backups de la BD NO incluyen adjuntos. Crear backup periodico del volumen por separado (snapshot de almacenamiento o contenedor de backup con acceso readonly); replicar cifrado al destino externo. Probar recuperacion de archivo.
- Redis AOF es persistente y ayuda con reinicios, pero NO sustituye un plan de recuperacion. Restaurar Redis/colas requiere entender si tareas ya se procesaron; evitar envios dobles con idempotencia.
- `ENCRYPTION_KEY`: registrar valor secreto en gestor cifrado independiente y procedimiento de rotacion. Sin esa clave, la BD restaurada no permitira descifrar algunos secretos.
- Guardar repositorio Git/version de imagen y configuracion DNS/TLS de Traefik.
- Crear una BD temporal y restaurar backup real antes de traer clientes; verificar login, meta tokens y adjuntos.

## Actualizaciones

1. Crear snapshot/backup validado y registrar version/digest de Twenty y AppUnite.
2. Deploy primero en staging con nuevos tags fijos; ejecutar migraciones una sola vez desde twenty-web.
3. Probar login, permisos, API, Meta webhooks y trabajos cron.
4. Programar despliegue de produccion y plan de rollback que incluya restauracion de BD cuando hay migraciones incompatibles. **Cambiar etiqueta de Docker no revierte el esquema.**
5. Monitorear logs y healthz tras cada despliegue.

## Escalar sin duplicar clientes

- 1 instancia Twenty por entorno con workspaces. Escalar worker cuando haya evidencia de backlog y recurso libre; revisar crons y duplicacion de trabajos antes de replicar.
- Mientras archivos usen un volumen local, no repartir los servicios entre hosts. Para multi-host usar MinIO autoalojado (S3 compatible) y mover adjuntos de modo controlado, tras probar migracion.
- Incrementar RAM/CPU del Main Server segun medidas; para verdadera alta disponibilidad se necesita un segundo host y PostgreSQL/Redis adecuados, no solo un segundo worker.
- Mantener metricas de memoria, disco, conexiones PostgreSQL, tiempos de API, errores de webhooks, cola Redis, y salud/backup.

## Responsabilidad de datos

Documentar contrato de encargo RGPD, ubicacion de datos, retencion de formularios Meta, acceso JFF, incidentes y peticiones de borrado. Las restauraciones desde backup son de la instancia compartida; recuperacion granular de un solo workspace requiere procedimiento y validacion especificos.
