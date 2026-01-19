# SOS Contador API - Documentación para IA

> Documentación estructurada de la API de SOS Contador optimizada para uso con herramientas de IA y asistentes de código.

## Información Base

```yaml
base_url: https://api.sos-contador.com/api-comunidad
authentication: Bearer Token (JWT)
token_type: Dos niveles (Usuario + CUIT)
content_type: application/json
```

---

## Autenticación

### 1. Login - Obtener Token de Usuario

```http
POST /login
Content-Type: application/json
```

**Request Body:**
```json
{
  "usuario": "string (email)",
  "password": "string"
}
```

**Response:**
```json
{
  "jwt": "string (JWT token de usuario)"
}
```

**Uso:** Este token se usa para obtener el token de CUIT.

---

### 2. Obtener Token de CUIT

```http
GET /cuit/credentials/{id}
Authorization: Bearer {USER_TOKEN}
Content-Type: application/json
```

**Path Parameters:**
- `id` (integer): ID de la CUIT a acceder

**Response:**
```json
{
  "jwt": "string (JWT token de CUIT)"
}
```

**Uso:** Este token se usa para TODAS las operaciones posteriores.

---

## Endpoints - Productos

### GET /producto/listado

Listar productos registrados.

```http
GET /producto/listado
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Query Parameters:**
- `registros` (integer, opcional): Cantidad de registros por página
- `pagina` (integer, opcional): Número de página

**Response:** Lista de productos

---

### PUT /producto/{id}

Crear o actualizar un producto.

```http
PUT /producto/{id}
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Path Parameters:**
- `id` (integer): Identificador del producto (usar 0 para crear nuevo)

**Request Body:**
```json
{
  "codigo": "string (código del producto)",
  "nombre": "string (nombre/descripción)",
  "unidad": "string (unidad de medida)",
  "precio": "number (precio unitario)",
  "alicuota_iva": "number (alícuota IVA, ej: 21)",
  "activo": "boolean (si está activo)"
}
```

**Response:** Datos del producto creado/actualizado

---

### DELETE /producto/{id}

Eliminar un producto.

```http
DELETE /producto/{id}
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Path Parameters:**
- `id` (integer): Identificador del producto a eliminar

**Response:** Sin cuerpo de respuesta (204 No Content)

---

## Endpoints - Clientes/Proveedores

### GET /cliente/listado

Listar clientes y/o proveedores.

```http
GET /cliente/listado
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Query Parameters:**
- `proveedor` (boolean): Incluir proveedores (true/false)
- `cliente` (boolean): Incluir clientes (true/false)
- `registros` (integer): Registros por página (default: 16)
- `pagina` (integer): Número de página (default: 1)

**Response:**
```json
{
  "clientes": [
    {
      "id": "integer",
      "nombre": "string",
      "cuit": "string",
      "tipo": "string (cliente|proveedor)"
    }
  ],
  "total": "integer",
  "pagina": "integer"
}
```

---

## Endpoints - Puntos de Venta

### GET /puntoventa/listado

Listar puntos de venta registrados.

```http
GET /puntoventa/listado
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Response:** Lista de puntos de venta

---

## Endpoints - Ventas

### PUT /venta/{id}

Crear o actualizar una venta/factura.

```http
PUT /venta/{id}
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Path Parameters:**
- `id` (integer): Identificador de la venta (usar 0 para crear nueva)

**Request Body:**
```json
{
  "idtipo_operacion": "integer (tipo de operación)",
  "fecha": "string|null (fecha YYYY-MM-DD, null = hoy)",
  "idclipro": "integer (ID del cliente/proveedor)",
  "cuitclipro": "string (CUIT del cliente/proveedor)",
  "idcuenta": "integer|null (ID de cuenta)",
  "fcncnd": "string (F=Factura, NC=Nota Crédito, ND=Nota Débito)",
  "letra": "string (A, B, C)",
  "puntoventa": "integer (número de punto de venta)",
  "numero": "integer (número de comprobante)",
  "numerohasta": "integer|null (número hasta para lotes)",
  "obtienecae": "boolean (solicitar CAE a AFIP)",
  "fechaiva": "string|null (fecha para IVA)",
  "idprovinciaiibb": "integer|null (ID provincia para IIBB)",
  "idcentrocosto": "integer|null (ID centro de costo)",
  "memo": "string (descripción/memo)",
  "referencia": "string (referencia externa)",
  "descuento": "number (descuento en %, ej: 10.5)",
  "uniqueid": "string (UUID único para idempotencia)",
  "imputaciones": [
    {
      "i": "string (tipo: neto, iva, otros)",
      "a": "number (alícuota)",
      "v": "number (valor)"
    }
  ],
  "productos": [
    {
      "id": "integer (ID del producto)",
      "u": "number (cantidad/unidades)",
      "fc": "number (factor de conversión)",
      "fu": "number (precio unitario)",
      "fa": "number (alícuota IVA)"
    }
  ]
}
```

