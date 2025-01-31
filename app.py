# app.py
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import pytz
from summary_engine import generate_summary
from scheduler import get_next_email_time
from email_sender import send_email
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Discord Digest Control Panel",
    layout="wide"
)

# Sidebar
st.sidebar.title("Discord Digest Controls")
page = st.sidebar.selectbox(
    "Select Page",
    ["Dashboard", "Message Viewer", "Email Controls"]
)

def load_messages(days=1):
    try:
        conn = sqlite3.connect('messages.db')
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = """
        SELECT content, author, timestamp, channel_id 
        FROM messages 
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
        """
        df = pd.read_sql_query(query, conn, params=(cutoff_date,))
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading messages: {e}")
        return pd.DataFrame(columns=['content', 'author', 'timestamp', 'channel_id'])

def generate_and_send_digest():
    with st.spinner('Generating digest...'):
        summary = generate_summary()
        st.text_area("Preview", summary, height=300)
        if st.button("Send Digest"):
            try:
                send_email(summary)
                st.success("Digest sent successfully!")
            except Exception as e:
                st.error(f"Failed to send digest: {e}")

def show_dashboard():
    st.title("Discord Digest Dashboard")
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        df = load_messages(1)
        st.metric("Messages Today", len(df))
        
    with col2:
        df_week = load_messages(7)
        st.metric("Messages This Week", len(df_week))
        
    with col3:
        unique_authors = df_week['author'].nunique()
        st.metric("Active Users", unique_authors)
    
    # Message Activity Chart
    st.subheader("Message Activity")
    if not df_week.empty:
        df_week['date'] = pd.to_datetime(df_week['timestamp']).dt.date
        daily_counts = df_week.groupby('date').size().reset_index(name='count')
        fig = px.line(daily_counts, x='date', y='count', title='Daily Message Count')
        st.plotly_chart(fig)
    
        # Most Active Users
        st.subheader("Most Active Users")
        user_counts = df_week['author'].value_counts().head(5)
        fig2 = px.bar(x=user_counts.index, y=user_counts.values, 
                     title='Most Active Users',
                     labels={'x': 'User', 'y': 'Messages'})
        st.plotly_chart(fig2)

def show_message_viewer():
    st.title("Message Viewer")
    
    days = st.slider("Select time range (days)", 1, 30, 1)
    df = load_messages(days)
    
    # Message filtering
    search_term = st.text_input("Search messages")
    if search_term:
        df = df[df['content'].str.contains(search_term, case=False, na=False)]
    
    # Display messages with all columns
    st.dataframe(df, height=500)
    
    # Export option
    if not df.empty and st.button("Export to CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            "discord_messages.csv",
            "text/csv"
        )

def show_email_controls():
    st.title("Email Controls")
    
    # # Timezone Selection
    # timezones = ['Asia/Kolkata', 'America/Los_Angeles']
    # selected_timezone = st.selectbox(
    #     "Select Timezone", 
    #     timezones, 
    #     index=0
    # )
    
    # # Time Selection
    # current_time = st.time_input(
    #     "Daily digest time",
    #     datetime.strptime("19:00", "%H:%M").time()
    # )
    
    # Next Mail Time Preview
    if st.button("Preview Next Mail Time"):
        try:
            next_email_info = get_next_email_time()
            st.success(f"Next email will be sent at: {next_email_info['next_email_time']}")
            st.info(f"Time until next email: {next_email_info['time_until_next_email']}")
            st.info(f"Timezone: {next_email_info['timezone']}")
        except Exception as e:
            st.error(f"Error calculating next mail time: {e}")
    
    # Manual digest generation
    st.subheader("Generate Manual Digest")
    generate_and_send_digest()
    
    if st.button("Update Schedule"):
        st.success(f"Schedule updated to {current_time} in {selected_timezone}")

# def show_settings():
#     st.title("Settings")
    
#     # Multi-Channel Configuration
#     st.subheader("Discord Channels")
#     channel_ids = st.text_area(
#         "Enter Channel IDs (comma-separated)", 
#         os.getenv('TARGET_CHANNEL_IDS', '')
#     )
    
#     if st.button("Save Channels"):
#         try:
#             # Validate channel IDs
#             channels = [ch.strip() for ch in channel_ids.split(',') if ch.strip()]
            
#             # Update .env file
#             with open('.env', 'r') as f:
#                 lines = f.readlines()
            
#             with open('.env', 'w') as f:
#                 for line in lines:
#                     if not line.startswith('TARGET_CHANNEL_IDS='):
#                         f.write(line)
#                 f.write(f"TARGET_CHANNEL_IDS={','.join(channels)}\n")
            
#             st.success(f"Saved {len(channels)} channels")
#         except Exception as e:
#             st.error(f"Error saving channels: {e}")

# Main content
if page == "Dashboard":
    show_dashboard()
elif page == "Message Viewer":
    show_message_viewer()
elif page == "Email Controls":
    show_email_controls()
# else:
#     show_settings()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Discord Digest Bot v1.0")