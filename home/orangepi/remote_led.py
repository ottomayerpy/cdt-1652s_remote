#!/usr/bin/env python3
import evdev
import subprocess
import time

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
remote = None
for device in devices:
    if "sunxi-ir" in device.name:
        remote = device
        break

if not remote:
    print("IR-приемник не найден!")
    exit(1)

NAME_MAP = {
    "KEY_1": "/usr/local/bin/led_control.sh red on",
    "KEY_4": "/usr/local/bin/led_control.sh red off",
    "KEY_7": "/usr/local/bin/led_control.sh red heartbeat",
    "KEY_3": "/usr/local/bin/led_control.sh green on",
    "KEY_6": "/usr/local/bin/led_control.sh green off",
    "KEY_9": "/usr/local/bin/led_control.sh green heartbeat",
    "KEY_MUTE": "sudo reboot",
    "KEY_POWER": "sudo poweroff",
}

for event in remote.read_loop():
    # 1 = EV_KEY (нажатие кнопки)
    if event.type == evdev.ecodes.EV_KEY and event.value == 1:
        keycode = event.code
        # Получаем имя клавиши (evdev может вернуть строку или список строк)
        key_names = evdev.ecodes.KEY[keycode]
        # Если вернулся список, берем нужное нам имя
        if isinstance(key_names, list):
            # Ищем KEY_MUTE, иначе берем последнее
            if 'KEY_MUTE' in key_names:
                key_name = 'KEY_MUTE'
            else:
                key_name = key_names[-1]
        else:
            key_name = key_names
        # Выполняем команду, если она есть в словаре
        if key_name in NAME_MAP:
            cmd = NAME_MAP[key_name]
            subprocess.run(cmd, shell=True)