**Campos importantes:**

- **idtipo_operacion**: Tipo de operación (consultar catálogo)
- **fcncnd**: Tipo de comprobante
  - `F` = Factura
  - `NC` = Nota de Crédito
  - `ND` = Nota de Débito
- **letra**: Tipo de factura según régimen
  - `A` = Responsable inscripto a responsable inscripto
  - `B` = Responsable inscripto a consumidor final
  - `C` = Monotributista
- **obtienecae**: Si es `true`, solicita CAE a AFIP
- **uniqueid**: UUID para prevenir duplicados (mismo UUID = misma operación)
- **imputaciones**: Array de imputaciones contables
  - `i`: Tipo de imputación (neto, iva, otros)
  - `a`: Alícuota (0 para neto)
  - `v`: Valor
- **productos**: Array de items de la venta
  - `id`: ID del producto
  - `u`: Unidades/cantidad
  - `fc`: Factor de conversión (normalmente 1)
  - `fu`: Precio unitario
  - `fa`: Alícuota de IVA (ej: 21 para 21%)

**Response:** Datos de la venta creada/actualizada

**Ejemplo completo:**
```json
{
  "idtipo_operacion": 2,
  "fecha": null,
  "idclipro": 1,
  "cuitclipro": "50000000016",
  "idcuenta": null,
  "fcncnd": "F",
  "letra": "C",
  "puntoventa": 1,
  "numero": 1,
  "numerohasta": null,
  "obtienecae": false,
  "fechaiva": null,
  "idprovinciaiibb": null,
  "idcentrocosto": null,
  "memo": "Factura de Prueba",
  "referencia": "Factura Prueba 12345",
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

---

### PUT /venta/archivar/{id}

Archivar una venta (marcar como archivada).

```http
PUT /venta/archivar/{id}
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Path Parameters:**
- `id` (integer): Identificador de la venta

**Response:** Sin cuerpo de respuesta

---

### DELETE /venta/{id}

Eliminar una venta.

```http
DELETE /venta/{id}
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

**Path Parameters:**
- `id` (integer): Identificador de la venta a eliminar

**Response:** Sin cuerpo de respuesta (204 No Content)

---

## Flujo de Trabajo Típico

### 1. Crear una Factura Completa

```
1. POST /login
   → Obtener USER_TOKEN

2. GET /cuit/credentials/{cuit_id}
   → Obtener CUIT_TOKEN

3. GET /cliente/listado?cliente=true
   → Obtener lista de clientes y sus IDs

4. GET /producto/listado
   → Obtener lista de productos y sus IDs

5. PUT /venta/0
   → Crear nueva venta con:
     - idclipro y cuitclipro del cliente
     - productos con IDs obtenidos
     - uniqueid único (generar UUID)
```

### 2. Actualizar un Producto

```
1. Autenticarse (pasos 1-2)

2. GET /producto/listado
   → Encontrar el producto a modificar

3. PUT /producto/{id}
   → Actualizar con nuevos datos
```

---

## Códigos de Error Comunes

- `401 Unauthorized`: Token inválido o expirado
- `404 Not Found`: Recurso no encontrado
- `400 Bad Request`: Datos inválidos en el request
- `500 Internal Server Error`: Error del servidor

---

## Buenas Prácticas para IA

### 1. Generación de UUID

Siempre generar un UUID único para `uniqueid` en ventas:

```python
import uuid
unique_id = str(uuid.uuid4())
```

```javascript
const { v4: uuidv4 } = require('uuid');
const uniqueId = uuidv4();
```

### 2. Cálculo de Imputaciones

Para una venta con IVA:

```python
neto = 1550.00
iva_alicuota = 21.00
iva_monto = neto * (iva_alicuota / 100)
total = neto + iva_monto

