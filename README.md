# SunByte-Digital-Clock
SunByte is a Digital Clock with Weather updates. It is based on Python and Kivy Framework. It is designed for Unihiker. But can be used for desktop with few changes.
# Requirements and Steps
You need to install kivy using following command.

`pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/`

Next set the timezone before running this file. Yo can check your current timezone with the following command:

`timedatectl`

You can list the available timezones with,

`sudo timedatectl set-timezone Asia/Karachi`


And set the time zone with:

`sudo timedatectl set-timezone <your_time_zone>`

For Example, I'm in Pakistan. So,

`sudo timedatectl set-timezone Asia/Karachi`

And now you can run your program. But don't forget to change the Weather API credentials. 
