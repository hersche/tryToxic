from lib.header import *
import base64
import sys
from Crypto.Hash import SHA512
#'cryptoclass - cm = cryptoMeta'
class cm:
    def __init__(self, pyCryptoModule,  key=""):
        self.key = key
        self.mod = pyCryptoModule
        if self.mod is not None:
          self.name = self.mod.__name__[14:]
        else:
          self.name = "None"
        if self.key != "encryptionInit" and self.key != "":
            self.setKey(self.key)    
        logger.debug("|Crypt| Init cm/cryptoMeta with module "+self.name)
        from Crypto import Random as rand
        self.rand = rand

    def setKey(self, key):
        logger.error(key + " len "+str(len(key)))
        hash = SHA512.new(bytes(key,'ascii'))
        self.key = hash.hexdigest()
        if self.name == "CAST" or self.name=="IDEA":
           self.key = self.key[0:16]
        elif self.name == "Blowfish" or self.name == "ARC2" or self.name == "ARC4":
           if len(self.key) < self.mod.block_size:
             rest = (self.mod.block_size *2) - len(self.key)
           else:
             rest = 16
           while rest !=0:
             rest -=1
             self.key += "."
        elif self.name == "AES" or self.name == "XOR":
           self.key = self.key[0:32]
        elif self.name == "DES3":
          self.key = self.key[0:24]
        logger.error(self.key + " len "+str(len(self.key)))
        return self.key

    def encrypt(self, rawMessage):
      try:
        message=str(rawMessage)
        if self.mod == None:
            return rawMessage
        iv = self.rand.new().read(self.mod.block_size)
        if self.name == "XOR" or self.name == "ARC4":
          cipher = self.mod.new(self.key)          
        else:
          cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)
        mLen = len(message)
        if mLen > self.mod.block_size:
            rest = self.mod.block_size-(mLen% self.mod.block_size)
        else:
            rest = self.mod.block_size - mLen
        tmp = ""
        while rest != 0:
            rest -=1
            tmp += " "
        eMessage = message+tmp
        #print(eMessage+str(len(eMessage)))
        t =  base64.b64encode(iv + cipher.encrypt(eMessage))
        return t
      except Exception as e:
        logger.error("|Crypt| Encryptionerror: "+ str(e.args[0]))
    def decrypt(self, encryptedMessage):
        try:
          if self.mod == None:
              return encryptedMessage
          if encryptedMessage is None:
              return ""
          tDec = base64.b64decode(encryptedMessage)
          iv = tDec[:self.mod.block_size]
          if self.name == "XOR" or self.name == "ARC4":
            cipher = self.mod.new(self.key)          
          else:
            cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)
          clearText = str(cipher.decrypt(tDec[self.mod.block_size:]))
          #workAround for b'-signed floats and ints..
          if clearText[0:2] == "b'":
              clearText = clearText[2:-1]
          else:
              clearText = clearText[0:-1]
          return clearText.rstrip()
        except Exception as e:
          logger.error("|Crypt| Decryptionerror: "+ str(e.args[0]))

#static crypt manager
class scm:
    #oldMod - self.encryptionObject,
    @staticmethod
    def migrateEncryptionData(newCryptManager, toxMessagesHandler):
      logger.error("|Crypt|Start migrateEncryptionData")
      toxMessagesHandler.updateMessages()
      toxMessagesHandler.eo=newCryptManager
      toxMessagesHandler.saveAllMessages()
          

    @staticmethod
    def getMod(configValue):
        configValue = configValue.lower()
        try:
            if configValue == "1" or configValue == "cast":
                if("CAST" not in sys.modules):
                    from Crypto.Cipher import CAST
                return CAST
            elif configValue == "2"  or configValue == "blowfish":
                if("Blowfish" not in sys.modules):
                    from Crypto.Cipher import Blowfish
                return Blowfish
            elif configValue == "3"  or configValue == "des3":
                if("DES3" not in sys.modules):
                    from Crypto.Cipher import DES3
                return DES3
            elif configValue == "4"  or configValue == "arc4":
                if("ARC4" not in sys.modules):
                    from Crypto.Cipher import ARC4
                return ARC4
            elif configValue == "5"  or configValue == "xor":
                if("XOR" not in sys.modules):
                    from Crypto.Cipher import XOR
                return XOR
            elif configValue == "6"  or configValue == "aes":
                if("AES" not in sys.modules):
                    from Crypto.Cipher import AES
                return AES
            elif configValue == "7"  or configValue == "arc2":
                if("ARC2" not in sys.modules):
                    from Crypto.Cipher import ARC2
                return ARC2
            else:
                return None
        except  Exception as e:
            logger.error("Could not find pycrypt-Module. Please install it via apt-get install python3-crypto")
