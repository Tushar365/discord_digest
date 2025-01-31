# Clone repository (use cmd):
git clone https://github.com/Tushar365/discord_digest.git
cd discord_digest

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

# start the timer shedule manually :
set the timer and zone manually : scheduler.py (change the code)
python scheduler.py

# check time :
python scheduler.py --preview



