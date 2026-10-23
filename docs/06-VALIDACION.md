# 06 - Criterios de aceptacion antes de clientes reales

No marcar la instalacion como lista para produccion hasta completar todos los items:

- [ ] Inventario de CPU, RAM, almacenamiento libre, cuotas y crecimiento esperado; hay margen para despliegue, picos y backups.
- [ ] Imagen de Twenty fijada y revisadas notas de cambios; Compose sin publicacion de `3000`, `5432` o `6379`.
- [ ] Tres workspaces creados en la edicion **self-hosted gratuita** sin bloqueo/licencia de Organization. Verificada viabilidad juridica/comercial para uso SaaS.
- [ ] Instalar AppUnite en todos; ejecutarla multiples veces; confirmar si hay creditos/cuotas y que no se interrumpe con alto volumen.
- [ ] Rol cliente NO puede gestionar Apps, Developers, Logic Functions, Workflows Code, API keys/roles ni crear otro workspace; validado desde UI y API.
- [ ] Alta anonima sin invitacion rechazada tras bootstrap, segun comportamiento real de Twenty v2.48.
- [ ] A/B/C cross-workspace: sin lectura/escritura/exportacion de records/archivos/configuraciones/tokens del resto por UI ni API.
- [ ] SMTP configurado y probado con invitacion y recuperacion de contrasena, evitando servicio pago adicional si no es necesario.
- [ ] DNS wildcard y certificados raiz + wildcard emitidos, renovables y sin romper dominios existentes en Traefik.
- [ ] Meta app de pruebas recibe 10 envios validos, reintento, idempotencia y reconciliacion. Recupera datos tras reinicios.
- [ ] Copia PostgreSQL programada y restaurada en BD temporal; backup y restauracion de un adjunto; clave de cifrado resguardada.
- [ ] Backups offsite y retencion aprobada; logs/rate limiting/alertas suficientes.
- [ ] Actualizacion y rollback documentados y ensayados, incluida recuperacion de BD tras migraciones.
- [ ] Conocida y aceptada la limitacion de seguridad de `LOCAL` (codigo confiable sin sandbox).

Si cualquiera de estos puntos falla, continuar solo en staging hasta resolverlo.
