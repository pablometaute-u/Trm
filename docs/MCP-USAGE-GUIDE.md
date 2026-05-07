# Guía de uso MCP en Eclipse Copilot (TRM)

## 1) Uso de `@sap-notes`

Casos comunes:

- Buscar notas por error técnico
- Revisar prerequisitos de implementación
- Consultar correcciones para componentes SAP

Ejemplos de prompts:

- `@sap-notes busca SAP Note para error HTTP 401 en servicios OData`
- `@sap-notes resume las notas relevantes para SAP_BASIS y autenticación`

## 2) Uso de `@abap-adt` para código ABAP

Casos comunes:

- Navegar paquetes/programas en QAS
- Proponer refactors o fixes en objetos ABAP
- Generar clases o reportes para integración TRM

Ejemplos de prompts:

- `@abap-adt lista objetos relacionados con integración TRM`
- `@abap-adt crea un ejemplo de clase para consumir endpoint /api/moneda-valor`

## 3) Ejemplos prácticos con TRM

### Escenario A: diagnóstico de integración

1. `@sap-notes` para buscar notas asociadas a errores de autenticación RFC/HTTP.
2. `@abap-adt` para revisar implementación ABAP actual.
3. Aplicar cambios en ABAP considerando headers `X-API-Key` y manejo de errores HTTP.

### Escenario B: ajuste de consumo de API MonedaValor

- Verificar endpoint esperado: `/api/moneda-valor`
- Validar envío de header `X-API-Key`
- Estandarizar parseo de respuesta JSON (`count`, `data`)

## 4) Best practices

- Mantén `abap-adt` como servidor principal para objetos internos.
- Usa `abap-mcp` remoto como fallback si el servidor local falla.
- No compartas contraseñas en prompts/chat.
- Versiona solo ejemplos (`.env.example`, `*.json.example`), nunca secretos reales.
