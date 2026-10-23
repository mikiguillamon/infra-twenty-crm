# 04 - Instalar AppUnite de Meta Leads en todos los workspaces

Origen: https://github.com/appunite/meta-for-twenty-crm
Paquete: `@appunite/meta-leads-for-twenty` v1.1.0 (MIT), requiere Twenty >=2.39.0.

## Staging antes que automatizacion

1. Crear un workspace de pruebas administrado por JFF.
2. Ir a Settings -> Applications, permitir aplicaciones community si fuese necesario, instalar `Meta Leads` desde el catalogo en ese workspace.
3. Comprobar que aparezcan `Lead Ads -> Status`, `Meta Leads` y `Lead forms`.
4. Seguir SETUP.md upstream: Meta app con caso `Capture & manage ad leads`, asignacion de pagina, permisos `leads_retrieval`, `pages_show_list`, `pages_manage_metadata` y otros requeridos segun la app.
5. Configurar App ID/secret/Meta Page access token/Page ID en el workspace; usar la funcion Connect de AppUnite si aplica.
6. Registrar webhook `leadgen` en Meta y probar firma, autenticidad de lead, duplicados, faltas y recuperacion horaria.
7. Verificar que los leads siguen llegando despues del restart de web/worker y que no hay consumo pago o bloqueo de ejecuciones.
8. Repetir instalacion para el segundo y tercer workspace y confirmar aislamiento de tokens y rutas. **Una Facebook Page por workspace** en upstream.

## Preinstalacion automatica por JFF

El deseo es que TODOS los nuevos workspaces nazcan con Meta Leads. Una aplicacion se registra a nivel servidor y se instala por workspace. El SDK oficial contiene una funcion `appInstall`; el alta automatica la ejecutara un servicio/procedimiento de aprovisionamiento de JFF autenticado como operador de ese workspace.

Flujo previsto (implementar y validar en staging, no fingir que ya esta listo):

`nuevo cliente -> crear workspace -> asignar JFF admin -> instalar Meta Leads -> verificar installed app -> configurar rol cliente -> crear API key n8n -> invitar usuarios -> cliente conecta su Meta Page`

La publicacion privada y enlaces de compartir pueden tener restricciones de plan. Utilizar inicialmente la version publica MIT del marketplace y comprobar elegibilidad en el self-host gratuito.

## Advertencias

- AppUnite no envia conversiones de vuelta a Meta; crear flujos separados en n8n para Conversions API.
- Los callbacks de una Meta App son globales por objeto; usar una sola Meta App para muchos clientes requiere el resolver multiworkspace/una integracion central, no simplemente pegar varias URLs.
- Un negocio externo puede requerir app review y Advanced Access de Meta.
- Por seguridad, no otorgar al cliente permisos para publicar o editar funciones.
- Una app registrada puede tener resolvers globales propiedad de un workspace: no borrar el workspace propietario sin evaluar el impacto en todas las instalaciones.

Guia upstream: https://github.com/appunite/meta-for-twenty-crm/blob/main/SETUP.md
