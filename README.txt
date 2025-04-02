🌐 Telegram Bot for Web Scraping

Need to extract information from websites easily and automatically? This bot performs web scraping tasks, gathering data and sending it directly to you in Telegram!
With this bot, you can automate the extraction of data from websites, such as product prices, reviews, or any publicly available content.

✅ What does it do?

 • 🌍 Scrapes data from websites based on your specified criteria
 • 📈 Collects and organizes information for easy access
 • 📤 Sends the scraped data directly to you on Telegram
 • 🗂️ Supports storing data in a structured format (e.g., CSV or JSON)

🔧 Features

✅ Customizable scraping rules based on your needs
✅ Supports scraping multiple websites
✅ Real-time notifications when new data is available
✅ Easy-to-use interface for managing scraping tasks

📩 Need data from websites on demand?

Contact me on Telegram, and I’ll help you set up this bot to scrape the information you need! 🚀

# INSTRUCTIONS FOR INSTALLING AND LAUNCHING A TELEGRAM BOT FOR PARSING

## FOR WINDOWS

### Step 1: Install Python
1. Download Python 3.9.13 from the official website: https://www.python.org/downloads/release/python-3913 /
- Scroll down and select "Windows installer (64-bit)"
- When the installer starts, BE SURE to check the box "Add Python 3.9 to PATH"
- Click "Install Now"

2. Check the installation:
- Click Start → type "cmd" → open the Command prompt
   - Enter the command: python --version
   - It should sound like "Python 3.9.13"

### Step 2: Preparing the folder for the bot
1. Create a telegram-bot folder on your desktop
2. Copy the files "telegram_parser_bot.py " and "requirements.txt " to this folder

### Step 3: Getting the Bot Token
1. Open Telegram
2. Find @BotFather (this is the official bot for creating bots)
3. Write him a command: /newbot
4. Come up with a name for the bot
5. Come up with a unique username for the bot (must end with "bot")
6. BotFather will give you a bot token - a long string of characters
7. COPY AND SAVE THIS TOKEN (it is needed for the next step)

### Step 4: Create a Token file
1. Open the Notepad
2. Write in it: BOT_TOKEN=your_token_bot
   (insert the copied token instead of "your_token_bot")
3. Save the file to the telegram-bot folder named ".env"
- When saving, select "File type: All files (*.*)"
- Important: the file name SHOULD be ".env" (with a dot at the beginning)

### Step 5: Install Dependencies
1. Click Start → type "cmd" → open the Command Prompt
2. Enter the commands (press Enter after each line):
   ```
   cd Desktop\telegram-bot
   pip install -r requirements.txt
   ```
3. Wait for the installation to finish (it may take a few minutes)

### Step 6: Launch the Bot
1. In the same command prompt, type:
   ```
   python telegram_parser_bot.py
   ```
2. If everything is done correctly, you will see messages about the launch of the bot.
3. The bot is running! DO NOT CLOSE the command line, otherwise the bot will stop.

### Step 7: Using the Bot
1. Open Telegram
2. Find your bot by the name you specified
3. Press the "Start" button or send the command /start
4. Now you can use the bot!
   - /set_url - set the website URL for parsing
   - /parse - perform parsing
   - /help - get help

### If you need to stop the bot:
- Press Ctrl+C at the command prompt.

### If you need to start the bot again:
1. Open the command prompt
2. Enter:
   ```
   cd Desktop\telegram-bot
   python telegram_parser_bot.py
   ```

## FOR LINUX

### Step 1: Install Python and pip
1. Open a Terminal (usually Ctrl+Alt+T)
2. Enter the following commands (press Enter after each line):
   ```
   sudo apt update
   sudo apt install python3.9 python3.9-venv python3-pip
   ```
3. Check the installation:
``
   python3.9 --version
   ```
   It should sound like something like "Python 3.9.x"

### Step 2: Preparing the folder for the bot
1. Create a folder for the bot:
   ```
   mkdir ~/telegram-bot
   cd ~/telegram-bot
   ```

2. Create a file with the bot code:
   ```
   nano telegram_parser_bot.py
``
- Insert the bot code
- To save: Ctrl+O, then Enter
   - To exit: Ctrl+X

3. Create a file with dependencies:
``
   nano requirements.txt
``
- Enter:
     ```
     aiogram>=3.0.0
requests==2.31.0
beautifulsoup4==4.12.2
python-dotenv==1.0.0
``
- To save: Ctrl+O, then Enter
   - To exit: Ctrl+X

### Step 3: Getting a bot token (just like in Windows)
1. Open Telegram
2. Find @BotFather
3. Send him a command: /newbot
4. Come up with a name for the bot
5. Come up with a unique username (must end with "bot")
6. COPY AND SAVE the TOKEN that BotFather will give you

### Step 4: Create a Token file
1. Enter:
   ```
   nano .env
   ```
2. Enter: BOT_TOKEN=your_token_bot
   (insert the copied token instead of "your_token_bot")
3. To save: Ctrl+O, then Enter
4. To exit: Ctrl+X

### Step 5: Create a virtual environment and install dependencies
1. Enter the commands:
   ```
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Wait for the installation to finish

### Step 6: Launch the Bot
1. In the terminal, enter:
   ```
   python telegram_parser_bot.py
   ```
2. If everything is done correctly, you will see messages about the launch of the bot.
3. The bot is running! DO NOT CLOSE the terminal, otherwise the bot will stop.

### Step 7: Using the Bot
1. Open Telegram
2. Find your bot by the name you specified
3. Press the "Start" button or send the command /start
4. Now you can use the bot!
   - /set_url - set the website URL for parsing
   - /parse - perform parsing
- /help - get help

### If you need to stop the bot:
- Press Ctrl+C in the terminal.

### If you need to start the bot again:
1. Open the terminal
2. Enter:
   ```
   cd ~/telegram-bot
   source venv/bin/activate
   python telegram_parser_bot.py
   ```

## SOLVING POSSIBLE PROBLEMS

### "Python not found" on Windows
1. Check if the "Add Python to PATH" checkbox is worth checking during installation
2. If you have already installed it without this check mark, run the installer again and select "Modify"

### "Cannot install dependencies" on Windows or Linux
1. Try to install them one at a time:
   ```
   pip install aiogram
   pip install requests
   pip install beautifulsoup4
   pip install python-dotenv
   ```

### "Unable to connect to Telegram" on Windows or Linux
1. Check your internet connection
2. Check the validity of the token in the .env file
3. If you use a proxy, you may need additional settings.

### Bot is not responding in Telegram
1. Make sure that the command prompt/terminal with the bot is open and running
2. Try restarting the bot
3. Try to send the command /start

### HOW TO USE THE BOT

1. Send the /set_url command to the bot
2. The bot will ask you to enter the website address. Enter the full URL (for example, https://www.example.com )
3. After setting the URL, send the command /parse
4. The bot will start parsing the site and send you the results.:
   - Page title
- Main links on the page
- Text content
5. To change the site, use the /set_url command again.
