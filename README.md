# Simulador de Máquina de Turing

Proyecto 3 - Teoría de la Computación  

Nelson Escalante - 22046
Eliazar Canastuj - 23384

## Descripción

Simulador de Máquinas de Turing (MT) de una cinta que permite:
- Introducir la descripción formal de una MT mediante archivo YAML
- Simular entradas configuradas
- Obtener configuraciones finales sobre la cinta
- Indicar si el resultado es aceptado o rechazado
- Visualizar descripciones instantáneas (IDs) en cada paso

## Requisitos

- PyYAML

### Instalación de dependencias

```bash
pip install pyyaml
```

## Uso

### Ejecución básica

```bash
python turing_machine.py <archivo_configuracion.yaml>
```

### Ejemplos

**MT Reconocedora:**
```bash
python turing_machine.py recognizer_mt.yaml
```

**MT Alteradora:**
```bash
python turing_machine.py altering_mt.yaml
```

## Formato del archivo YAML

```yaml
mt:
  states: [q0, q1, q2, qf]              # Lista de estados
  input_alphabet: [a, b]                 # Alfabeto de entrada
  tape_alphabet: [a, b, B, X, Y]        # Alfabeto de cinta (incluye blancos)
  initial_state: q0                      # Estado inicial
  accept_states: [qf]                    # Estados de aceptación
  transitions:
    - state: q0                          # Estado origen
      read: [a]                          # Símbolo leído
      write: [X]                         # Símbolo a escribir
      move: R                            # Dirección (L/R/S)
      next: q1                           # Estado destino

inputs:
  - "aabb"                               # Cadenas a simular
  - "ab"
```

## Máquinas de Turing Implementadas

### 1. MT Reconocedora: Lenguaje {a^n b^n | n ≥ 1}

**Archivo:** `recognizer_mt.yaml`

**Descripción:** Reconoce cadenas con igual número de 'a's seguidas de igual número de 'b's.

**Algoritmo:**
1. Marca la primera 'a' con 'X'
2. Avanza hasta encontrar la primera 'b' y la marca con 'Y'
3. Regresa al inicio
4. Repite hasta procesar todos los símbolos
5. Verifica que todo esté marcado correctamente

**Casos de prueba incluidos:**
- ✓ Aceptadas: `aaabbb`, `aaaabbbb`, `aaaaabbbbb`, `aaaaaabbbbbb`
- ✗ Rechazadas: `aaabbbbb`, `aaaaabbb`, `ababab`, `bbbbaaa`

### 2. MT Alteradora: Intercambiar a ↔ b

**Archivo:** `altering_mt.yaml`

**Descripción:** Intercambia todas las 'a' por 'b' y todas las 'b' por 'a'.

**Algoritmo:**
1. Recorre la cinta de izquierda a derecha
2. Marca cada 'a' con 'X' y cada 'b' con 'Y'
3. Regresa al inicio
4. Reemplaza cada 'X' con 'b' y cada 'Y' con 'a'
5. Acepta la cadena alterada

**Casos de prueba incluidos:**
- `aaaaa` → `bbbbb`
- `bbbbb` → `aaaaa`
- `aaabbb` → `bbbaaa`
- `ababab` → `bababa`

## Arquitectura del Programa

### Componentes Principales

1. **Clase `TuringMachine`:**
   - Gestiona el estado completo de la MT
   - Mantiene la cinta, posición del cabezal y estado actual
   - Implementa la lógica de transición

2. **Estructura de Datos:**
   - **Cinta:** Lista de Python que se extiende dinámicamente
   - **Transiciones:** Diccionario con clave `(estado, símbolo)` para acceso O(1)
   - **Estados:** Conjuntos para verificación eficiente de aceptación

3. **Métodos Principales:**
   - `_parse_transitions()`: Convierte YAML a estructura interna
   - `_step()`: Ejecuta un paso de la MT
   - `simulate()`: Ejecuta la simulación completa
   - `_get_instantaneous_description()`: Genera IDs en formato estándar

### Formato de Descripción Instantánea (ID)

Las IDs se muestran en el formato: `w1[estado]w2`

Donde:
- `w1`: Contenido de la cinta a la izquierda del cabezal
- `[estado]`: Estado actual de la MT
- `w2`: Contenido desde la posición del cabezal hasta el final

**Ejemplo:**
```
Paso 0: [q0]aaabbb
Paso 1: X[q1]aabbb
Paso 2: Xa[q1]abbb
...
```

## Características Implementadas

✅ Parsing de archivos YAML  
✅ Simulación de MT de una cinta  
✅ Extensión dinámica de la cinta  
✅ Visualización de descripciones instantáneas  
✅ Detección de estados de aceptación/rechazo  
✅ Manejo de múltiples entradas  
✅ Protección contra loops infinitos (límite de pasos)  
✅ Soporte para movimiento L/R/S  
✅ Símbolos de cinta personalizables  

## Ejemplo de Salida

```
======================================================================
SIMULADOR DE MÁQUINA DE TURING
======================================================================

Estados: ['q0', 'q1', 'q2', 'q4', 'qaccept']
Alfabeto de entrada: ['a', 'b']
Alfabeto de cinta: ['a', 'b', 'B', 'X', 'Y']
Estado inicial: q0
Estados de aceptación: ['qaccept']
Número de transiciones: 12

======================================================================
Simulando entrada: 'aaabbb'
======================================================================

Descripciones Instantáneas:
----------------------------------------------------------------------
Paso 0: [q0]aaabbb
Paso 1: X[q1]aabbb
Paso 2: Xa[q1]abbb
Paso 3: Xaa[q1]bbb
Paso 4: XaY[q2]bb
...
----------------------------------------------------------------------
✓ CADENA ACEPTADA
Estado final: qaccept
Contenido final de la cinta: XXXYYYY
======================================================================
```