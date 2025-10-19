# -*- coding: utf-8 -*-
"""
xor_known_plaintext_finder.py by g3p3t0 & ChatGPT

Este script permite descifrar mensajes XOR:
 - Si conoces la clave (known_key), descifra directamente.
 - Si solo conoces un fragmento del texto plano (known_plaintext),
   deduce el keystream parcial, encuentra claves candidatas y prueba
   sus rotaciones.

"""

from typing import List, Optional
import base64, binascii


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes([a[i] ^ b[i % len(b)] for i in range(len(a))])


def from_hex_or_b64(data: str) -> bytes:
    data = data.strip()
    try:
        return binascii.unhexlify(data)
    except (binascii.Error, ValueError):
        return base64.b64decode(data)


def rotate_bytes(b: bytes, shift: int) -> bytes:
    n = len(b)
    if n == 0:
        return b
    s = shift % n
    return b[s:] + b[:s]


def find_smallest_period(fragment: bytes, max_period: Optional[int] = None) -> int:
    n = len(fragment)
    if n == 0:
        return 1
    max_p = n if max_period is None else min(n, max_period)
    for p in range(1, max_p + 1):
        if all(fragment[i] == fragment[i % p] for i in range(n)):
            return p
    return n


def deduce_keystream_fragment(cipher: bytes, known: bytes, offset: int) -> bytes:
    return bytes([cipher[offset + i] ^ known[i] for i in range(len(known))])


def candidate_keys_from_fragment(fragment: bytes, max_keylen: int = 40) -> List[bytes]:
    n = len(fragment)
    candidates = []
    max_p = min(max_keylen, n)
    for p in range(1, max_p + 1):
        if all(fragment[i] == fragment[i % p] for i in range(n)):
            candidates.append(fragment[:p])
    if not candidates:
        candidates.append(fragment)
    unique = []
    for c in candidates:
        if c not in unique:
            unique.append(c)
    return unique


# === CONFIGURACIÓN ===
cipher_hex = "1f5243145f1538434301502156171313112c43590f56215f021c480c6f116f16002640502d02070007040a546041530740097f0d5f445f3213001d5e043e11440540"
known_plaintext = b"Hola mundo desde la universidad"
known_key: bytes = b"S3cr3t_c0d3"  # si pones aquí la key ignora el known_plaintext
force_offset: Optional[int] = None # si conoces donde empieza el  known_plaintext en el cipher_hex
max_keylen_to_try = 16 # tamaño maximo de la key para deducir las posibles periocidades
preview_bytes = 200 # tamaño maximo de previsualicación por si el cipher_hex es muy grande
# ======================


def analyze(cipher_hex: str,
            known_plaintext: bytes = b"",
            force_offset: Optional[int] = None,
            max_keylen_to_try: int = 40,
            known_key: bytes = b"",
            preview_bytes: int = 200):
    cipher = from_hex_or_b64(cipher_hex)

    # Si ya tenemos la clave, desciframos directamente
    if known_key:
        print("Clave conocida: aplicando...")
        pt = xor_bytes(cipher, known_key)
        print(pt.decode(errors='replace'))
        return

    if not known_plaintext:
        print("No has proporcionado known_plaintext ni known_key. Nada que hacer.")
        return

    L = len(known_plaintext)
    offsets = [force_offset] if force_offset is not None else list(range(0, len(cipher) - L + 1))

    found_any = False
    for off in offsets:
        frag = deduce_keystream_fragment(cipher, known_plaintext, off)
        candidates = candidate_keys_from_fragment(frag, max_keylen=max_keylen_to_try)

        for k in candidates:
            for shift in range(len(k)):
                rot = rotate_bytes(k, shift)
                pt = xor_bytes(cipher, rot)
                texto = pt.decode(errors='replace')
                if known_plaintext.decode(errors='replace') in texto:
                    print("\n =) Posible clave:")
                    print(f"Offset: {off}, Clave rotada (rot={shift}): {rot!r}, hex={rot.hex()}")
                    print("Texto descifrado completo:")
                    print(texto)
                    found_any = True
    
    if not found_any:
        print("❌ No se encontró ninguna coincidencia con el known_plaintext.")


if __name__ == '__main__':
    analyze(cipher_hex, known_plaintext, force_offset, max_keylen_to_try, known_key, preview_bytes)

# FIN
