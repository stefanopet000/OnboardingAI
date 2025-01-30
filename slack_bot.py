from flask import Flask, request, abort
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from scenario_manager import ScenarioManager
from database import DatabaseManager
from fuzzywuzzy import fuzz
import os
import logging
import time
import hashlib
import hmac

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
flask_app = Flask(__name__)

class SlackBot:
    def __init__(self, bot_token):
        self.client = WebClient(token=bot_token)
        self.db_manager = DatabaseManager()
        self.conversations = {}  # Track active conversations
        
    def handle_message(self, event):
        try:
            user = event['user']
            channel = event['channel']
            
            # Track conversation state
            conv_key = f"{channel}:{user}"
            if conv_key not in self.conversations:
                self.conversations[conv_key] = {
                    'state': 'new',
                    'last_interaction': time.time()
                }
            
            message = event['text']
            thread_ts = event.get('thread_ts')  # Get thread timestamp if it exists
            
            # Get response from database
            response = self.get_scenario_response(message)
            
            # Send response in thread if it's a threaded message
            self.client.chat_postMessage(
                channel=channel,
                text=response,
                thread_ts=thread_ts if thread_ts else None
            )
            
        except SlackApiError as e:
            logger.error(f"Error sending message: {e.response['error']}")
        except KeyError as e:
            logger.error(f"Missing key in event data: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            self.client.chat_postMessage(
                channel=channel,
                text="Sorry, I encountered an error while processing your request."
            )

    def get_scenario_response(self, message):
        scenarios = []
        with next(self.db_manager.get_session()) as session:
            scenario_manager = ScenarioManager(session)
            scenarios = scenario_manager.get_scenarios()
            
            # Multiple matching attempts
            best_match = None
            highest_score = 0
            
            # Try exact match
            for scenario in scenarios:
                if message.lower() == scenario.title.lower():
                    return self.format_scenario_response(scenario)
            
            # Try fuzzy match
            for scenario in scenarios:
                # Try title
                title_score = fuzz.ratio(message.lower(), scenario.title.lower())
                # Try content
                content_score = fuzz.ratio(message.lower(), 
                    f"{scenario.given} {scenario.when} {scenario.then}".lower())
                
                score = max(title_score, content_score)
                if score > highest_score:
                    highest_score = score
                    best_match = scenario

    def send_message(self, channel, text, thread_ts=None, retries=3):
        try:
            return self.client.chat_postMessage(
                channel=channel,
                text=text or "No content available",  # Ensure text is never empty
                thread_ts=thread_ts,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": text or "No content available"
                        }
                    }
                ]
            )
        except SlackApiError as e:
            logger.error(f"Error sending message: {e.response['error']}")
            if e.response['error'] == 'account_inactive':
                logger.error("Bot token is inactive. Please reinstall the app and update the token.")
            raise

    def cleanup_old_conversations(self):
        current_time = time.time()
        expired_convs = []
        
        for conv_key, conv_data in self.conversations.items():
            # Remove conversations inactive for more than 30 minutes
            if current_time - conv_data['last_interaction'] > 1800:
                expired_convs.append(conv_key)
        
        for conv_key in expired_convs:
            del self.conversations[conv_key]

def verify_slack_request(request):
    try:
        # Get Slack signing secret
        signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
        if not signing_secret:
            logger.error("Missing Slack signing secret")
            return False
        
        # Get timestamp and signature from headers
        timestamp = request.headers.get('X-Slack-Request-Timestamp', '')
        slack_signature = request.headers.get('X-Slack-Signature', '')
        
        # Debug logging
        logger.info(f"Timestamp: {timestamp}")
        logger.info(f"Slack Signature: {slack_signature}")
        logger.info(f"Signing Secret length: {len(signing_secret)}")
        
        if not timestamp or not slack_signature:
            logger.error("Missing timestamp or signature")
            return False
        
        # Check if timestamp is too old
        current_time = time.time()
        if abs(current_time - int(timestamp)) > 60 * 5:
            logger.error(f"Request timestamp too old. Current: {current_time}, Request: {timestamp}")
            return False
        
        # Create base string
        req_body = request.get_data().decode()
        base_string = f'v0:{timestamp}:{req_body}'.encode('utf-8')
        logger.info(f"Base string: {base_string}")
        
        # Create signature
        my_signature = 'v0=' + hmac.new(
            signing_secret.encode('utf-8'),
            base_string,
            hashlib.sha256
        ).hexdigest()
        
        # Debug logging
        logger.info(f"Generated Signature: {my_signature}")
        logger.info(f"Received Signature: {slack_signature}")
        
        # Compare signatures
        is_valid = hmac.compare_digest(my_signature, slack_signature)
        logger.info(f"Signature valid: {is_valid}")
        return is_valid
        
    except Exception as e:
        logger.error(f"Error verifying request: {str(e)}")
        return False

# Flask routes
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # Add debug logging
    logger.info("Received request to /slack/events")
    logger.info(f"Headers: {dict(request.headers)}")
    
    # Verify request is from Slack
    if not verify_slack_request(request):
        logger.error("Request verification failed")
        abort(403)
    
    data = request.json
    logger.info(f"Request data: {data}")
    
    # Handle URL verification
    if data.get("type") == "url_verification":
        return {"challenge": data["challenge"]}
    
    # Handle events
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        if event.get("type") == "message":
            bot.handle_message(event)
    
    return "", 200

if __name__ == "__main__":
    bot_token = os.environ.get("SLACK_BOT_TOKEN")
    
    if not bot_token:
        logger.error("Missing Slack bot token in environment variables")
        raise ValueError("Missing Slack bot token")
    
    logger.info("Initializing Slack bot...")
    bot = SlackBot(bot_token)
    
    # Run Flask app
    flask_app.run(host="0.0.0.0", port=3000, debug=True)