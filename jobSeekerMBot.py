import logging
import requests
from telegram import Update
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime, timedelta

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = 'https://www.corporatestaffing.co.ke/category/it-jobs-in-kenya/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the first job and date
    job_list = soup.find('main', class_='content').find_all('article', class_='job_posting')
    today = datetime.now()
    job_found = False
    for job in job_list:
        date_str = job.find('time', class_='entry-time').text.strip()
        job_date = datetime.strptime(date_str, '%B %d, %Y')
        days_since_posted = (today - job_date).days
        if days_since_posted <= 30:
            job_title = job.h2.a.text.strip()
            job_link = job.h2.a['href']
            job_str = f"{job_title}\n{date_str}\n{job_link}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=job_str)
            job_found = True
            break
    
    if not job_found:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='No jobs found.')


if __name__ == '__main__':
    application = ApplicationBuilder().token('6079009912:AAHrPDtYOwLqUTq-xzF9PbLf1PwAb_tHm-s').build()
    
    start_handler = CommandHandler('search', start)
    application.add_handler(start_handler)
    
    application.run_polling()