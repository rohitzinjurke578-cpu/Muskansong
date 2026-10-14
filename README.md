# Telegram Music Search Bot (Railway)

A small Telegram bot with `/start`, `/help`, and `/play <query>`. The `/play` command searches YouTube and returns links/buttons; it does not download or redistribute music.

## 1. Create a bot token
1. Open Telegram and contact **@BotFather**.
2. Send `/newbot`, follow the prompts, and copy the token.
3. Keep the token private. If it leaks, revoke it with BotFather.

## 2. Put the code on GitHub
Upload all files in this folder to a new GitHub repository. Do **not** upload `.env`, session files, API hashes, or session strings.

## 3. Deploy on Railway
1. Open https://railway.app/ and create a project.
2. Choose **Deploy from GitHub Repo** and select this repository.
3. In the service's **Variables** tab, add:
   - `BOT_TOKEN` = your BotFather token
   - `BOT_NAME` = the display name you want
4. Railway should detect the `Procfile`. If it asks for a start command, use `python bot.py`.
5. Deploy and inspect the deployment logs. A successful start should show `Bot is starting`.
6. Open your bot in Telegram and test `/start`, `/help`, and `/play relaxing instrumental`.

This is a worker process and does not need a public web domain. Confirm Railway's current plan/usage and billing before deploying; availability and free credits can change.

## 4. Generate your own Pyrogram String Session (LOCAL ONLY)
The session generator is intentionally a separate script and should **not** be deployed on Railway.

1. On a trusted computer, install Python 3.10–3.12.
2. In this folder run:
   ```bash
   python -m venv .venv
   ```
   Activate it:
   - Windows: `.venv\\Scripts\\activate`
   - macOS/Linux: `source .venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Get your own API ID and API Hash from https://my.telegram.org (never from a stranger).
5. Run:
   ```bash
   python session_generator.py
   ```
6. Enter your API ID and API Hash. Complete Telegram's login verification when prompted. The script prints a session string.

**Security:** A session string is equivalent to an account credential. Never send it to anyone, never put it in GitHub, and never paste it into bot chats or public logs. If exposed, terminate active sessions in Telegram Settings → Devices and create a fresh session. Do not run an unknown third-party session generator.

## Notes
- This starter is a search bot, not a voice-chat streaming bot.
- Use official or authorized music sources and respect copyright and platform terms.
- Pyrogram is an older, no-longer-actively-maintained library; consider a maintained alternative for new production projects.
