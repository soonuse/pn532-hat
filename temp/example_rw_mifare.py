"""
This example shows connecting to the PN532 and writing an M1
type RFID tag

Warning: DO NOT write the blocks of 4N+3 (3, 7, 11, ..., 63)
or else you will change the password for blocks 4N ~ 4N+2.

Note: 
1.  The first 6 bytes (KEY A) of the 4N+3 blocks are always shown as 0x00,
since 'KEY A' is unreadable. In contrast, the last 6 bytes (KEY B) of the 
4N+3 blocks are readable.
2.  Block 0 is unwritable. 
"""
import RPi.GPIO as GPIO

import pn532.pn532 as nfc

#from pn532.spi import PN532_SPI
from pn532.uart import PN532_UART

#pn532 = PN532_SPI(debug=False, reset=20, cs=4)
pn532 = PN532_UART(debug=False, reset=20)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print('Waiting for RFID/NFC card to write to!')
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="")
    # Try again if no card is available.
    if uid is not None:
        break
print('Found card with UID:', [hex(i) for i in uid])

"""
Warning: DO NOT write the blocks of 4N+3 (3, 7, 11, ..., 63)
or else you will change the password for blocks 4N ~ 4N+2.

Note: 
1.  The first 6 bytes (KEY A) of the 4N+3 blocks are always shown as 0x00,
since 'KEY A' is unreadable. In contrast, the last 6 bytes (KEY B) of the 
4N+3 blocks are readable.
2.  Block 0 is unwritable. 
"""
block_number = 0
key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
data = bytes([0x4A, 0x3B, 0xC7, 0x54, 0xE2, 0x08, 0x04, 0x00, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69])

try:
    pn532.mifare_classic_authenticate_block(
        uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
    pn532.mifare_classic_write_block(block_number, data)
    if pn532.mifare_classic_read_block(block_number) == data:
        print('write block %d successfully' % block_number)
except nfc.PN532Error as e:
    print(e.errmsg)
GPIO.cleanup()
