#!/bin/bash

# Скрипт для управления светодиодами Orange Pi

COLOR="$1"
MODE="$2"
LED_PATH="/sys/class/leds/orangepi:${COLOR}:status/trigger"

if [ "$COLOR" == "green" ]; then
    LED_PATH="/sys/class/leds/orangepi:green:pwr/trigger"
fi

case "$MODE" in
    "on")        echo "default-on" | sudo tee $LED_PATH > /dev/null ;;
    "off")       echo "none" | sudo tee $LED_PATH > /dev/null ;;
    "heartbeat") echo "heartbeat" | sudo tee $LED_PATH > /dev/null ;;
esac
