from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from main import FAQAssistant
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlackBot:
    def __init__(self, bot_token, app_token):
        self.app = App(token=bot_token)
        self.app_token = app_token
        self.faq_assistant = FAQAssistant(
            ruby_file="data/scenarios.rb",
            json_file="data/scenarios.json"
        )
        
        @self.app.message("")
        def handle_message(message, say):
            logger.info(f"Received message: {message}")
            question = message["text"]
            logger.info(f"Processing question: {question}")
            answer = self.faq_assistant.get_answer(question)
            logger.info(f"Sending answer: {answer}")
            say(answer)
            
    def start(self):
        logger.info("Starting Slack bot...")
        handler = SocketModeHandler(app=self.app, app_token=self.app_token)
        handler.start()

if __name__ == "__main__":
    bot_token = os.environ.get("SLACK_BOT_TOKEN")
    app_token = os.environ.get("SLACK_APP_TOKEN")
    
    if not bot_token or not app_token:
        logger.error("Missing Slack tokens in environment variables")
        raise ValueError("Missing Slack tokens in environment variables")
    
    logger.info("Initializing Slack bot...")
    bot = SlackBot(bot_token, app_token)
    bot.start() 