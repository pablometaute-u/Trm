# MCP ABAP Setup para TRM (Eclipse + SAP QAS)

## 1) Objetivo
Esta guía documenta la configuración recomendada del MCP ABAP para conectar Eclipse Copilot Language Server con SAP QAS (PUP) y resolver errores como:

```text
[CopilotMCP] Connection failed: McpError: MCP error -32000: Connection closed
```

## 2) Datos del entorno QAS (TRM)
- Sistema: **QAS - PURO POLLO (PUP)**
- Host: **10.11.248.5**
- Puerto: **8000**
- Cliente: **00**
- SAP Router: **/H/190.145.112.71/S/3299**
- Servidor de aplicación: **10.11.248.5**

> Seguridad: no guardar contraseñas reales en el repositorio. Usa `.env` local (no versionado).

## 3) Setup rápido

### 3.1 Instalar MCP ABAP
```bash
git clone https://github.com/mario-andreschak/mcp-abap-abap-adt-api.git
cd mcp-abap-abap-adt-api
npm install
npm run build
```

### 3.2 Configurar variables de entorno
En este repositorio TRM, copia el ejemplo:

```bash
cp .env.example .env
```

Luego completa al menos:
- `SAP_USERNAME`
- `SAP_PASSWORD`

### 3.3 Configuración de Eclipse (ejemplo)
Agrega/ajusta el servidor MCP en la configuración de Copilot:

```json
{
  "mcpServers": {
    "sap-abap": {
      "command": "node",
      "args": [
        "C:/path/to/mcp-abap-abap-adt-api/dist/mcp-server.js"
      ],
      "env": {
        "AUTH_METHOD": "password",
        "SAP_HOST": "10.11.248.5",
        "SAP_PORT": "8000",
        "SAP_CLIENT": "00",
        "SAP_SYSTEM": "PUP",
        "SAP_ROUTER": "/H/190.145.112.71/S/3299",
        "SAP_USERNAME": "<TU_USUARIO>",
        "SAP_PASSWORD": "<TU_PASSWORD>"
      }
    }
  }
}
```

## 4) Troubleshooting

### Error: `MCP error -32000: Connection closed`
Checklist recomendado:

1. **Node y build válidos**
   - `node --version`
   - Verificar que exista `dist/mcp-server.js`
2. **Variables requeridas presentes**
   - `SAP_HOST`, `SAP_PORT`, `SAP_CLIENT`, `SAP_USERNAME`, `SAP_PASSWORD`
3. **Conectividad de red a QAS**
   - Ejecutar script: `python scripts/validate_mcp_abap_connection.py --from-env`
4. **Credenciales SAP**
   - Validar usuario/clave en SAP GUI
5. **SAP Router**
   - Confirmar que `SAP_ROUTER` esté correcto para acceso remoto
6. **Método de autenticación**
   - `AUTH_METHOD=password` o `AUTH_METHOD=certificate`
7. **Reinicio de Eclipse**
   - Después de cualquier cambio en settings/env

### Error de navegador faltante (si aplica)
Si el MCP requiere Playwright en tu flujo:

```bash
npx playwright install chromium
```

## 5) Validación de conexión
Este repositorio incluye un validador básico:

```bash
python scripts/validate_mcp_abap_connection.py \
  --host 10.11.248.5 \
  --port 8000 \
  --client 00 \
  --user <TU_USUARIO>
```

O cargando desde `.env`:

```bash
python scripts/validate_mcp_abap_connection.py --from-env
```

El script valida:
- Variables obligatorias
- Formato de puerto/cliente
- Conectividad TCP al host:puerto
