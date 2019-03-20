

import MFRC522
MIFAREReader = MFRC522.MFRC522()
KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
BLOCK_ADDRS = [8, 9, 10]
    
while True:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print "Card detected"
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        MIFAREReader.MFRC522_SelectTag(uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 11, KEY, uid)
    data = []
    text_read = ''
    if status == MIFAREReader.MI_OK:
        for block_num in BLOCK_ADDRS:
            block = MIFAREReader.MFRC522_Read(block_num)
            if block:
                data += block
        if data:
            text_read = ''.join(chr(i) for i in data)
        MIFAREReader.MFRC522_StopCrypto1()
        print text_read
        break




