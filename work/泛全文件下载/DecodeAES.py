from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import base64




def aes_ecb_decrypt(ciphertext, key):
    """
    使用AES-128-ECB模式解密密文，密文格式为Base64，解密后使用UTF-8编码。

    :param ciphertext: 要解密的密文，Base64编码的字符串
    :param key: 用于AES解密的密钥，长度为128 bits（16字符）
    :return: 解密后的字符串，使用UTF-8编码
    """
    # Base64解码
    ciphertext_bytes = base64.b64decode(ciphertext)

    # 创建AES解密器
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)

    # 解密并去除PKCS7填充
    decrypted_bytes = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)

    # 返回解密后的字符串，使用UTF-8编码
    return decrypted_bytes.decode('utf-8')


# 示例调用
if __name__ == '__main__':
    encrypted_text = "fukCqYgn0IEIQtKCOL3NHNXExNMDXj3ZYC9BtNtzwWmy9vzPPzeIWiFnH2UmkJ8vHk6qOOKEHJOPHCOCA13xshl7itTEzaLus44VWACuoie1XQWbBRas0+lHj7UADfnhaJrP5g/0lSHACovKGlQScHkJLtUyf6POnV0S4uovfbpKAXREz8oex5C6oY3nEvll78N6bDF2DKK+KzzfIcl34RwAGOExr/YLhrRAkqntiQINwlTTTBDCeajAbsSupyHLX8cKIXYulxM0QoXtF7zsqhKRmveOq5mFCvI792krxpA8tiG8f7koKbfHa+Auwa6W"
    # 这是一个示例的Base64编码的密文，你可以替换为实际的密文
    key = "THAF0lD*1Lq#GA3#"

    try:
        decrypted_text = aes_ecb_decrypt(encrypted_text, key)
        print(f"解密后的文本: {decrypted_text}")
    except Exception as e:
        print(f"解密时出错: {e}")
