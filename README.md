# Пульт CDT-1652S для Orange Pi PC

Этот проект превращает Orange Pi PC в устройство с управлением с ИК-пульта. Пульт может управлять встроенными светодиодами (красным и зелёным), а также выключать и перезагружать плату.

## 📦 Шаг 1. Установка зависимостей

Так как Debian 10 (Buster) официально не поддерживается, все пакеты перенесены в архив. Без этих команд `apt` не сможет найти нужные утилиты.

```bash
# Бэкап текущего списка репозиториев
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# Замена адресов на архивные
sudo sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list
sudo sed -i 's|security.debian.org|archive.debian.org|g' /etc/apt/sources.list

# Удаление устаревших веток (updates/backports), которых нет в архиве
sudo sed -i '/buster-updates/d' /etc/apt/sources.list
sudo sed -i '/buster-backports/d' /etc/apt/sources.list

# Отключение проверки срока действия (обязательно для архивов)
echo 'Acquire::Check-Valid-Until "false";' | sudo tee /etc/apt/apt.conf.d/99no-check-valid-until

# Обновление индексов и установка пакетов
sudo apt update
sudo apt install -y ir-keytable python3-evdev
```

## 📂 Шаг 2. Размещение файлов

Скопируйте файлы из репозитория в соответствующие директории на Orange Pi:

| Файл из репозитория | Куда копировать на Orange Pi |
| :--- | :--- |
| `home/orangepi/cdt-1652s_remote_keymap.toml` | `~/` (домашняя папка пользователя `orangepi`) |
| `home/orangepi/remote_led.py` | `~/` |
| `usr/local/bin/led_control.sh` | `/usr/local/bin/` |
| `etc/systemd/system/ir-setup.service` | `/etc/systemd/system/` |
| `etc/systemd/system/remote-led.service` | `/etc/systemd/system/` |

После копирования **обязательно** сделайте скрипт `led_control.sh` исполняемым и выставите права на Python-скрипт:

```bash
sudo chmod +x /usr/local/bin/led_control.sh
sudo chmod +x ~/remote_led.py
```

## ⚙️ Шаг 3. Включение и запуск служб

Перезагрузите конфигурацию systemd, чтобы он увидел новые файлы служб:
```bash
sudo systemctl daemon-reload
```
Включите автозапуск и запустите службы прямо сейчас:
```bash
sudo systemctl enable --now ir-setup remote-led
```
Проверьте, что службы успешно запустились:
```bash
systemctl status ir-setup.service --no-pager
systemctl status remote-led.service --no-pager
```

Также можно проверить, видит ли система нажатия кнопок на уровне драйвера:
```bash
sudo ir-keytable -t
```
Нажимайте кнопки на пульте. Вы должны увидеть в терминале строки вида key_down: KEY_...


## 🎮 Что умеет пульт

После запуска служб пульт выполняет следующие действия:

Управление питанием:

    Power — выключение платы (poweroff).

    Mute (выключение звука) — перезагрузка платы (reboot).

Управление красным светодиодом:

    1 — включить (постоянное свечение).

    4 — выключить.

    7 — анимация «сердцебиение».

Управление зелёным светодиодом:

    3 — включить (постоянное свечение).

    6 — выключить.

    9 — анимация «сердцебиение».
