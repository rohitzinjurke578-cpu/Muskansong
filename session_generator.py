"""
Run this file LOCALLY on your own trusted device.
Do not deploy it as a public web app or paste its output into chats/logs.
A Pyrogram session string can grant access to your Telegram account.
"""
from pyrogram import Client

api_id_text = input("Telegram API ID (from my.telegram.org): ").strip()
api_hash = input("Telegram API Hash (from my.telegram.org): ").strip()

if not api_id_text.isdigit() or not api_hash:
    raise SystemExit("API ID must be numeric and API Hash must not be empty.")

with Client(
    name="my_account_session",
    api_id=int(api_id_text),
    api_hash=api_hash,
    in_memory=True
) as app:
    session_string = app.export_session_string()

print("\nSESSION STRING (PRIVATE — DO NOT SHARE):\n")
print(session_string)
print("\nSave it only in a trusted password manager or a private secret store.")
