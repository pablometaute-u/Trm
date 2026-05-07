# MCP Setup para TRM + Eclipse Copilot

Esta guía configura dos servidores MCP para trabajar con SAP desde Eclipse Copilot:

- `sap-notes`: búsqueda y lectura de documentación SAP Notes
- `abap-adt`: desarrollo ABAP remoto contra QAS

## 1) Requisitos previos

- Node.js 18+ (`node -v`)
- Eclipse 2026-03 o superior con GitHub Copilot habilitado
- Acceso de red al sistema QAS (VPN/SAP Router)
- Credenciales SAP (QAS) y S-User para SAP Notes

## 2) Instalación de SAP Notes MCP

```bash
# ejemplo local
cd C:/tools
npm install
# en el repo del servidor notes
npm run build
```

Configura variables en `.env` (basado en `.env.example`):

- `SAP_NOTES_USERNAME`
- `SAP_NOTES_PASSWORD`

## 3) Instalación de ABAP ADT MCP

```bash
# ejemplo local
cd C:/tools
npm install
# en el repo del servidor abap adt
npm run build
```

Variables mínimas para conexión QAS:

- `SAP_HOST=10.11.248.5`
- `SAP_PORT=8000`
- `SAP_CLIENT=00`
- `SAP_USER=JMETAUTE`
- `SAP_PASSWORD=<tu_password>`
- `SAP_ROUTER=/H/190.145.112.71/S/3299`

## 4) Configuración de variables de entorno

1. Copia `.env.example` a `.env`.
2. Reemplaza placeholders por credenciales reales.
3. Nunca subas `.env` al repositorio.

```bash
copy .env.example .env
```

## 5) Configuración en Eclipse Copilot

1. Copia `eclipse-copilot-config.json.example` a tu configuración real de MCP en Eclipse.
2. Ajusta rutas `args` a las rutas locales donde compilaste cada servidor.
3. Reinicia Eclipse.
4. Verifica en Copilot Chat que aparezcan `@sap-notes`, `@abap-adt` y (opcional) `@abap-mcp`.

## 6) Validación rápida

Ejecuta el validador incluido:

```bash
node scripts/validate-mcp-setup.js --env /ruta/al/.env
```

Si todo está bien verás `MCP setup validation completed successfully`.
