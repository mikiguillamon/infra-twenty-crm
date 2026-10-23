# 07 - Conexion n8n y API por workspace

- Elegir un workspace `cliente-a` y registrar una API key exclusiva de la integracion JFF en sus settings de API.
- Crear un rol para esa clave limitado a People, Meta Leads, Opportunities y los objetos precisos para la automatizacion. No usar Admin ni reutilizar la misma clave en otro workspace.
- En n8n guardar credenciales por cliente y apuntar al hostname de ese workspace, p.ej. `https://cliente-a.twenty.justforfun.es`.
- Usar la API REST y GraphQL segun requiera el objeto, con `Authorization: Bearer <TOKEN>`. La metadata API depende de version y permisos; descubrir rutas de tu workspace desde Settings -> API y probar antes de automatizar.
- Flujos sugeridos: Meta Lead status -> n8n -> Meta Conversions API, asignacion comercial, notificaciones, scoring, sincronizaciones y auditoria del conector.
- Evitar bucles: integrar idempotency keys, correlacion de lead por ID de Meta, retries con backoff, queue para errores 429 y logging de event ID, workflow y cliente.
- No mezclar claves entre workspaces ni poner secretos en nodes Set, expresiones de logs o payloads de webhook.
- AppUnite almacena Persona + Meta Lead, no crea automaticamente Opportunity ni devuelve conversiones Meta.

Referencia API oficial: https://docs.twenty.com/developers/extend/capabilities/apis
