"""cryptography 库最小示例：对称加密、口令哈希、非对称签名。

运行: python examples/cryptography_demo.py
"""

import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def symmetric_demo(message: str) -> bytes:
    """对称加密：同一把密钥加解密。"""
    key = Fernet.generate_key()
    cipher = Fernet(key)
    token = cipher.encrypt(message.encode())
    assert cipher.decrypt(token).decode() == message
    return key


def password_hash(password: str) -> tuple[bytes, bytes]:
    """口令哈希：存盐和结果，绝不存明文。"""
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    return salt, kdf.derive(password.encode())


def verify_password(password: str, salt: bytes, expected: bytes) -> bool:
    """校验口令：用同一派生参数重算并定长比较。"""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    try:
        kdf.verify(password.encode(), expected)
        return True
    except Exception:
        return False


def signature_demo(message: str) -> None:
    """非对称签名：私钥签名，公钥验签。"""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    signature = private_key.sign(message.encode())
    public_key.verify(signature, message.encode())  # 验签失败会抛 InvalidSignature
    print(f"签名: {base64.b64encode(signature).decode()[:32]}...")


if __name__ == "__main__":
    text = "攻击计划：今晚吃火锅"

    key = symmetric_demo(text)
    print(f"Fernet 密钥(需妥善保存): {key.decode()}")

    salt, digest = password_hash("hunter2")
    assert verify_password("hunter2", salt, digest)
    assert not verify_password("wrong", salt, digest)
    print(f"口令哈希: {digest.hex()[:32]}...")

    signature_demo(text)
    print("✅ 全部自检通过")
