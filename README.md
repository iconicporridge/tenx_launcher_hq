# tenx_launcher_hq

A repository for my python codes to operate a Tenx (M&amp;S) USB foam missile launcher. I'm running elementary os Juno, probably won't work straight off the bat in Windows (because I haven't used os to control filepaths). 

## Dependancies

You'll probably find out when it doesn't work, but python 3.x, pyqt5, and pyusb are the main ones. 

## How to use

Run "command_centre.py" with "python command_centre.py" or your system equivalent (eg. python3). 

## Udev Rules

You might need extra permissions to use a USB device from python. One way is to use sudo, but you might not want your kids to have your password. I've included an example udev rule "99-missile-launcher.rules", which goes in /etc/udev/rules.d on Ubuntu like systems. You'll need to modify the rule to your username etc. place it in the correct directory and restart your computer.

## License Stuff
Icons from FlatIcon/freepik under CC 3.0 BY

Code for sending the USB signals was modified from https://code.google.com/archive/p/pymissile/ and Codedance's Retaliation: https://github.com/codedance/Retaliation

Feel free to reuse my code, but it would be nice if you would let me know/credit me :-)
