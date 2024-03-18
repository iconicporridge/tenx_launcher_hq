import usb.core
from usb.backend import libusb0

# This backend works on windows
backend = libusb0.get_backend()


class tenx:

    def __init__(self):
        self.setup_commands()

    def connect_launcher(self):
        self.dev = usb.core.find(idVendor=0x1130, idProduct=0x0202, backend=backend)
        # On Linux we detach the kernel driver because that seemed to help
        try:
            self.dev.detach_kernel_driver(0)
            self.dev.detach_kernel_driver(1)
        # I'm expecting connect attempts when Dev isn't set (AttributeErrors)
        # but also NotImplementedErrors when on windows
        except Exception:
            pass
        try:
            self.dev.set_configuration()
        #  I'm expecting connect attempts when Dev isn't set
        except AttributeError:
            pass

    def check_connection(self):
        dev = usb.core.find(idVendor=0x1130, idProduct=0x0202, backend=backend)
        if (dev is None):
            return False
        else:
            return True

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
        self.stop = (0,  0,  0,  0,  0,  0)
        self.left = (0,  1,  0,  0,  0,  0)
        self.right = (0,  0,  1,  0,  0,  0)
        self.up = (0,  0,  0,  1,  0,  0)
        self.down = (0,  0,  0,  0,  1,  0)
        self.leftup = (0,  1,  0,  1,  0,  0)
        self.rightup = (0,  0,  1,  1,  0,  0)
        self.leftdown = (0,  1,  0,  0,  1,  0)
        self.rightdown = (0,  0,  1,  0,  1,  0)
        self.fire = (0,  0,  0,  0,  0,  1)

    def fire_launcher(self):
        if (self.dev is not None):
            self.dev.ctrl_transfer(bmRequestType=33, bRequest=9, wValue=2, wIndex=1, data_or_wLength=self.INITA)
            self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, self.INITB)
            self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, self.fire+self.CMDFILL)

    def move(self, cmd):
        if (self.dev is not None):
            self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, self.INITA)
            self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, self.INITB)
            self.dev.ctrl_transfer(0x21, 0x09, 0x02, 0x01, cmd+self.CMDFILL)
