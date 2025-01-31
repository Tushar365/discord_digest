import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from summary_engine import generate_summary
from email_sender import send_email
import argparse
from datetime import datetime, timezone

def daily_job():
    try:
        print(f"Starting digest job at {datetime.now()}")
        summary = generate_summary()
        send_email(summary)
        print("Digest sent successfully!")
    except Exception as e:
        print(f"Error in daily job: {e}")

def get_next_email_time(timezone='Asia/Kolkata', hour=22, minute=53): ## update the time and zone here
    # Validate and set timezone
    try:
        selected_tz = pytz.timezone(timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Invalid timezone: {timezone}. Defaulting to Kolkata.")
        selected_tz = pytz.timezone('Asia/Kolkata')  ## update the time and zone here
    
    # Create a scheduler with the selected timezone
    scheduler = BlockingScheduler(timezone=selected_tz)
    
    # Get current time in selected timezone
    now = datetime.now(selected_tz)
    #now = datetime.now(selected_tz.utc)
    
    # Schedule job at specified time
    trigger = CronTrigger(hour=hour, minute=minute)
    next_run = trigger.get_next_fire_time(None, now)
    
    return {
        'next_email_time': next_run,
        'time_until_next_email': next_run - now,
        'timezone': str(selected_tz)
    }

def main():
    parser = argparse.ArgumentParser(description='Discord Message Digest Scheduler')
    parser.add_argument('--test', action='store_true', help='Run job immediately')
    parser.add_argument('--preview', action='store_true', help='Show next email time')
    parser.add_argument('--timezone', type=str, default='Asia/Kolkata', 
                        help='Timezone for scheduling (e.g., America/Los_Angeles)')
    args = parser.parse_args()

    if args.preview:
        next_email_info = get_next_email_time(args.timezone)
        print(f"Next email will be sent at: {next_email_info['next_email_time']}")
        print(f"Time until next email: {next_email_info['time_until_next_email']}")
        print(f"Timezone: {next_email_info['timezone']}")
        return

    # Use the specified timezone or default to Kolkata
    scheduler_tz = pytz.timezone(args.timezone)
    scheduler = BlockingScheduler(timezone=scheduler_tz)

    if args.test:
        daily_job()
    else:
        scheduler.add_job(
            daily_job, 
            CronTrigger(hour=22, minute=53), ## update the time and zone here
            id='daily_digest'
        )

    print(f"Scheduler started at {datetime.now()}")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('\nScheduler stopped.')

if __name__ == "__main__":
    main()