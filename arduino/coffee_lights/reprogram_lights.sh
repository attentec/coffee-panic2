sudo systemctl stop coffee-monitor.service
/home/pi/bin/arduino-cli compile coffee-panic2/arduino/coffee_lights/  --fqbn arduino:avr:uno
/home/pi/bin/arduino-cli upload coffee-panic2/arduino/coffee_lights/ --fqbn arduino:avr:uno -p /dev/ttyACM0
sudo systemctl start coffee-monitor.service
