# Textcipher
Python module for text based cipher(s)

#### List of available ciphers:
* caesar Cipher (Shift Cipher)
* more coming soon.....

#### Example
* Caesar Cipher
```python

from Textcipher.Ciphers import Caesar

# Example message
msg = "A quick brown fox jumped over the lazy dog."
# Our key for encryption and decryption
key = 23

# the message, key and the mode must be passed to the instance of Caesar
# encryption or decryption depends on the 'mode' parameter. if mode is set True while encrypting then it must be
# set to False for decrypting and vice versa.

encrypt = Caesar(msg, key, True)
encrypted_msg = encrypt.crypto()
print(encrypted_msg)

decrypt = Caesar(encrypt.crypto(), key, False)
decrypted_msg = decrypt.crypto()
print(decrypted_msg)

```
