# SOS Contador API - Quick Reference

## Authentication Flow
```
1. POST /login → user_token
2. GET /cuit/credentials/{id} + user_token → cuit_token
3. Use cuit_token for all operations
```

## Base URL
```
https://api.sos-contador.com/api-comunidad
```

## Headers
```
Authorization: Bearer {CUIT_TOKEN}
Content-Type: application/json
```

---

## Quick Endpoints Reference

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/login` | Get user token | None |
| GET | `/cuit/credentials/{id}` | Get CUIT token | User Token |
| GET | `/cliente/listado` | List clients/providers | CUIT Token |
| GET | `/producto/listado` | List products | CUIT Token |
| PUT | `/producto/{id}` | Create/update product | CUIT Token |
| DELETE | `/producto/{id}` | Delete product | CUIT Token |
| GET | `/puntoventa/listado` | List sales points | CUIT Token |
| PUT | `/venta/{id}` | Create/update sale | CUIT Token |
| PUT | `/venta/archivar/{id}` | Archive sale | CUIT Token |
| DELETE | `/venta/{id}` | Delete sale | CUIT Token |

---

## Quick Examples

### Login
```bash
curl -X POST https://api.sos-contador.com/api-comunidad/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"email@example.com","password":"pass"}'
```

### Get CUIT Token
```bash
curl https://api.sos-contador.com/api-comunidad/cuit/credentials/1665 \
  -H "Authorization: Bearer {USER_TOKEN}"
```

### List Clients
```bash
curl "https://api.sos-contador.com/api-comunidad/cliente/listado?cliente=true&registros=10" \
  -H "Authorization: Bearer {CUIT_TOKEN}"
```

### Create Sale (Minimal)
```json
PUT /venta/0
{
  "idtipo_operacion": 2,
  "idclipro": 1,
  "cuitclipro": "50-00000001-6",
  "fcncnd": "F",
  "letra": "C",
  "puntoventa": 1,
  "numero": 1,
  "obtienecae": false,
  "memo": "Sale description",
  "referencia": "REF-001",
  "descuento": 0,
  "uniqueid": "UUID-HERE",
  "imputaciones": [{"i": "neto", "a": 0, "v": 1000.00}],
  "productos": [{"id": 123, "u": 1, "fc": 1, "fu": 1000.00, "fa": 21.00}]
}
```

---

## Field Reference

### Sale (venta) Required Fields
- `idtipo_operacion`: Operation type ID (int)
- `idclipro`: Client/provider ID (int)
- `cuitclipro`: Client/provider CUIT (string: "XX-XXXXXXXX-X")
- `fcncnd`: Document type ("F"|"NC"|"ND")
- `letra`: Invoice type ("A"|"B"|"C")
- `puntoventa`: Sales point number (int)
- `numero`: Document number (int)
- `uniqueid`: UUID for idempotency (string)
- `imputaciones`: Array of imputations
- `productos`: Array of products

### Product (producto) in Sale
- `id`: Product ID (int)
- `u`: Units/quantity (number)
- `fc`: Conversion factor (number, usually 1)
- `fu`: Unit price (number)
- `fa`: VAT rate (number, e.g., 21)

### Imputation
- `i`: Type ("neto"|"iva"|others)
- `a`: Rate (number, 0 for "neto")
- `v`: Value (number)

---

## Important Notes for AI

1. **ALWAYS** generate unique UUID for `uniqueid`
2. **VALIDATE** client exists before creating sale
3. **VALIDATE** products exist before creating sale
4. **CALCULATE** imputations from products
5. **USE** null for `fecha` to use current date
6. **USE** 0 as ID to create new resource
7. **CUIT format**: XX-XXXXXXXX-X (with dashes)

---

## Python Quick Start

```python
import requests
import uuid

base = "https://api.sos-contador.com/api-comunidad"

# 1. Login
r = requests.post(f"{base}/login", json={"usuario": "...", "password": "..."})
user_token = r.json()["jwt"]

# 2. Get CUIT token
r = requests.get(f"{base}/cuit/credentials/1665", 
                 headers={"Authorization": f"Bearer {user_token}"})
cuit_token = r.json()["jwt"]

# 3. Use CUIT token
headers = {"Authorization": f"Bearer {cuit_token}", "Content-Type": "application/json"}

# List clients
r = requests.get(f"{base}/cliente/listado?cliente=true", headers=headers)
clients = r.json()

# Create sale
sale = {
    "idtipo_operacion": 2,
    "idclipro": 1,
    "cuitclipro": "50-00000001-6",
    "fcncnd": "F",
    "letra": "C",
    "puntoventa": 1,
    "numero": 1,
    "obtienecae": False,
    "memo": "Test",
    "referencia": "REF-001",
    "descuento": 0,
    "uniqueid": str(uuid.uuid4()),
    "imputaciones": [{"i": "neto", "a": 0, "v": 1000}],
    "productos": [{"id": 123, "u": 1, "fc": 1, "fu": 1000, "fa": 21}]
}
r = requests.put(f"{base}/venta/0", json=sale, headers=headers)
```

---

## Common Patterns

### Create product, then sell it
```python
# 1. Create product
product = {
    "codigo": "PROD001",
    "nombre": "My Product",
    "precio": 1000,
    "alicuota_iva": 21
}
r = requests.put(f"{base}/producto/0", json=product, headers=headers)
product_id = r.json()["id"]

# 2. Use in sale
sale["productos"] = [{"id": product_id, "u": 1, "fc": 1, "fu": 1000, "fa": 21}]
requests.put(f"{base}/venta/0", json=sale, headers=headers)
```

### Calculate VAT
```python
net = 1000.00
vat_rate = 21.00
vat_amount = net * (vat_rate / 100)
total = net + vat_amount

imputaciones = [
    {"i": "neto", "a": 0, "v": net},
    {"i": "iva", "a": vat_rate, "v": vat_amount}
]
```

---

## Error Handling

```python
try:
    r = requests.put(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        # Re-authenticate
        pass
    elif e.response.status_code == 404:
        # Resource not found
        pass
    else:
        # Other error
        raise
```

---

## Validation Checklist

Before creating a sale:
- [ ] Client ID exists (check with GET /cliente/listado)
- [ ] Client CUIT is valid format
- [ ] All product IDs exist (check with GET /producto/listado)
- [ ] Sales point exists (check with GET /puntoventa/listado)
- [ ] Document number is sequential
- [ ] UUID is unique
- [ ] Imputations are calculated correctly
- [ ] All required fields present

---

**For complete documentation see:** [API_DOCUMENTATION_AI.md](./API_DOCUMENTATION_AI.md)
