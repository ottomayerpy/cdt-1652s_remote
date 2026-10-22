#!/bin/bash

# Скрипт для управления красным светодиодом

LED_PATH="/sys/class/leds/orangepi:green:pwr/trigger"

case "$1" in
    "on")       echo "default-on" | sudo tee $LED_PATH > /dev/null ;;
    "off")      echo "none" | sudo tee $LED_PATH > /dev/null ;;
    "heartbeat") echo "heartbeat" | sudo tee $LED_PATH > /dev/null ;;
esac
