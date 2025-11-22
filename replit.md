# Telegram Channel Verification Bot

## Overview
A Telegram bot that verifies users' membership in two specified channels before allowing them to download an APK file.

## Features
- `/start` command with inline keyboard showing channel join links
- Automatic verification of channel membership
- APK file delivery after successful verification
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
- 2025-11-22: Initial project setup with environment variable configuration
