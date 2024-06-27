import base64
from django.contrib.auth import get_user_model
from io import BytesIO
import sys
from django.core.files import File
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from base64 import  b64decode, b64encode
from cryptography.hazmat.backends import default_backend
from uuid import uuid4
from django.contrib.auth import get_user_model
import base64
from io import BytesIO
from django.core.files import File
import sys

class DataEncryption():

    def encrypt(key, plaintext):
        key                 = key.encode('utf-8')
        iv                  = os.urandom(16)
        cipher              = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor           = cipher.encryptor()
        padder              = PKCS7(128).padder()
        padded_plaintext    = padder.update(plaintext.encode("utf-8")) + padder.finalize()
        ciphertext          = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode("utf-8")

    def decrypt(key, ciphertext):
        key               = key.encode('utf-8')
        ciphertext        = b64decode(ciphertext.encode("utf-8"))
        iv                = ciphertext[:16]
        ciphertext        = ciphertext[16:]
        cipher            = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor         = cipher.decryptor()
        decrypted_padded  = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder          = PKCS7(128).unpadder()
        decrypted_plaintext_padded = unpadder.update(decrypted_padded) + unpadder.finalize()
        plaintext = decrypted_plaintext_padded.decode("utf-8")
        return plaintext
    
def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def get_token_user_or_none(request):
    User = get_user_model()
    try:
        instance = User.objects.get(id=request.user.id)
    except Exception:
        instance = None
    finally:
        return instance
    
class ConvertBase64File():
    
    def base64_to_file(self,value):
        try:
            format, base64_data = value.split(';base64,')
            decoded_data = base64.b64decode(base64_data)
            stream = BytesIO()
            stream.write(decoded_data)
            stream.seek(0)
            return File(stream)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return None
        
        
    def base64_file_extension(self,value):
        try:
            format, base64_data = value.split(';base64,')
            media_type = format.split('/')[1]
            base64_extension = media_type.split('+')[0] 
            return base64_extension

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return None
