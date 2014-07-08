import random
import unittest
from Crypto.Hash import MD5
from lib.cryptClass import *

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mod = scm.getMod("3")
        self.cm = cm(self.mod, "Password")
    def test_name(self):
        self.assertEqual(self.mod.__name__[14:], "DES3")
    def test_enDecryptText(self):
        encrypted = self.cm.encrypt("Test")
        decrypted =self.cm.decrypt(encrypted)
        self.assertEqual("Test", decrypted)
    def test_enDecryptInt(self):
        encrypted = self.cm.encrypt(34)
        decrypted =self.cm.decrypt(encrypted)
        self.assertEqual(34, int(decrypted))
    def test_enDecryptFloat(self):
        encrypted = self.cm.encrypt(3.14)
        decrypted =self.cm.decrypt(encrypted)
        self.assertEqual(3.14, float(decrypted))
        
    def test_enDecryptFile(self):
        # 1. fill random in file
        # 2. md5sum from file
        # 3. encrypt
        # 4. decrypt
        # 5. compare a new md5 against the old one
        # 6. pass it!
        pass
    


if __name__ == '__main__':
    unittest.main()