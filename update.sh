sudo systemctl stop coffee-panic.service
arduino-cli compile --fqbn arduino:avr:uno ./arduino/arduino.ino
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno ./arduino/arduino.ino
sudo systemctl start coffee-panic.service
