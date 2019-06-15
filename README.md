# appsense
Aerial raspberry pi platform

Point the gps daemon to the GPS device on UART
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock

Then run cgps to check the GPS data
cgps -s


Notes:

I had to disable a systemd service that gpsd installs
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket

To enable it, run these commands

sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket


If there's no data, double check that everything's plugged in.
Then run this:
pi@pitestenv:~ $ sudo nano /etc/default/gpsd
pi@pitestenv:~ $ sudo ln -s /lib/systemd/system/gpsd.service /etc/systemd/system/multi-user.target.wants/
pi@pitestenv:~ $ sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
pi@pitestenv:~ $ gpsmon
pi@pitestenv:~ $ cgps

gpsmon and cgps -s should show data

####If they show NOFIX, run these, wait a few minutes and try again
pi@pitestenv:~ $ sudo killall gpsd
pi@pitestenv:~ $ sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock


Once data is being retrieved, python can get the GPS data
pi@pitestenv:~ $ python ~/dv/test/gpsdData.py
