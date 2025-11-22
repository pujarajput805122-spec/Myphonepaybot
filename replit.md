# Telegram Channel Verification Bot

## Overview
A Telegram bot that verifies users' membership in two specified channels before allowing them to download an APK file.

## Features
- `/start` command with inline keyboard showing channel join links
- Automatic verification of channel membership
- APK file delivery after successful verification with password caption
- Forward protection to prevent APK file sharing
- Anti-spam cooldown mechanism (3 second cooldown on verify button)
- File caching for faster APK delivery (speeds up subsequent sends)
- Concurrent updates for better performance
- Error handling for missing channels or files

## Project Structure
- `bot.py` - Main bot application
- `requirements.txt` - Python dependencies
- APK file (to be uploaded by user)

## Environment Variables
Required environment variables:
- `BOT_TOKEN` - Telegram bot token from @BotFather
- `CHANNEL_1` - First channel chat ID
- `CHANNEL_2` - Second channel chat ID
- `CHANNEL_1_URL` - First channel invite URL
- `CHANNEL_2_URL` - Second channel invite URL
- `APK_PATH` - Path to APK file (default: PhonePe_1.0.apk)

## Setup Instructions
1. Get bot token from @BotFather on Telegram
2. Add bot as admin to both channels
3. Configure environment variables in Replit Secrets
4. Upload your APK file to the project
5. Run the bot

## Recent Changes
- 2025-11-22: Added Flask keep-alive server for 24/7 continuous operation on Replit
- 2025-11-22: Fixed callback timeout issues for reliable APK delivery
- 2025-11-22: Added performance optimizations (file caching, concurrent updates)
- 2025-11-22: Added forward protection and password caption to APK delivery
- 2025-11-22: Added anti-spam cooldown on verify button
- 2025-11-22: Initial project setup with environment variable configuration

## How It Works 24/7
The bot runs with:
1. **Telegram Bot Polling** - Continuously listens for user messages and button clicks
2. **Flask Keep-Alive Server** - Runs on port 8080 to prevent Replit from stopping the instance
3. **VM Deployment** - Configured to run continuously without interruption

## Status
✅ **Bot is live and running 24/7**
- Telegram Bot: @Phonepay2026_bot
- Keep-Alive Server: http://localhost:8080
- All features enabled and tested
