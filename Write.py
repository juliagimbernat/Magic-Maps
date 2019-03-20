import MFRC522
START_X = str(-0.1736854)
START_Y = str(51.4966478)
END_X = str(-0.1640704)
END_Y = str(51.5006107)


text = START_X+","+START_Y+","+END_X+","+END_Y+","
#text = "dahkfhakufh"
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
        MIFAREReader.MFRC522_Read(11)
        data = bytearray()
        data.extend(bytearray(text.ljust(len(BLOCK_ADDRS) * 16).encode('ascii')))
        i = 0
        for block_num in BLOCK_ADDRS:
            MIFAREReader.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
            i += 1
        MIFAREReader.MFRC522_StopCrypto1()
        break






