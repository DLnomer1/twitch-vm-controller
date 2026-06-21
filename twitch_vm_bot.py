"""
Twitch VM Shell Controller
Зрители выполняют команды в терминале виртуальной машины через чат Twitch.

Установка:
    pip install twitchio

Запуск:
    python twitch_vm_bot.py
"""

import asyncio
import time
import logging
from twitchio.ext import commands

# ─── Конфиг ────────────────────────────────────────────────────────────────────

TWITCH_TOKEN   = "oauth:ВСТАВЬ_ТОКЕН_ЗДЕСЬ"   # https://twitchtokengenerator.com
TWITCH_PREFIX  = "!"
TWITCH_CHANNEL = "ИМЯ_ТВОЕГО_КАНАЛА"

# Кто может выполнять команды:
#   "all"         — все зрители
#   "subscribers" — только подписчики
#   "mods"        — только модераторы
#   "mods+subs"   — модераторы и подписчики
ACCESS_LEVEL = "all"

# Задержка между командами одного зрителя (секунды)
USER_COOLDOWN = 5.0

# Глобальный кулдаун между любыми командами (секунды)
GLOBAL_COOLDOWN = 1.0

# Таймаут выполнения команды (секунды). Зависшие команды убиваются.
COMMAND_TIMEOUT = 10

# Максимальная длина вывода, отправляемого обратно в чат (символов)
OUTPUT_MAX_LEN = 400

# Отправлять ли результат команды обратно в чат
REPLY_IN_CHAT = True

# Заблокированные команды — зрители не смогут выключить ВМ или убить бота
BLOCKED_COMMANDS = [
    "shutdown", "poweroff", "reboot", "halt", "init",
    "systemctl poweroff", "systemctl reboot", "systemctl halt",
    "kill", "killall", "pkill",
]

# ─── Логирование ───────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("vmbot")

# ─── Проверка доступа ──────────────────────────────────────────────────────────

def has_access(author) -> bool:
    if ACCESS_LEVEL == "all":
        return True
    is_mod = author.is_mod or author.is_broadcaster
    is_sub = author.is_subscriber
    if ACCESS_LEVEL == "mods":
        return is_mod
    if ACCESS_LEVEL == "subscribers":
        return is_sub or is_mod
    if ACCESS_LEVEL == "mods+subs":
        return is_mod or is_sub
    return False

# ─── Проверка блокировки ───────────────────────────────────────────────────────

def is_blocked(cmd: str) -> bool:
    first = cmd.strip().split()[0].lower() if cmd.strip() else ""
    if first in BLOCKED_COMMANDS:
        return True
    for blocked in BLOCKED_COMMANDS:
        if cmd.strip().lower().startswith(blocked):
            return True
    return False

# ─── Выполнение команды ────────────────────────────────────────────────────────

async def run_shell(cmd: str) -> str:
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        try:
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=COMMAND_TIMEOUT)
        except asyncio.TimeoutError:
            proc.kill()
            return f"[таймаут {COMMAND_TIMEOUT}с — команда убита]"

        output = stdout.decode("utf-8", errors="replace").strip()
        if not output:
            return "[выполнено, нет вывода]"
        if len(output) > OUTPUT_MAX_LEN:
            output = output[:OUTPUT_MAX_LEN] + "…"
        return output

    except Exception as exc:
        return f"[ошибка: {exc}]"

# ─── Twitch бот ────────────────────────────────────────────────────────────────

class VMBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix=TWITCH_PREFIX,
            initial_channels=[TWITCH_CHANNEL],
        )
        self._user_cd: dict[str, float] = {}
        self._last_global: float = 0.0

    async def event_ready(self):
        log.info("Бот подключён как: %s", self.nick)
        log.info("Канал: #%s  |  Доступ: %s", TWITCH_CHANNEL, ACCESS_LEVEL)
        log.info("Кулдаун: %.0fс на юзера, %.1fс глобальный", USER_COOLDOWN, GLOBAL_COOLDOWN)

    async def event_message(self, message):
        if message.echo:
            return

        content = message.content.strip()
        if not content.startswith(TWITCH_PREFIX):
            return

        cmd = content[len(TWITCH_PREFIX):].strip()
        if not cmd:
            return

        author = message.author
        user   = author.name

        if not has_access(author):
            return

        now = time.monotonic()

        # Глобальный кулдаун
        if now - self._last_global < GLOBAL_COOLDOWN:
            return

        # Кулдаун на пользователя
        last = self._user_cd.get(user, 0.0)
        if now - last < USER_COOLDOWN:
            remaining = USER_COOLDOWN - (now - last)
            if REPLY_IN_CHAT:
                await message.channel.send(f"@{user} подожди ещё {remaining:.1f}с")
            return

        # Заблокированные команды
        if is_blocked(cmd):
            log.warning("BLOCKED  %-20s  %s", user, cmd)
            if REPLY_IN_CHAT:
                await message.channel.send(f"@{user} эта команда запрещена")
            return

        self._user_cd[user] = now
        self._last_global   = now

        log.info("RUN  %-20s  $ %s", user, cmd)

        output = await run_shell(cmd)
        log.info("OUT  %s", output[:120])

        if REPLY_IN_CHAT:
            await message.channel.send(f"@{user}: {output}")


# ─── Точка входа ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Запуск Twitch VM Shell Bot...")
    bot = VMBot()
    bot.run()
