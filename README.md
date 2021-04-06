MIT licensed Sam Henderson 2021 https://opensource.org/licenses/MIT

# tenx_launcher_hq

A repository for my python codes to operate a Tenx (M&amp;S) USB foam missile launcher. See the Udev rules section for a known Linux problem and the Windows problems for things you might have to do to get it running under windows. 

## Dependancies

You'll probably find out when it doesn't work, but python 3.x, pyqt5, and pyusb are the main ones. 

## How to use

Run "command_centre.py" with "python command_centre.py" or your system equivalent (eg. python3). 

## Udev Rules

You might need extra permissions to use a USB device from python. One way is to use sudo, but you might not want your kids to have your password. I've included an example udev rule "99-missile-launcher.rules", which goes in /etc/udev/rules.d on Ubuntu like systems. You'll need to modify the rule to your username etc. place it in the correct directory and restart your computer.

## Windows Problems

Libusb is not a default on windows like it is for most linux systems. Install https://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.6.0/libusb-win32-devel-filter-1.2.6.0.exe/ or some other version of libusb. Right now there is a comment in launcher.py you may need to uncomment on windows, in the connect_launcher function.

## License Stuff
Icons from FlatIcon/freepik under CC 3.0 BY

Code for sending the USB signals was modified from https://code.google.com/archive/p/pymissile/ and Codedance's Retaliation: https://github.com/codedance/Retaliation


