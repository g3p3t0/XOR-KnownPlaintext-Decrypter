# XOR Known-Plaintext Decrypter

## Descripción

Este proyecto es un script en Python para descifrar mensajes cifrados con XOR. Permite deducir la clave o el keystream a partir de un fragmento conocido del texto plano (known plaintext) y también admite la inserción de una clave conocida directamente.

El script soporta:

* Ciphertext en formato hexadecimal o Base64.
* Known plaintext en cualquier posición del mensaje.
* Claves más cortas que el fragmento de texto conocido.
* Rotaciones cíclicas de la clave para probar diferentes alineamientos.
* Filtrado automático para mostrar únicamente descifrados que contengan el texto conocido.

## Características

* **Clave conocida:** Si ya conoces la clave, el script descifra directamente sin necesidad del texto conocido.
* **Texto conocido:** Deduce la clave a partir de un fragmento de texto conocido y prueba todas sus rotaciones, mostrando solo las coincidencias.
* **Rotaciones de la clave:** Genera todas las rotaciones posibles de la clave candidata, útil si no se conoce el alineamiento exacto.
* **Filtros de coincidencia:** Muestra únicamente los resultados que contienen el known plaintext.

## Configuración

Edita la sección de configuración en el script:

```python
cipher_hex = "<tu_ciphertext_aquí>"
known_plaintext = b"<tu_texto_conocido_aquí>"
known_key = b""  
force_offset = None  
max_keylen_to_try = 16
preview_bytes = 200  
```

* `cipher_hex`: Texto cifrado en hexadecimal o Base64.
* `known_plaintext`: Fragmento del texto que conoces.
* `known_key`: Clave completa si ya la conoces.
* `force_offset`: Indica la posición donde comienza el known plaintext en el ciphertext.
* `max_keylen_to_try`: Longitud máxima de la clave a considerar al deducirla.
* `preview_bytes`: Cantidad de bytes a mostrar del descifrado.

## Uso

Ejecuta el script en Python 3:

```bash
python xor_known_plaintext_finder.py
```

El script mostrará:

* La clave deducida o usada.
* El texto descifrado completo si contiene el known plaintext.
* Rotaciones de la clave y su correspondiente descifrado (si aplica).

## Ejemplo de salida

```
✅ Coincidencia encontrada:
Offset: 0, Clave rotada (rot=0): b'secret', hex=736563726574
Texto descifrado completo:
Hola mundo...
```

## Requisitos

* Python 3.x

No requiere librerías externas.

## ------------------------------------------------------------------

Este proyecto fue desarrollado con la ayuda de IA para algunas partes del código. =)

