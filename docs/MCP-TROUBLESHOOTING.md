# MCP Troubleshooting (TRM + Eclipse Copilot)

## Error: "Connection closed"

**Causas comunes**
- Proceso Node del MCP se cerró
- Ruta `args` incorrecta en configuración Eclipse
- Variables de entorno incompletas

**Solución**
1. Ejecuta `node scripts/validate-mcp-setup.js --env /ruta/.env`
2. Verifica rutas `dist/*.js`
3. Reinicia Eclipse y vuelve a abrir Copilot Chat

## Error: "nodeContents schema validation error"

**Mensaje típico**
`Invalid schema for function 'mcp_abap-adt_nodeContents' ... array schema missing items`

**Qué significa**
- Es un problema del schema publicado por la versión del servidor `abap-adt`.

**Solución recomendada**
1. Actualiza a la última versión del servidor ABAP ADT MCP.
2. Si persiste, usa `@abap-mcp` (HTTP) como workaround temporal.
3. Reporta/consulta el issue en el repositorio del servidor MCP.

## Error: "Missing environment variables"

**Síntoma**
- El servidor MCP inicia pero no conecta a SAP.

**Solución**
- Completa como mínimo: `SAP_HOST`, `SAP_PORT`, `SAP_CLIENT`, `SAP_USER`, `SAP_PASSWORD`, `SAP_ROUTER`.
- Para Notes: `SAP_NOTES_USERNAME`, `SAP_NOTES_PASSWORD`.

## Conexión a SAP falla

Checklist:
- VPN activa
- SAP Router vigente
- Usuario no bloqueado
- Cliente correcto (`00`)
- Puerto accesible (`8000`)

Prueba de red (ejemplo):

```bash
# Windows PowerShell
Test-NetConnection 10.11.248.5 -Port 8000
```

## Eclipse no detecta Copilot / MCP

1. Verifica que GitHub Copilot esté habilitado en Eclipse.
2. Revisa logs de Eclipse (`.metadata/.log`).
3. Valida JSON de configuración (`eclipse-copilot-config.json`).
4. Reinicia Eclipse después de cambios en MCP.
