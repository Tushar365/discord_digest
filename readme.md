# Clone repository (use cmd):
git clone <your-repo-url>
cd discord-digest-bot

# Create virtual environment :
python -m venv venv
On mac/linux: source venv/bin/activate  
On Windows: venv\Scripts\activate

# Install dependencies :
pip install -r requirements.txt

# Create & Update .env :
DISCORD_TOKEN=your_discord_bot_token
TARGET_CHANNEL_IDS=your_channel_ids
OPENAI_KEY=your_openai_api_key
EMAIL_USER=your_email
EMAIL_PASSWORD=your_email_password
EMAIL_TO=recipient_email

# start the bot and initiate database :
python discord_bot.py

# start the control pannel server to use UI:
streamlit run app.py

or 

# start it manually :
python scheduler.py



