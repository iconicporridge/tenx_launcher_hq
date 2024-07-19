# tenx_launcher_hq
A repository for my python code to operate a Tenx (M&amp;S) USB foam missile launcher.

## Installation
### Windows specific details
You will need to install some version of LibUSB for the launcher. I've found the easiest way to do this is with [Zadig](https://zadig.akeo.ie/).

I used Zadig 2.9:
- Make sure the launcher is plugged into your computer and powered on
- Run Zadig
- Options -> List All Devices
- Select the 'Tenx Nonstandard Devic'\[sic\] Vendor=0x1130, Product=0x0202.
- For the driver select 'libusb-win32' (at the time of writing that was 1.4.0). [You could select a different driver if you choose to you use a different backend.](#libusb)
- Hit install driver and wait for it to finish

### Linux specific details
You might have permissions issues. If you do read the [Udev rules](#udev-rules) section.

### All platforms
- Clone the project: `https://github.com/iconicporridge/tenx_launcher_hq.git`
- Move into the directory: `cd tenx_launcher_hq`
- I'd recommend creating a conda environment using the provided file:
    - `conda env create -f environment.yml`
    - `conda activate usb-launcher`
- Or you can create a pip virtual environment (warning: I'm not sure PyQT installs very nicely from pip):
    - ` python -m venv usb-launcher`
    - Use the path to the virtual environment to install the requirements file: ` ./usb-launcher/bin/pip install -r requirements.txt`.
    - Going forward use the virtual environment python: `./usb-launcher/bin/python3` instead of just `python`.
- Run the application: `python command_centre.py`
- [You should get this GUI if your device is detected.](./images/gui.png)

## Troubleshooting
### Udev rules
You might need extra permissions to use a USB device from python. One way is to use sudo, but you might not want your kids to have your password.

An alternative is setting udev rules. I've included an example udev rule `99-missile-launcher.rules`, which goes in /etc/udev/rules.d on Ubuntu like systems. You'll need to modify the rule to use your username, then place it in the correct directory and restart your computer.

### LibUSB
LibUSB is not a default on windows like it is for most linux systems. I've had lots of trouble faffing around with LibUSB versions over the years, hopefully that is now sorted and everything is configured automatically by [Zadig](https://zadig.akeo.ie/) and pyusb.

However, if you run into trouble you can try changing the backend in `lib/launcher.py` for `usb` functions with the `backend=` kwarg. You can import different backends from `usb.backend` like `from usb.backend import libusb1`. [Find out more on the pyusb github page](https://github.com/pyusb/pyusb). On  windows you'll also then need to install the corresponding driver for your device with Zadig.

If Zadig isn't working you could also try experimenting with using the filter wizard you get when you install `libusb-win32-devel-filter.exe` on the [libusb-win32 releases page](https://github.com/mcuee/libusb-win32/releases).




