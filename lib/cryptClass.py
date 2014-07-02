from lib.header import *
import base64
import sys, os, mmap
from Crypto.Hash import SHA512

class cm:
    """
    Crypto-Meta-Class, should be able to do any symetric encryption and decryption for any text-data.
    """
    def __init__(self, pyCryptoModule, key=""):
      """
      Keywords:
      pyCryptoModule -- get a valid cryptoModule by scm.getMod
      key -- is the passPhrase or also password
      """
      self.key = key
      self.mod = pyCryptoModule
      if self.mod is not None:
        self.name = self.mod.__name__[14:]
      else:
        self.name = "None"
      if self.key != "encryptionInit" and self.key != "":
          self.setKey(self.key)
      logger.debug(tr("|Crypt| Init cm/cryptoMeta with module ") + self.name)
      from Crypto import Random as rand
      self.rand = rand

    def setKey(self, key):
      """
      self.setKey does hash the password and shortens the hash to max of algorithm's key-block_size.
      return new Key
      """
      if len(key) is not 0:
        hash = SHA512.new(bytes(key, 'ascii'))
        self.key = hash.hexdigest()
        if self.name == "CAST" or self.name == "IDEA":
          self.key = self.key[0:16]
        elif self.name == "ARC2":
          self.key = self.key[0:127]
        elif self.name == "Blowfish"  or self.name == "ARC4":
          self.key = self.key[0:56]
        elif self.name == "AES" or self.name == "XOR":
          self.key = self.key[0:32]
        elif self.name == "DES3":
          self.key = self.key[0:24]
        return self.key
      else:
        self.mod = None
        self.name = "None"

    def encrypt(self, rawMessage):
      """
      Encrypt plaintext.
      return encryptedMessage
      """
      try:
        message = str(rawMessage)
        if self.mod == None and self.name == "None" and self.key != "encryptionInit":
            return message
        iv = self.rand.new().read(self.mod.block_size)
        if self.name == "XOR" or self.name == "ARC4":
          cipher = self.mod.new(self.key)
        else:
          cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)
        mLen = len(message)
        if mLen > self.mod.block_size:
            rest = self.mod.block_size - (mLen % self.mod.block_size)
        else:
            rest = self.mod.block_size - mLen
        tmp = ""
        while rest != 0:
            rest -= 1
            tmp += "."
        eMessage = message + tmp
        t = base64.b64encode(iv + cipher.encrypt(eMessage))
        return t
      except Exception as e:
        logger.error(tr("|Crypt| Encryptionerror: ") + str(e.args[0]) + tr(" Message ") + str(rawMessage))
    def decrypt(self, encryptedMessage):
        """
        Decrypt encrypted text.
        return clearText
        """
        try:
          if encryptedMessage is None:
              return ""
          if self.mod != None and self.name != "None" and self.key != "encryptionInit":
            tDec = base64.b64decode(encryptedMessage)
            iv = tDec[:self.mod.block_size]
            # logger.error("mod-value: "+str(self.name)+" block-lenght: "+str(self.mod.block_size))
            # logger.error("iv-value: "+str(iv)+" iv-lenght: "+len(str(iv)))
            if self.name == "XOR" or self.name == "ARC4":
              cipher = self.mod.new(self.key)
            else:
              cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)

            clearText = str(cipher.decrypt(tDec[self.mod.block_size:]))
            # workAround for b'-signed floats and ints..
            if clearText[0:2] == "b'":
                clearText = clearText[2:-1]
            else:
                clearText = clearText[0:-1]
            return clearText.rstrip(".")
          else:
            return encryptedMessage
        except Exception as e:
          logger.error(tr("|Crypt| Decryptionerror: ") + str(e.args[0]))
        
    def encryptFile(self,FileName):
      """
      Encrypt plain-file.
      return none, but lets a encrypted file on your hd
      """
      try:
        if self.mod == None and self.name == "None" and self.key != "encryptionInit":
            return open(FileName, "r")
        iv = self.key[:self.mod.block_size]
        if self.name == "XOR" or self.name == "ARC4":
          cipher = self.mod.new(self.key)
        else:
          cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)
        print(FileName)
        inputFile = open(FileName)
        print("blub")
        outputFile = open(FileName+".encryptionTmp", "wb")
        print("created")
        bs = self.mod.block_size
        finished = False
        while not finished:
            chunk = inputFile.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                    padding_length = (bs - len(chunk) % bs) or bs
                    chunk += padding_length * chr(padding_length) # changed right side to str.encode(...)
                    finished = True
            outputFile.write(cipher.encrypt(chunk))
        #t = base64.b64encode(iv + cipher.encrypt(eMessage))
        #os.remove(Filename)
        #os.rename(FileName+".encryptionTmp",FileName)
      except Exception as e:
        logger.error(tr("|Crypt| FileEncryptionerror: ") + str(e.args[0]) + tr(" Message "))
    def decryptFile(self, encryptedFileName):
        """
        Decrypt encrypted file.
        return clearText
        """
        try:
          if self.mod != None and self.name != "None" and self.key != "encryptionInit":
            inputFile = open(encryptedFileName, "r")
            iv = self.key[:self.mod.block_size]
            bs = self.mod.block_size
            if self.name == "XOR" or self.name == "ARC4":
              cipher = self.mod.new(self.key)
            else:
              cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)
            next_chunk = ''
            finished = False
            decryptedContent = ''
            outputFile = mmap.mmap(-1, 13)
            while not finished:
                chunk, next_chunk = str(next_chunk), str(cipher.decrypt(inputFile.read(1024 * bs)))
                if len(next_chunk) == 0:
                    padding_length = chunk[-1] # removed ord(...) as unnecessary
                    chunk = chunk[:-padding_length]
                    finished = True
                #print(str(bytes(x for x in chunk)))
                outputFile.write(bytes(x for x in chunk))
            return outputFile
        except Exception as e:
          logger.error(tr("|Crypt| FileDecryptionerror: ") + str(e.args))


class scm:
  """
  Static crypt manager, just contains static methods in context to encryption/decryption-stuff.
  """
  @staticmethod
  def migrateEncryptionData(newCryptManager, toxMessagesHandler):
    """
    In this case, there are just messages to migrate..
    return None
    """
    logger.debug("|Crypt|Start migrateEncryptionData")
    toxMessagesHandler.saveAllMessages(newCryptManager)
    toxMessagesHandler.eo = newCryptManager
    toxMessagesHandler.updateMessages()


  @staticmethod
  def getMod(configValue):
    """
    get cryptomodule for cm. This is specialised for values, which you should enter in config.
    return cryptoModule or None in case of not found.
    """
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
        logger.error(tr("Could not find pycrypt-Module. Please install it via apt-get install python3-crypto"))
        return None