imputaciones = [
    {"i": "neto", "a": 0, "v": neto},
    {"i": "iva", "a": iva_alicuota, "v": iva_monto}
]
```

### 3. Validación de CUIT

Formato: XX-XXXXXXXX-X (ej: 50-00000001-6)

### 4. Manejo de Fechas

- Formato: `YYYY-MM-DD`
- `null` = fecha actual
- Zona horaria: Argentina (UTC-3)

### 5. Idempotencia

Usar siempre el mismo `uniqueid` para reintentos de la misma operación.

---

## Schemas JSON

### Schema: Venta

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "idtipo_operacion",
    "idclipro",
    "cuitclipro",
    "fcncnd",
    "letra",
    "puntoventa",
    "numero",
    "uniqueid",
    "imputaciones",
    "productos"
  ],
  "properties": {
    "idtipo_operacion": {"type": "integer"},
    "fecha": {"type": ["string", "null"], "format": "date"},
    "idclipro": {"type": "integer"},
    "cuitclipro": {"type": "string", "pattern": "^\\d{2}-\\d{8}-\\d$"},
    "idcuenta": {"type": ["integer", "null"]},
    "fcncnd": {"type": "string", "enum": ["F", "NC", "ND"]},
    "letra": {"type": "string", "enum": ["A", "B", "C"]},
    "puntoventa": {"type": "integer", "minimum": 1},
    "numero": {"type": "integer", "minimum": 1},
    "numerohasta": {"type": ["integer", "null"]},
    "obtienecae": {"type": "boolean"},
    "fechaiva": {"type": ["string", "null"], "format": "date"},
    "idprovinciaiibb": {"type": ["integer", "null"]},
    "idcentrocosto": {"type": ["integer", "null"]},
    "memo": {"type": "string"},
    "referencia": {"type": "string"},
    "descuento": {"type": "number", "minimum": 0, "maximum": 100},
    "uniqueid": {"type": "string", "format": "uuid"},
    "imputaciones": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["i", "a", "v"],
        "properties": {
          "i": {"type": "string"},
          "a": {"type": "number"},
          "v": {"type": "number"}
        }
      }
    },
    "productos": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "u", "fc", "fu", "fa"],
        "properties": {
          "id": {"type": "integer"},
          "u": {"type": "number"},
          "fc": {"type": "number"},
          "fu": {"type": "number"},
          "fa": {"type": "number"}
        }
      }
    }
  }
}
```

---

## Ejemplos de Uso Completos

### Python

