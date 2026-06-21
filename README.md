[README.md](https://github.com/user-attachments/files/29181381/README.md)
# twitch-vm-controller
Бот для Twitch, который позволяет зрителям выполнять команды Linux прямо в чате — и управлять машиной в реальном времени.
# Twitch VM Controller 🎮

**RU** | [EN](#english)

Бот для Twitch, который позволяет зрителям выполнять команды Linux прямо в чате — и управлять виртуальной машиной в реальном времени.

## Как это работает

Зритель пишет в чат `!ls` — бот выполняет команду на виртуальной машине и отправляет результат обратно в чат.

## Требования

- Python 3.10+
- Linux
- Аккаунт Twitch

## Установка

```bash
# 1. Создать виртуальное окружение
python3 -m venv ~/venv
source ~/venv/bin/activate

# 2. Установить зависимости
pip install "twitchio==2.10.0"

# 3. Скачать скрипт
wget https://raw.githubusercontent.com/DLnomer1/twitch-vm-controller/main/twitch_vm_bot.py
```

## Настройка

Открой `twitch_vm_bot.py` и вставь свои данные в начале файла:

```python
TWITCH_TOKEN   = "oauth:ВАШ_ТОКЕН"    # https://twitchtokengenerator.com
TWITCH_CHANNEL = "имя_канала"
```

Получить токен: https://twitchtokengenerator.com → **Bot Chat Token** → скопировать Access Token.

### Параметры

| Параметр | По умолчанию | Описание |
|---|---|---|
| `ACCESS_LEVEL` | `"all"` | Кто может выполнять команды: `all`, `subscribers`, `mods`, `mods+subs` |
| `USER_COOLDOWN` | `5.0` | Задержка между командами одного зрителя (секунды) |
| `GLOBAL_COOLDOWN` | `1.0` | Глобальная задержка между любыми командами (секунды) |
| `COMMAND_TIMEOUT` | `10` | Максимальное время выполнения команды (секунды) |
| `BLOCKED_COMMANDS` | см. файл | Список запрещённых команд |

## Запуск

```bash
source ~/venv/bin/activate
python3 twitch_vm_bot.py
```

## Примеры команд для зрителей

```
!ls -la
!whoami
!echo привет мир
!python3 --version
!date
!free -h
!uptime
```

## Безопасность

> ⚠️ **Запускай бота только внутри виртуальной машины**, а не на основном компьютере.
- Не вставляй токен в публичный репозиторий — добавь `.env` в `.gitignore`
---

<a name="english"></a>

# Twitch VM Controller 🎮

A Twitch bot that lets viewers execute Linux commands in chat and control a virtual machine in real time.

## How it works

A viewer types `!ls` in chat — the bot runs the command on the virtual machine and sends the output back to chat.

## Requirements

- Python 3.10+
- Linux
- A Twitch account

## Installation

```bash
# 1. Create virtual environment
python3 -m venv ~/venv
source ~/venv/bin/activate

# 2. Install dependencies
pip install "twitchio==2.10.0"

# 3. Download the script
wget https://raw.githubusercontent.com/DLnomer1/twitch-vm-controller/main/twitch_vm_bot.py
```

## Setup

Open `twitch_vm_bot.py` and fill in your credentials at the top:

```python
TWITCH_TOKEN   = "oauth:YOUR_TOKEN"   # https://twitchtokengenerator.com
TWITCH_CHANNEL = "your_channel_name"
```

Get your token at: https://twitchtokengenerator.com → **Bot Chat Token** → copy Access Token.

### Settings

| Parameter | Default | Description |
|---|---|---|
| `ACCESS_LEVEL` | `"all"` | Who can run commands: `all`, `subscribers`, `mods`, `mods+subs` |
| `USER_COOLDOWN` | `5.0` | Cooldown per viewer between commands (seconds) |
| `GLOBAL_COOLDOWN` | `1.0` | Global cooldown between any commands (seconds) |
| `COMMAND_TIMEOUT` | `10` | Max execution time before a command is killed (seconds) |
| `BLOCKED_COMMANDS` | see file | List of forbidden commands |

## Running

```bash
source ~/venv/bin/activate
python3 twitch_vm_bot.py
```

## Example commands for viewers

```
!ls -la
!whoami
!echo hello world
!python3 --version
!date
!free -h
!uptime
```

## Security

> ⚠️ **Only run this bot inside a virtual machine**, never on your main computer.
- Never put your token in a public repository — add `.env` to `.gitignore`
