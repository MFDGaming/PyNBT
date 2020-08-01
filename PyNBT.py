import os
from struct import unpack, pack, calcsize

class PyNBT:
    root = {}
    TAG_END = 0
    TAG_BYTE = 1
    TAG_SHORT = 2
    TAG_INT = 3
    TAG_LONG = 4
    TAG_FLOAT = 5
    TAG_DOUBLE = 6
    TAG_BYTE_ARRAY = 7
    TAG_STRING = 8
    TAG_LIST = 9
    TAG_COMPOUND = 10
    TAG_INT_ARRAY = 11
    TAG_LONG_ARRAY = 12
    
    @staticmethod
    def checkLength(string, expect):
        length = len(string)
        assert (length == expect), 'Expected ' + str(expect) + 'bytes, got ' + str(length)
     
    @staticmethod
    def readTriad(str: bytes) -> int:
        PyNBT.checkLength(str, 3)
        return unpack('>L', b'\x00' + str)[0]

    @staticmethod
    def writeTriad(value: int) -> bytes:
        return pack('>L', value)[1:]

    @staticmethod
    def readLTriad(str: bytes) -> int:
        PyNBT.checkLength(str, 3)
        return unpack('<L', b'\x00' + str)[0]

    @staticmethod
    def writeLTriad(value: int) -> bytes:
        return pack('<L', value)[0:-1]
    
    @staticmethod
    def readBool(b: bytes) -> int:
        return unpack('?', b)[0]

    @staticmethod
    def writeBool(b: int) -> bytes:
        return b'\x01' if b else b'\x00'
  
    @staticmethod
    def readByte(c: bytes) -> int:
        PyNBT.checkLength(c, 1)
        return unpack('>B', c)[0]
    
    @staticmethod
    def readSignedByte(c: bytes) -> int:
        PyNBT.checkLength(c, 1)
        return unpack('>b', c)[0]

    @staticmethod
    def writeByte(c: int) -> bytes:
        return pack(">B", c)
    
    @staticmethod
    def readShort(str: bytes) -> int:
        PyNBT.checkLength(str, 2)
        return unpack('>H', str)[0]

    @staticmethod
    def writeShort(value: int) -> bytes:
        return pack('>H', value)
    
    @staticmethod
    def readLShort(str: bytes) -> int:
        PyNBT.checkLength(str, 2)
        return unpack('<H', str)[0]

    @staticmethod
    def writeLShort(value: int) -> bytes:
        return pack('<H', value)
    
    @staticmethod
    def readInt(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('>L', str)[0]

    @staticmethod
    def writeInt(value: int) -> bytes:
        return pack('>L', value)

    @staticmethod
    def readLInt(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('<L', str)[0]

    @staticmethod
    def writeLInt(value: int) -> bytes:
        return pack('<L', value)

    @staticmethod
    def readFloat(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('>f', str)[0]

    @staticmethod
    def writeFloat(value: int) -> bytes:
        return pack('>f', value)

    @staticmethod
    def readLFloat(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('<f', str)[0]

    @staticmethod
    def writeLFloat(value: int) -> bytes:
        return pack('<f', value)

    @staticmethod
    def readDouble(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('>d', str)[0]

    @staticmethod
    def writeDouble(value: int) -> bytes:
        return pack('>d', value)

    @staticmethod
    def readLDouble(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('<d', str)[0]

    @staticmethod
    def writeLDouble(value: int) -> bytes:
        return pack('<d', value)

    @staticmethod
    def readLong(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('>Q', str)[0]

    @staticmethod
    def writeLong(value: int) -> bytes:
        return pack('>Q', value)

    @staticmethod
    def readLLong(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('<Q', str)[0]

    @staticmethod
    def writeLLong(value: int) -> bytes:
        return pack('<Q', value)
    
    @staticmethod
    def loadFile(filename):
        if os.path.isfile(filename):
            fp = open(filename, "rb")
        else:
            print("First parameter must be a filename")
            return False
        bname = os.path.splitext(os.path.basename(filename))[0]
        if bname == 'level':
            version = PyNBT.readLInt(fp.read(4))
            lenght = PyNBT.readLInt(fp.read(4))
        elif(bname == 'entities'):
            fp.read(12)
        PyNBT.traverseTag(fp, PyNBT.root)
        return PyNBT.root
   
    @staticmethod
    def traverseTag(fp, tree: dict):
        tagType = PyNBT.readType(fp, PyNBT.TAG_BYTE)
        if not tagType == PyNBT.TAG_END:
            tagName = PyNBT.readType(fp, PyNBT.TAG_STRING)
            tagData = PyNBT.readType(fp, tagType)
            tree.update({'type': tagType, 'name': tagName, 'value': tagData})
            return True
     
    @staticmethod
    def readType(fp, tagType):
        if tagType == PyNBT.TAG_BYTE:
            return PyNBT.readByte(fp.read(1))
        elif tagType == PyNBT.TAG_SHORT:
            return PyNBT.readLShort(fp.read(2))
        elif tagType == PyNBT.TAG_INT:
            return PyNBT.readLInt(fp.read(4))
        elif tagType == PyNBT.TAG_LONG:
            return PyNBT.readLLong(fp.read(8))
        elif tagType == PyNBT.TAG_FLOAT:
            return PyNBT.readLFloat(fp.read(4))
        elif tagType == PyNBT.TAG_DOUBLE:
            return PyNBT.readLDouble(fp.read(8))
        elif tagType == PyNBT.TAG_BYTE_ARRAY:
            arrayLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(PyNBT.readType(fp, PyNBT.TAG_BYTE))
                i += 1
                return arr
        elif tagType == PyNBT.TAG_STRING:
            stringLength = PyNBT.readType(fp, PyNBT.TAG_SHORT)
            if not stringLength:
                return ""
            string = fp.read(stringLength)
            return string
        elif tagType == PyNBT.TAG_LIST:
            tagID = PyNBT.readType(fp, PyNBT.TAG_BYTE)
            listLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            list = {'type': tagID, 'value': []}
            i = 0
            while i < listLength:
                list["value"] = PyNBT.readType(fp, tagID)
                i += 1
            return list
        elif tagType == PyNBT.TAG_COMPOUND:
            tree = {}
            while PyNBT.traverseTag(fp, tree): pass
            return tree
        elif tagType == PyNBT.TAG_INT_ARRAY:
            arrayLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(PyNBT.readType(fp, PyNBT.TAG_INT))
                i += 1
                return arr
        elif tagType == PyNBT.TAG_LONG_ARRAY:
            arrayLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(PyNBT.readType(fp, PyNBT.TAG_LONG))
                i += 1
                return arr
