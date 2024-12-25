"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import re
from base64 import b64encode
from urllib.parse import urlparse, urlunparse

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


def encrypt_aes_ecb(data: str, key: str) -> str:
    """Encrypt aes ecb."""
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key.encode("utf-8")), modes.ECB(), backend=backend)  # noqa: S305
    encryptor = cipher.encryptor()
    padder = PKCS7(16 * 8).padder()
    padded_data = padder.update(data.encode("utf-8")) + padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return b64encode(ct).decode("utf-8")


def modify_url(url: str) -> str:
    """Modify url."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")
    if len(path_parts) < 2:
        return url
    last_part = path_parts[-1].split(".")
    if len(last_part) != 2 or not re.match(r"^\d+$", last_part[0]) or last_part[1] != "jhtml":
        return url
    encrypted_part = encrypt_aes_ecb(last_part[0], "qnbyzzwmdgghmcnm")
    encrypted_part = encrypted_part.replace("/", "^")[:-2]
    new_last_part = f"{encrypted_part}.{last_part[1]}"
    path_parts[-1] = new_last_part
    new_path = "/".join(path_parts)
    modified_url = parsed_url._replace(path=new_path)
    return urlunparse(modified_url)
