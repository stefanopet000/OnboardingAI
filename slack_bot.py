from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from scenario_manager import ScenarioManager
from database import DatabaseManager
from fuzzywuzzy import fuzz
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlackBot:
    def __init__(self, bot_token, app_token):
        self.app = App(token=bot_token)
        self.app_token = app_token
        self.db_manager = DatabaseManager()  # Will use env variables from docker-compose
        
        @self.app.message("")
        def handle_message(message, say):
            try:
                with next(self.db_manager.get_session()) as session:
                    scenario_manager = ScenarioManager(session)
                    question = message["text"]
                    scenarios = scenario_manager.get_scenarios()
                    
                    # Find best match using fuzzy matching
                    best_match = None
                    highest_score = 0
                    
                    for scenario in scenarios:
                        score = fuzz.ratio(question.lower(), scenario.title.lower())
                        if score > highest_score:
                            highest_score = score
                            best_match = scenario
                    
                    if best_match and highest_score > 70:
                        response = (
                            f"Based on the scenario '{best_match.title}':\n"
                            f"Given {best_match.given}\n"
                            f"When {best_match.when}\n"
                            f"Then {best_match.then}"
                        )
                        say(response)
                    elif highest_score > 0:
                        say("I found a similar scenario but I'm not confident enough. Could you rephrase your question?")
                    else:
                        say("Sorry, I couldn't find a matching scenario.")
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
                say("Sorry, I encountered an error.")
            
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