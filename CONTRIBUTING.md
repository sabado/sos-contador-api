# Contribuir a la Documentación

¡Gracias por contribuir! Esta documentación es comunitaria y cualquier ayuda es bienvenida.

## 🎯 Qué necesitamos

- **Nuevos endpoints** no documentados
- **Ejemplos de uso** reales
- **Correcciones** de errores
- **Mejoras** en la claridad
- **Traducciones** a otros idiomas

## 📝 Cómo agregar un nuevo endpoint

### 1. Actualizar `API_DOCUMENTATION_AI.md`

Agregá la documentación completa del endpoint siguiendo este formato:

```markdown
### MÉTODO /ruta/del/endpoint

Descripción breve.

**Endpoint:** `MÉTODO /ruta/del/endpoint`

```http
MÉTODO https://api.sos-contador.com/api-comunidad/ruta/del/endpoint
Authorization: Bearer {TOKEN_DE_CUIT}
Content-Type: application/json
```

**Path Parameters:**
- `param` (tipo): Descripción

**Query Parameters:**
- `param` (tipo): Descripción

**Request Body:**
```json
{
  "campo": "valor"
}
```

**Response:**
```json
{
  "resultado": "valor"
}
```

**Ejemplo Python:**
```python
# código de ejemplo
```
```

### 2. Actualizar `QUICK_REFERENCE.md`

Agregá una línea en la tabla:

```markdown
| MÉTODO | `/ruta/endpoint` | Descripción | CUIT Token |
```

### 3. Actualizar `openapi.yaml`

Agregá el path en la sección `paths:`:

```yaml
  /ruta/endpoint:
    metodo:
      tags:
        - tag
      summary: Resumen
      description: Descripción
      operationId: operationId
      security:
        - bearerAuthCuit: []
      # ... resto de la spec
```

### 4. Agregar ejemplo si es complejo

Si el endpoint es complejo, agregá un ejemplo en `examples/python/` o `examples/javascript/`

## 🧪 Validar cambios

Antes de hacer PR:

1. **Verificar formato Markdown:**
   ```bash
   # Previsualizar en VS Code o GitHub
   ```

2. **Validar OpenAPI:**
   ```bash
   # Usar https://editor.swagger.io/
   # O instalar validator:
   npm install -g @apidevtools/swagger-cli
   swagger-cli validate openapi.yaml
   ```

3. **Probar ejemplos de código:**
   ```bash
   python examples/python/nuevo_ejemplo.py
   ```

## 📋 Checklist para PR

- [ ] Endpoint documentado en `API_DOCUMENTATION_AI.md`
- [ ] Entrada agregada en `QUICK_REFERENCE.md`
- [ ] Path agregado en `openapi.yaml`
- [ ] Ejemplos de código incluidos (si aplica)
- [ ] OpenAPI validado
- [ ] Código probado (si aplica)
- [ ] Descripción clara del PR

## 🔍 Encontrar nuevos endpoints

### Método 1: Scraping de Postman
```bash
python scraper_sos_completo.py
# Revisar archivos generados
```

### Método 2: Network tab del navegador
1. Abrir DevTools (F12) en SOS Contador
2. Tab Network
3. Realizar acciones en la plataforma
4. Ver requests a `api.sos-contador.com`

### Método 3: Consultar con SOS Contador
Email: soporte@sos-contador.com
Tel: 011 5263-0200

## 💡 Tips para documentación clara

1. **Ser específico:**
   ❌ "El endpoint devuelve datos"
   ✅ "El endpoint devuelve un array de objetos Cliente con id, nombre y CUIT"

2. **Incluir ejemplos reales:**
   - Usar valores realistas
   - Mostrar responses completos
   - Incluir casos de error

3. **Documentar para IA:**
   - Especificar tipos de datos
   - Marcar campos requeridos
   - Indicar valores por defecto
   - Explicar validaciones

4. **Mantener consistencia:**
   - Seguir el formato existente
   - Usar misma terminología
   - Mantener estilo de código

## 🚫 Qué NO hacer

- ❌ Commitear credenciales reales
- ❌ Copiar/pegar documentación de otros sin permiso
- ❌ Agregar endpoints sin verificar que funcionen
- ❌ Romper el formato OpenAPI

## 📬 Preguntas

¿Dudas? Abrí un Issue antes de empezar el PR.

## 📄 Licencia

Al contribuir, aceptás que tu contribución se licencie bajo MIT License.

---

**¡Gracias por hacer esta documentación mejor! 🎉**
