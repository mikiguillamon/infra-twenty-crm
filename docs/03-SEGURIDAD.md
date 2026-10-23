# 03 - Modelo de seguridad obligatorio

**Aislamiento:** logico por workspace (registros, objetos, miembros, API keys y secretos separados por tenancy), pero mismo servidor y misma BD PostgreSQL. LOCAL logic functions son procesos Node **sin sandbox** para codigo no confiable.

## Roles

- Mantener como minimo un administrador JFF por workspace. El Admin del workspace NO equivale necesariamente al administrador de servidor.
- Cliente Gestor: leer/editar leads, contactos, oportunidades y tareas. Sin permisos para instalar aplicaciones, desarrollarlas, gestionar funciones, editar workflows con Code, administrar claves/API o gestionar roles. Probar endpoint GraphQL y REST contra estas prohibiciones.
- Cliente Comercial: acceso aun mas limitado. Restringir exportaciones si el caso de negocio lo requiere.
- API key de n8n por workspace: rol especifico, solo objetos/operaciones necesarios. Nunca reutilizar tokens entre clientes. No confiar solo en ocultar UI.
- Si el cliente requiere crear campos personalizados, evaluar permisos independientes de configuracion del modelo de datos. No regalar rol Admin a cambio de esa comodidad.

## Control de codigo

- `LOGIC_FUNCTION_TYPE=LOCAL` solo para AppUnite, con version fija, codigo fuente y dependencias revisadas. Nada de plugins externos arbitrarios ni Code action del builder para clientes.
- `CODE_INTERPRETER_TYPE=DISABLED` (no confundir con las logic functions de las apps).
- Auditar los disparadores de AppUnite, como verifica la firma del webhook y como valida entradas externas.
- Evitar montajes del socket Docker, host networking, credenciales root, puertos publicos y env secretos en logs.
- Probar que un cliente NO puede crear/publicar functions ni `Code` por REST/GraphQL. Si se puede, bloquear go-live hasta resolver permisos.
- Revisar permisos de apps en Twenty 2.48/2.50 antes de actualizar: 2.50 introduce breaking change de apps.

## Comprobaciones de tenancy

1. Crear 3 workspaces con tres cuentas no compartidas.
2. Crear lead A, B, C y adjuntos distintos.
3. Con login/token A intentar leer, modificar, exportar y descargar lead B por ID conocido.
4. Con tokens A intentar consultar endpoints metadata, funciones, secretos, workflows e instalaciones del workspace B.
5. Comprobar que JFF puede administrar el workspace sin usar credenciales de cliente.
6. Probar acceso no invitado antes y despues de arrancar; no fiarse solo del flag de alta.
7. Revisar acceso por hostname y API con un Host header de otro cliente.

**No asumir que passing UI test implica seguridad:** repetir llamadas directas a API y cookies tras deshabilitar funciones.

Documentacion: https://docs.twenty.com/developers/self-host/capabilities/setup
