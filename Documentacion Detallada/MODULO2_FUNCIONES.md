# 🛡️ Módulo 2: Seguridad y Reportes

## 🔐 Encriptación para Principiantes

### ¿Cómo funciona?
Imagina un candado digital:
1. Tu documento es el tesoro
2. La clave es la combinación secreta
3. Encriptar = Guardar el tesoro con candado
4. Desencriptar = Abrir con la combinación correcta

### 🔑 Explicación Detallada de XOR
La encriptación XOR funciona como un interruptor de luz:
1. Cada letra de tu mensaje se convierte en número (código ASCII)
2. Cada número se combina con la clave usando XOR (⊕)
   - 0 ⊕ 0 = 0
   - 0 ⊕ 1 = 1  
   - 1 ⊕ 0 = 1
   - 1 ⊕ 1 = 0
3. Para desencriptar, aplicas XOR con la misma clave

**Ejemplo Práctico**:
```python
# Supongamos que tu clave es "ABC"
clave = generar_clave()  # "ABC"

# Encriptar
texto_original = "Hola"
texto_encriptado = xor_encrypt_decrypt(texto_original, clave)  # Resultado inlegible

# Desencriptar 
texto_recuperado = xor_encrypt_decrypt(texto_encriptado, clave)  # "Hola" nuevamente
```

### 🔐 Sistema de Llaves Maestras
El sistema usa una llave maestra compartida pero protegida:

1. **Primer Usuario (Admin)**:
   - Se genera una llave aleatoria segura
   - Se encripta usando la contraseña del admin
   - Se guarda la versión encriptada en la base de datos

2. **Usuarios Nuevos**:
   - El admin desencripta la llave (usando su contraseña)
   - Vuelve a encriptarla con la contraseña del nuevo usuario
   - Guarda esta nueva versión encriptada

**Beneficios**:
- Todos acceden a la misma llave maestra
- Cada usuario solo puede desencriptarla con su contraseña
- No se almacenan llaves en texto plano

**Ejemplo Visual**:
```
Llave Maestra Real: ABC123
Encriptada para Admin: X7Z9 (usando su contraseña)
Encriptada para Usuario2: P4Q8 (usando su contraseña)  
```

### 📋 Lista de Funciones Clave
1. `generar_clave()` - Crea una clave aleatoria segura
2. `xor_encrypt_decrypt()` - Encripta/desencripta texto
3. `almacenar_pdf()` - Guarda PDFs encriptados  
4. `descargar_pdf()` - Recupera PDFs originales
5. `generar_reporte_proyecto()` - Crea reporte completo
6. `generar_reporte_rev0()` - Genera reporte de documentos finales
7. `manejar_llave_maestra()` - Gestiona el ciclo de vida de la llave

## 📁 Cómo Trabajamos con Archivos

### Proceso de Encriptación:
1. 📄 **Paso 1:** Lee el PDF original como datos binarios
2. 🔐 **Paso 2:** Aplica la operación XOR con tu clave secreta
3. 💾 **Paso 3:** Guarda el resultado como archivo .enc

### Proceso de Desencriptación:
1. 🔍 **Paso 1:** Abre el archivo .enc
2. 🔓 **Paso 2:** Aplica XOR con la misma clave usada para encriptar
3. 📤 **Paso 3:** Recupera el PDF original listo para usar

## 📊 Generación de Reportes

### Tipos de Reportes:
1. **Reporte Completo** - Todos los documentos del proyecto
   - Incluye: disciplinas, códigos, revisiones, estados
   - Formato profesional con gráficos y tablas

2. **Reporte Rev 0** - Documentos finales aprobados
   - (Nota: En este sistema, Rev 0 indica versión final)
   - Muestra: porcentaje de completitud
   - Detalla fechas de emisión/recepción

**Ejemplo Práctico**:
```python
# Reporte completo (todos los documentos)
generar_reporte_proyecto(
    proyecto_id=5,
    output_path="informes/"
)

# Reporte de documentos finales (Rev 0)
generar_reporte_rev0(
    proyecto_id=5, 
    output_path="informes/"
)
```

## ⚠️ Consideraciones de Seguridad
- XOR ofrece seguridad básica
- Planes de migrar a AES-256 en futuras versiones
- Las claves deben guardarse de forma segura

## 🔄 Flujo Completo
1. Generar clave → 2. Encriptar al guardar → 3. Desencriptar al descargar

## 🛠️ Ejemplo Práctico
```python
clave = generar_clave()
pdf_enc = almacenar_pdf("documento.pdf", clave)
pdf_original = descargar_pdf(pdf_enc, clave)
