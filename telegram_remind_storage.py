import psutil
import schedule
import time
from telegram import Bot

# === CONFIGURATION ===
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'      # Replace with your bot token
CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'              # Replace with your Telegram chat ID
CHECK_PATHS = ['/', '/media/hdd1', '/media/hdd2']  # Add your mount points here
REMINDER_TIME = "09:00"  # 24-hour format

# === TELEGRAM BOT ===
bot = Bot(token=TELEGRAM_TOKEN)

def get_disk_usage():
    message = "Disk usage report:\n"
    for path in CHECK_PATHS:
        try:
            usage = psutil.disk_usage(path)
            total = usage.total / (1024 ** 3)
            used = usage.used / (1024 ** 3)
            free = usage.free / (1024 ** 3)
            message += (f"{path}:\n"
                        f"  Total: {total:.2f} GB\n"
                        f"  Used: {used:.2f} GB\n"
                        f"  Free: {free:.2f} GB\n\n")
        except FileNotFoundError:
            message += f"{path}:\n  Not found or not mounted\n\n"
    return message

def send_reminder():
    message = get_disk_usage()
    bot.send_message(chat_id=CHAT_ID, text=message)

# === SCHEDULER ===
schedule.every().day.at(REMINDER_TIME).do(send_reminder)

print(f"Bot started. Will send daily disk report at {REMINDER_TIME}...")
while True:
    schedule.run_pending()
    time.sleep(60)