```python
import requests
import uuid
from typing import Dict, Any

class SOSContadorAPI:
    def __init__(self, usuario: str, password: str, cuit_id: str):
        self.base_url = "https://api.sos-contador.com/api-comunidad"
        self.usuario = usuario
        self.password = password
        self.cuit_id = cuit_id
        self.cuit_token = None
        self._authenticate()
    
    def _authenticate(self):
        # Login
        response = requests.post(
            f"{self.base_url}/login",
            json={"usuario": self.usuario, "password": self.password}
        )
        user_token = response.json()["jwt"]
        
        # Get CUIT token
        response = requests.get(
            f"{self.base_url}/cuit/credentials/{self.cuit_id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        self.cuit_token = response.json()["jwt"]
    
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.cuit_token}",
            "Content-Type": "application/json"
        }
    
    def crear_venta(
        self,
        cliente_id: int,
        cliente_cuit: str,
        productos: list,
        punto_venta: int = 1,
        numero: int = 1,
        obtener_cae: bool = False
    ) -> Dict[str, Any]:
        """
        Crear una nueva venta/factura
        
        productos = [
            {"id": 772500, "cantidad": 7, "precio": 1550.00, "iva": 21.00}
        ]
        """
        # Calcular imputaciones
        neto = sum(p["cantidad"] * p["precio"] for p in productos)
        
        venta = {
            "idtipo_operacion": 2,
            "fecha": None,
            "idclipro": cliente_id,
            "cuitclipro": cliente_cuit,
            "idcuenta": None,
            "fcncnd": "F",
            "letra": "C",
            "puntoventa": punto_venta,
            "numero": numero,
            "numerohasta": None,
            "obtienecae": obtener_cae,
            "fechaiva": None,
            "idprovinciaiibb": None,
            "idcentrocosto": None,
            "memo": "Venta generada vía API",
            "referencia": f"REF-{uuid.uuid4().hex[:8]}",
            "descuento": 0,
            "uniqueid": str(uuid.uuid4()),
            "imputaciones": [
                {"i": "neto", "a": 0, "v": neto}
            ],
            "productos": [
                {
                    "id": p["id"],
                    "u": p["cantidad"],
                    "fc": 1,
                    "fu": p["precio"],
                    "fa": p["iva"]
                }
                for p in productos
            ]
        }
        
        response = requests.put(
            f"{self.base_url}/venta/0",
            json=venta,
            headers=self._headers()
        )
        return response.json()

# Uso
api = SOSContadorAPI(
    usuario="tu-email@ejemplo.com",
    password="tu-password",
    cuit_id="1665"
)

venta = api.crear_venta(
    cliente_id=1,
    cliente_cuit="50-00000001-6",
    productos=[
        {"id": 772500, "cantidad": 7, "precio": 1550.00, "iva": 21.00}
    ]
)
print(f"Venta creada: {venta}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

class SOSContadorAPI {
  constructor(usuario, password, cuitId) {
    this.baseUrl = 'https://api.sos-contador.com/api-comunidad';
    this.usuario = usuario;
    this.password = password;
    this.cuitId = cuitId;
    this.cuitToken = null;
  }

  async authenticate() {
    // Login
    const loginResponse = await axios.post(`${this.baseUrl}/login`, {
      usuario: this.usuario,
      password: this.password
    });
    const userToken = loginResponse.data.jwt;

    // Get CUIT token
    const cuitResponse = await axios.get(
      `${this.baseUrl}/cuit/credentials/${this.cuitId}`,
      { headers: { Authorization: `Bearer ${userToken}` } }
    );
    this.cuitToken = cuitResponse.data.jwt;
  }

  getHeaders() {
    return {
      'Authorization': `Bearer ${this.cuitToken}`,
      'Content-Type': 'application/json'
    };
  }

  async crearVenta(clienteId, clienteCuit, productos, options = {}) {
    if (!this.cuitToken) await this.authenticate();

    const {
      puntoVenta = 1,
      numero = 1,
      obtenerCAE = false
    } = options;

    // Calcular neto
    const neto = productos.reduce(
      (sum, p) => sum + (p.cantidad * p.precio), 
      0
    );

    const venta = {
      idtipo_operacion: 2,
      fecha: null,
      idclipro: clienteId,
      cuitclipro: clienteCuit,
      idcuenta: null,
      fcncnd: 'F',
      letra: 'C',
      puntoventa: puntoVenta,
      numero: numero,
      numerohasta: null,
      obtienecae: obtenerCAE,
      fechaiva: null,
      idprovinciaiibb: null,
      idcentrocosto: null,
      memo: 'Venta generada vía API',
      referencia: `REF-${Date.now()}`,
      descuento: 0,
      uniqueid: uuidv4(),
      imputaciones: [
        { i: 'neto', a: 0, v: neto }
      ],
      productos: productos.map(p => ({
        id: p.id,
        u: p.cantidad,
        fc: 1,
        fu: p.precio,
        fa: p.iva
      }))
    };

    const response = await axios.put(
      `${this.baseUrl}/venta/0`,
      venta,
      { headers: this.getHeaders() }
    );

    return response.data;
  }
}

// Uso
(async () => {
  const api = new SOSContadorAPI(
    'tu-email@ejemplo.com',
    'tu-password',
    '1665'
  );

  const venta = await api.crearVenta(
    1, // cliente_id
    '50-00000001-6', // cliente_cuit
    [
      { id: 772500, cantidad: 7, precio: 1550.00, iva: 21.00 }
    ]
  );

  console.log('Venta creada:', venta);
})();
```

---

## Notas para Implementación en IA

### Cuando crear ventas:
1. SIEMPRE generar UUID único para `uniqueid`
2. SIEMPRE calcular correctamente las imputaciones
3. VALIDAR que el cliente exista (GET /cliente/listado primero)
4. VALIDAR que los productos existan (GET /producto/listado primero)
5. USAR `numero` secuencial correcto

### Campos que NUNCA inventar:
- `idclipro`: Debe existir en la base de datos
- `cuitclipro`: Debe ser válido y existir
- `id` en productos: Debe existir en la base de datos
- `puntoventa`: Debe estar configurado

### Campos que se pueden calcular:
- `imputaciones`: Calcular desde productos
- `uniqueid`: Generar UUID
- `referencia`: Generar secuencial o descriptivo
- `fecha`: Usar null para hoy

---

**Última actualización:** Enero 2026
**Versión:** 1.0.0
