import schedule
import time
import logging
from fetch_news import fetch_ai_news

# Set up logging to track background activity
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def update_job():
    """Wrapper function to execute the fetch and log the results."""
    logging.info("Starting scheduled AI news fetch...")
    try:
        # Calls the function we built in fetch_news.py
        fetch_ai_news() 
        logging.info("Scheduled fetch completed successfully.")
    except Exception as e:
        logging.error(f"Error during scheduled fetch: {e}")

def main():
    logging.info("Initializing AI News Scheduler. Task set to run every 30 minutes.")
    
    # Optional: Run the job immediately upon startup so you don't have to wait 30 minutes
    update_job()
    
    # Schedule the job to run every 30 minutes
    schedule.every(30).minutes.do(update_job)
    
    # Infinite loop to keep the scheduler alive
    try:
        while True:
            schedule.run_pending()
            # Sleep for 60 seconds between checks to save CPU cycles
            time.sleep(60) 
    except KeyboardInterrupt:
        logging.info("Scheduler manually stopped by user.")

if __name__ == "__main__":
    main()