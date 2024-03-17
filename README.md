# tenx_launcher_hq
A repository for my python codes to operate a Tenx (M&amp;S) USB foam missile launcher.

## Installation
On windows you will need [libusb](https://github.com/mcuee/libusb-win32/releases) -- I used libusb0.1 1.27. If you don't know what that means, [find out more on the pyusb github page](https://github.com/pyusb/pyusb). Once you've downloaded libusb0.1 run the gui to install the filter for your device (Vendor=0x1130, Product=0x0202).

On linux you might have permissions issues. If you do read the [troubleshooting](#troubleshooting) section. You might also want to change the backend to libusb1 in `lib/launcher.py`.

Clone the project: `https://github.com/iconicporridge/tenx_launcher_hq.git`
Move into the directory: `cd tenx_launcher_hq`

I'd recommend creating a conda environment using the provided file:
    - `conda env create -f environment.yml`
    - `conda activate usb-launcher`

Or you can create a pip virtual environment:
    - ` python -m venv usb-launcher`
    - and then use the path to the virtual environment to install the requirements file: ` ./usb-launcher/bin/pip install -r requirements.txt`.
However I'm not sure PyQT installs very nicely from pip.

To use the virtual environment python use the path like: `./usb-launcher/bin/python3`.

Then run the application: `python command_centre.py`

 You should get this GUI: [The GUI if your device is detected.](./images/gui.png)

## Troubleshooting
### Udev Rules
You might need extra permissions to use a USB device from python. One way is to use sudo, but you might not want your kids to have your password.

An alternative is setting udev rules. I've included an example udev rule `99-missile-launcher.rules`, which goes in /etc/udev/rules.d on Ubuntu like systems. You'll need to modify the rule to use your username, then place it in the correct directory and restart your computer.

### Libusb
Libusb is not a default on windows like it is for most linux systems. There are a variety of different libusb 'backends' available. The most common is called libusb1.0 but that didn't work on windows for this project (it worked fine on Arch). I'm using libusb0.1. You can change the backend in `lib/launcher.py`. Find out more at the [pyusb project](https://github.com/pyusb/pyusb).

## License Stuff
Icons from FlatIcon/freepik under CC 3.0 BY
Code for sending the USB signals was modified from [pymissile](https://code.google.com/archive/p/pymissile/) and [Codedance's Retaliation](https://github.com/codedance/Retaliation). I don't understand USB protocols so I wouldn't have done it without you, thanks :).


