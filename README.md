# SOS Contador API - Documentación No Oficial

> ⚠️ **Para IA/LLMs:** Lee [`API_DOCUMENTATION_AI.md`](./API_DOCUMENTATION_AI.md) para documentación completa estructurada.

[![AI Friendly](https://img.shields.io/badge/AI-Friendly-brightgreen)]()
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-blue)]()
[![Python](https://img.shields.io/badge/Python-3.8+-blue)]()

Documentación completa de la API de SOS Contador optimizada para IA y asistentes de código.

**¿Por qué existe este repo?** La documentación oficial solo está en Postman Documenter (no descargable, no importable), lo que hace imposible trabajar con herramientas modernas de desarrollo y IA.

## 📖 Documentación por tipo de usuario

| Tipo | Archivo | Descripción |
|------|---------|-------------|
| 🤖 **IA/Asistentes** | [`API_DOCUMENTATION_AI.md`](./API_DOCUMENTATION_AI.md) | Documentación estructurada optimizada para Claude Code, Copilot, etc. |
| ⚡ **Referencia rápida** | [`QUICK_REFERENCE.md`](./QUICK_REFERENCE.md) | Cheat sheet con ejemplos mínimos |
| 🔧 **OpenAPI Spec** | [`openapi.yaml`](./openapi.yaml) | Especificación OpenAPI 3.0 importable |
| 👨‍💻 **Desarrolladores** | Este README | Guía completa con ejemplos |
| 📝 **Instrucciones Claude** | [`.claude-instructions.md`](./.claude-instructions.md) | Reglas específicas para Claude Code |

## ⚡ Quick Start

```bash
# 1. Clonar repo
git clone https://github.com/sabado/sos-contador-api.git
cd sos-contador-api

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar credenciales
cp .env.example .env
# Editar .env con tus credenciales

# 4. Usar el cliente
python ejemplo_cliente.py
```

## 📋 Información General

- **Base URL:** `https://api.sos-contador.com/api-comunidad/`
- **Autenticación:** Bearer Token (sistema de 2 tokens)
- **Formato:** JSON
- **Documentación oficial:** [Postman Documenter](https://documenter.getpostman.com/view/1566360/SWTD6vnC?version=latest)

## 🔐 Autenticación

La API de SOS Contador utiliza un sistema de autenticación de **dos tokens**:

1. **Token de Usuario:** Obtenido mediante login con credenciales
2. **Token de CUIT:** Obtenido usando el Token de Usuario + ID de CUIT

### 1. Obtener Token de Usuario

**Endpoint:** `POST /login`

**Request:**
```http
POST https://api.sos-contador.com/api-comunidad/login
Content-Type: application/json

{
  "usuario": "tu-email@ejemplo.com",
  "password": "tu-password"
}
```

**Response exitoso:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Notas:**
- El campo `jwt` contiene el **Token de Usuario**
- Este token se usa para obtener el Token de CUIT
- Guardar este token para el siguiente paso

### 2. Obtener Token de CUIT

**Endpoint:** `GET /cuit/credentials/{ID_CUIT}`

**Request:**
```http
GET https://api.sos-contador.com/api-comunidad/cuit/credentials/{ID_CUIT}
Authorization: Bearer {TOKEN_DE_USUARIO}
```

**Parámetros:**
- `{ID_CUIT}`: ID numérico de la CUIT a la cual deseas acceder

**Response exitoso:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Notas:**
- El `jwt` devuelto es el **Token de CUIT**
- Este token se usa para **todas las operaciones posteriores**
- El Token de Usuario ya no es necesario después de este paso

## 📚 Endpoints Principales

### Clientes y Proveedores

#### Listar Clientes/Proveedores

**Endpoint:** `GET /cliente/listado`

**Request:**
```http
GET https://api.sos-contador.com/api-comunidad/cliente/listado?proveedor=true&cliente=true&registros=16&pagina=1
Authorization: Bearer {TOKEN_DE_CUIT}
```

**Query Parameters:**
| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `proveedor` | boolean | Incluir proveedores en el listado | No |
| `cliente` | boolean | Incluir clientes en el listado | No |
| `registros` | integer | Cantidad de registros por página | No |
| `pagina` | integer | Número de página | No |

**Response exitoso:**
```json
{
  "clientes": [
    {
      "id": 1,
      "nombre": "Cliente Ejemplo S.A.",
      "cuit": "30-12345678-9",
      "tipo": "cliente"
    }
  ],
  "total": 100,
  "pagina": 1
}
```

---

### Productos

#### Listar Productos

**Endpoint:** `GET /producto/listado`

```http
GET https://api.sos-contador.com/api-comunidad/producto/listado
Authorization: Bearer {TOKEN_DE_CUIT}
```

#### Crear/Actualizar Producto

**Endpoint:** `PUT /producto/{id}`

```http
PUT https://api.sos-contador.com/api-comunidad/producto/{id}
Authorization: Bearer {TOKEN_DE_CUIT}
Content-Type: application/json

{
  "codigo": "PROD001",
  "nombre": "Producto de ejemplo",
  "precio": 1500.00,
  "alicuota_iva": 21
}
```

**Path Parameters:**
- `id`: ID del producto (usar 0 para crear nuevo)

#### Eliminar Producto

**Endpoint:** `DELETE /producto/{id}`

```http
DELETE https://api.sos-contador.com/api-comunidad/producto/{id}
Authorization: Bearer {TOKEN_DE_CUIT}
```

---

### Ventas

#### Crear/Actualizar Venta

**Endpoint:** `PUT /venta/{id}`

```http
PUT https://api.sos-contador.com/api-comunidad/venta/{id}
Authorization: Bearer {TOKEN_DE_CUIT}
Content-Type: application/json
```

**Path Parameters:**
- `id`: ID de la venta (usar 0 para crear nueva)

**Request Body:**
```json
{
  "idtipo_operacion": 2,
  "fecha": null,
  "idclipro": 1,
  "cuitclipro": "50-00000001-6",
  "fcncnd": "F",
  "letra": "C",
  "puntoventa": 1,
  "numero": 1,
  "obtienecae": false,
  "memo": "Factura de Prueba",
  "referencia": "REF-12345",
  "descuento": 0,
  "uniqueid": "550e8400-e29b-41d4-a716-446655440000",
  "imputaciones": [
    {
      "i": "neto",
      "a": 0,
      "v": 1550.00
    }
  ],
  "productos": [
    {
      "id": 772500,
      "u": 7,
      "fc": 1,
      "fu": 1550.00,
      "fa": 21.00
    }
  ]
}
```

**Campos importantes:**
- `fcncnd`: Tipo de comprobante (F=Factura, NC=Nota Crédito, ND=Nota Débito)
- `letra`: Tipo de factura (A, B, C)
- `obtienecae`: Solicitar CAE a AFIP
- `uniqueid`: UUID único para idempotencia
- `imputaciones`: Array de imputaciones contables
- `productos`: Array de productos vendidos

#### Archivar Venta

**Endpoint:** `PUT /venta/archivar/{id}`

```http
PUT https://api.sos-contador.com/api-comunidad/venta/archivar/{id}
Authorization: Bearer {TOKEN_DE_CUIT}
```

#### Eliminar Venta

**Endpoint:** `DELETE /venta/{id}`

```http
DELETE https://api.sos-contador.com/api-comunidad/venta/{id}
Authorization: Bearer {TOKEN_DE_CUIT}
```

---

### Puntos de Venta

#### Listar Puntos de Venta

**Endpoint:** `GET /puntoventa/listado`

```http
GET https://api.sos-contador.com/api-comunidad/puntoventa/listado
Authorization: Bearer {TOKEN_DE_CUIT}
```

## 💡 Ejemplos de Uso

### Python

```python
import requests

# 1. Login
login_url = "https://api.sos-contador.com/api-comunidad/login"
login_data = {
    "usuario": "tu-email@ejemplo.com",
    "password": "tu-password"
}

response = requests.post(login_url, json=login_data)
user_token = response.json()["jwt"]

# 2. Obtener Token de CUIT
cuit_id = "1665"  # Reemplazar con tu ID de CUIT
cuit_url = f"https://api.sos-contador.com/api-comunidad/cuit/credentials/{cuit_id}"
headers = {"Authorization": f"Bearer {user_token}"}

response = requests.get(cuit_url, headers=headers)
cuit_token = response.json()["jwt"]

# 3. Usar el Token de CUIT para operaciones
clientes_url = "https://api.sos-contador.com/api-comunidad/cliente/listado"
params = {
    "proveedor": True,
    "cliente": True,
    "registros": 16,
    "pagina": 1
}
headers = {"Authorization": f"Bearer {cuit_token}"}

response = requests.get(clientes_url, params=params, headers=headers)
clientes = response.json()

print(clientes)
```

### cURL

```bash
# 1. Login
curl -X POST https://api.sos-contador.com/api-comunidad/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"tu-email@ejemplo.com","password":"tu-password"}'

# Respuesta: {"jwt":"TOKEN_DE_USUARIO"}

# 2. Obtener Token de CUIT
curl -X GET https://api.sos-contador.com/api-comunidad/cuit/credentials/1665 \
  -H "Authorization: Bearer TOKEN_DE_USUARIO"

# Respuesta: {"jwt":"TOKEN_DE_CUIT"}

# 3. Listar clientes
curl -X GET "https://api.sos-contador.com/api-comunidad/cliente/listado?proveedor=true&cliente=true&registros=16&pagina=1" \
  -H "Authorization: Bearer TOKEN_DE_CUIT"
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_BASE = 'https://api.sos-contador.com/api-comunidad';

async function sosContadorAPI() {
  // 1. Login
  const loginResponse = await axios.post(`${API_BASE}/login`, {
    usuario: 'tu-email@ejemplo.com',
    password: 'tu-password'
  });
  
  const userToken = loginResponse.data.jwt;
  
  // 2. Obtener Token de CUIT
  const cuitId = '1665'; // Reemplazar
  const cuitResponse = await axios.get(
    `${API_BASE}/cuit/credentials/${cuitId}`,
    { headers: { Authorization: `Bearer ${userToken}` } }
  );
  
  const cuitToken = cuitResponse.data.jwt;
  
  // 3. Listar clientes
  const clientesResponse = await axios.get(`${API_BASE}/cliente/listado`, {
    params: {
      proveedor: true,
      cliente: true,
      registros: 16,
      pagina: 1
    },
    headers: { Authorization: `Bearer ${cuitToken}` }
  });
  
  console.log(clientesResponse.data);
}

sosContadorAPI();
```

## 🔧 Buenas Prácticas

1. **Seguridad de Tokens:**
   - Nunca expongas los tokens en repositorios públicos
   - Usa variables de entorno para almacenar credenciales
   - Implementa renovación de tokens si es necesario

2. **Manejo de Errores:**
   - Implementa reintentos con backoff exponencial
   - Valida respuestas antes de procesarlas
   - Registra errores para debugging

3. **Paginación:**
   - Usa los parámetros `registros` y `pagina` para manejar grandes volúmenes de datos
   - Implementa lazy loading si trabajas con UI

## ⚠️ Limitaciones Conocidas

- La documentación oficial solo está disponible en Postman Documenter
- No hay especificación OpenAPI/Swagger pública
- Algunos endpoints pueden no estar documentados aquí (documentación incompleta)

## 📖 Recursos Adicionales

- **Sitio oficial:** [SOS Contador](https://www.sos-contador.com/)
- **Blog oficial:** [Blog de SOS Contador](https://www.sos-contador.com/blog/)
- **Ayuda oficial:** [Centro de ayuda](https://ayuda.sos-contador.com.ar/)
- **Soporte técnico:** soporte@sos-contador.com | Tel: 011 5263-0200

## 🤝 Contribuciones

Esta documentación fue creada de forma comunitaria. Si encontrás endpoints adicionales, errores, o mejoras:

1. Fork este repositorio
2. Crea una rama con tus cambios
3. Envía un Pull Request

## 📄 Licencia

Esta documentación es de dominio público. SOS Contador y su API son propiedad de SOS Contador S.A.

## ⚠️ Disclaimer

Esta es documentación **no oficial** creada por la comunidad. Para información autoritativa, consultar con SOS Contador directamente.

---

**Última actualización:** Enero 2026
**Contribuidores:** Comunidad de desarrolladores
