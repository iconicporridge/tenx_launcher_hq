# Code modified from https://code.google.com/archive/p/pymissile/ and Codedance
# Retaliation: https://github.com/codedance/Retaliation

import sys
import platform
import time
import usb

class Tenx:

    def __init__(self):
        self.dev = usb.core.find(idVendor=0x1130, idProduct=0x0202)
        try:
            self.dev.detach_kernel_driver(0)
            self.dev.detach_kernel_driver(1)
        except Exception as e:
            print(e)
            pass
        self.setup_commands()

    def setup_commands(self):
        self.INITA = (85, 83, 66, 67,  0,  0,  4,  0)
        self.INITB = (85, 83, 66, 67,  0, 64,  2,  0)
        self.CMDFILL = ( 8,  8,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0)


    def send_cmd(self, cmd):
        self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, self.INITA)
        self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, self.INITB)
        self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, cmd+self.CMDFILL)
        time.sleep(1)


def main(args):

    STOP      = ( 0,  0,  0,  0,  0,  0)
    LEFT      = ( 0,  1,  0,  0,  0,  0)
    RIGHT     = ( 0,  0,  1,  0,  0,  0)
    UP        = ( 0,  0,  0,  1,  0,  0)
    DOWN      = ( 0,  0,  0,  0,  1,  0)
    LEFTUP    = ( 0,  1,  0,  1,  0,  0)
    RIGHTUP   = ( 0,  0,  1,  1,  0,  0)
    LEFTDOWN  = ( 0,  1,  0,  0,  1,  0)
    RIGHTDOWN = ( 0,  0,  1,  0,  1,  0)
    FIRE      = ( 0,  0,  0,  0,  0,  1)

    myDevice = Tenx()
    myDevice.send_cmd(FIRE)


if __name__ == '__main__':
    main(sys.argv)
