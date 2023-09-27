"""
密码加密
"""
import requests
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class PasswordEncryption:

    @staticmethod
    def get_public_key(environment):
        """
        组装公钥
        :return: 公钥
        """
        # 获取公钥
        get_public_key_response = requests.get(url=environment + "/api/sso/security/k").json()
        public_keys = get_public_key_response["data"]
        # 替换公钥字符"-"和"_"
        keys = public_keys.replace("-", "+")
        rsa_keys = keys.replace("_", "/")
        # 组成真正的公钥
        public_key = '-----BEGIN PUBLIC KEY-----\n' + rsa_keys + '\n-----END PUBLIC KEY-----'
        return public_key

    @staticmethod
    def encrpt(password, public_key):
        """
        密码加密
        :param password: 明文密码
        :param public_key: 组装好的公钥
        :return: 已加密的密码
        """
        rsa_key = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
        return cipher_text.decode()
