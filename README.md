# Test Scenarios Bot

A Slack bot that helps teams access and query test scenarios stored in a database. The bot uses fuzzy matching to find and return relevant test scenarios based on user queries.

## Prerequisites

- Docker and Docker Compose
- Python 3.12
- A Slack workspace with admin permissions
- Slack Bot Token and App Token

## Slack App Setup

1. Go to [Slack API](https://api.slack.com/apps)
2. Create New App > From scratch
3. Add the following OAuth Scopes:
   - `chat:write`
   - `app_mentions:read`
   - `channels:join`
   - `channels:history`
4. Install the app to your workspace
5. Copy the Bot User OAuth Token (`xoxb-...`)
6. Enable Socket Mode and copy the App-Level Token (`xapp-...`)

## Project Setup

1. Clone the repository:
   bash
   git clone <repository-url>
   cd <repository-name>

2. Create a `.env` file in the project root:
   env
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_NAME=scenarios_db

3. Build and start the containers:
   bash
   docker-compose up --build

## Project Structure

.
├── Dockerfile # Docker configuration for the app
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── models.py # Database models
├── database.py # Database connection management
├── scenario_manager.py # Scenario operations
├── scenario_parser.py # Ruby file parser
├── upload_scenarios.py # CLI tool for uploads
└── slack_bot.py # Slack bot implementation

## Usage

### Managing Scenarios

1. Download your scenario file from Linear (Ruby format)

2. Upload scenarios to the database:
   bash
   Connect to the slackbot container
   docker-compose exec slackbot bash
   Inside the container
   python upload_scenarios.py /app/path/to/scenarios.rb

When prompted:

- Enter the circle name (team/group responsible)
- Enter the project name

### Using the Slack Bot

1. Invite the bot to your channel:
   /invite @scenarioBot

2. Ask questions about scenarios
   - The bot uses fuzzy matching to find relevant scenarios
   - Matches with >70% confidence will return the full scenario
   - Lower confidence matches will ask for clarification

### Database Management

View scenarios in the database:
bash
Connect to PostgreSQL
docker-compose exec db psql -U postgres -d scenarios_db
List all scenarios
SELECT FROM scenarios;

## Development

### Local Development Setup

1. Install dependencies:
   bash
   pip install -r requirements.txt

2. Run PostgreSQL locally or via Docker:

⌘K to generate a command
I need to make a couple of changes: fist of instead of "team name" I want to use "circle name" and then each circle is allowed to see all scenario, I don't want to block people. so everything is available to everyone

Let's update the code to reflect these changes:
First, update models.py to change "team" to "circle":
}
Update upload_scenarios.py:
)
Update scenario_manager.py:
scenarios
Since you want all scenarios to be available to everyone, I:
Renamed "team" to "circle" throughout the code
Removed team/circle filtering from get_scenarios
Kept category filtering as it might still be useful for organization
You'll need to recreate your database tables after these changes since we modified the schema. You can do this by:
;
Then restart your application to create the new table structure.
I want to add the database to docker too. How do I do that? the goal is that this app and its database lives together and can be started together when docker is initialized

Yes, let's containerize both the application and database together using Docker Compose. Here's how:
First, update the docker-compose.yml:
:
Update database.py to add retry logic for database connection:
)
Now you can:
Start everything with:
build
Upload scenarios using:
rb
Check the database:
;
This setup:
Creates a persistent PostgreSQL database
Connects your application to it
Stores data even if containers are stopped
Makes both services start together
Handles database connection retries
Would you like me to explain any part in more detail?
now please update readme.md with the required steps to setup this project

Here's the updated README.md:
:
bash
git clone <repository-url>
cd <repository-name>
:
bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_NAME=scenarios_db
:
bash
docker-compose up --build
:
bash
Connect to the slackbot container
docker-compose exec slackbot bash
Inside the container, run:
python upload_scenarios.py /app/path/to/your/scenarios.rb
:
/invite @your-bot-name
:
bash
Connect to the database
docker-compose exec db psql -U postgres -d scenarios_db
Inside psql
SELECT FROM scenarios;
Structure
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── models.py # Database models
├── database.py # Database connection
├── scenario_manager.py # Scenario operations
├── scenario_parser.py # Ruby file parser
├── upload_scenarios.py # CLI tool for uploads
└── slack_bot.py # Slack bot implementation
:
bash
docker-compose down
:
bash
docker-compose up --build
Request
This README provides:
Clear setup instructions
Usage examples
Development guidelines
Troubleshooting tips
Project structure overview
Would you like me to expand on any section?
in dockerFile I am missing the tokens for slackbot because they are in .env, why is docker file asking to store them there instead of using .env?

You're right! We should remove those environment variables from the Dockerfile since they're already in the .env file and docker-compose.yml. Let's update the Dockerfile:
]
The environment variables in the Dockerfile were redundant because:
Docker Compose loads variables from .env file
We pass them to the container through the environment section in docker-compose.yml
It's better practice to keep sensitive data like tokens out of the Dockerfile
This way:
Tokens stay secure in .env (which should be in .gitignore)
Configuration is more flexible
We follow Docker best practices
so if I do docker-compose down, will this destroy the db I just created? or will the database remain even when docker container is removed?

The database will persist even after docker-compose down because we're using a named volume (postgres_data) in our docker-compose.yml:
:
However, there are different commands that affect the data differently:
docker-compose down: Stops and removes containers, but preserves volumes
Database data is preserved
You can restart with docker-compose up and data will still be there
docker-compose down -v: Stops containers AND removes volumes
This WILL delete your database data
Use this only when you want to start completely fresh
docker-compose stop: Just stops containers
Everything is preserved
Can be restarted with docker-compose start
To verify your data is persisting:
"
The data should still be there unless you explicitly remove the volume with the -v flag.
do I need to run docker-compose build?

You need to run docker-compose build only when:
You make changes to:
Dockerfile
requirements.txt
Any files that are COPYed into the container during build
You don't need to run build when:
Making changes to Python files (since we're using volumes)
Starting/stopping containers
Database changes
Environment variable changes
Quick reference:
mounting
If you're unsure, using docker-compose up --build is safe - it will rebuild only if necessary.
I am still getting this, am I missing something here? I removed them drom docker file and they are in @.env

The error suggests that the environment variables aren't being properly loaded. Let's check a few things:
First, make sure your .env file is in the root directory and contains:
scenarios_db
Update docker-compose.yml to explicitly load all environment variables:
:
Verify the environment variables are being passed:
env
If you're still having issues, try:
recreate
Let me know if you still see the error after these changes.
@main.py do I need to make some change to this? based on latest setup of the application

You don't need main.py anymore since we've moved the functionality into other files. The main components are now:
slack_bot.py - Main entry point for the Slack bot
scenario_manager.py - Handles scenario operations
models.py - Database models
database.py - Database connection
However, I notice that slack_bot.py is looking for DATABASE_URL but we're not setting it. Let's update slack_bot.py:
)
Changes made:
Removed db_url parameter since we're using environment variables
Added error handling in message handler
Added temporary response for testing
Removed DATABASE_URL check since it's handled in DatabaseManager
You can safely remove main.py as it's no longer needed in the new architecture.
docker-compose up --build is failing because of this error

The error is because in your .env file you have DB_HOST=localhost, but in Docker, we need to use the service name as the host. Let's fix this:
Update .env:
scenarios_db
Also, let's update slack_bot.py to integrate the fuzzy matching from your main.py:
)
Key changes:
Changed database host to db (Docker service name)
Set database user and password to postgres
Integrated fuzzy matching from main.py
Added better response formatting
Now try:
build
This should resolve the connection error and give you a working Slack bot with fuzzy matching capabilities.
can you update README.md with all the steps and requirements needed for this project?

Here's a comprehensive README.md:
bash
git clone <repository-url>
cd <repository-name>
:
env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_NAME=scenarios_db
:
bash
docker-compose up --build

## Project Structure

.
├── Dockerfile # Docker configuration for the app
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── models.py # Database models
├── database.py # Database connection management
├── scenario_manager.py # Scenario operations
├── scenario_parser.py # Ruby file parser
├── upload_scenarios.py # CLI tool for uploads
└── slack_bot.py # Slack bot implementation
:
bash
Connect to the slackbot container
docker-compose exec slackbot bash
Inside the container
python upload_scenarios.py /app/path/to/scenarios.rb
:
/invite @your-bot-name 2. Ask questions about scenarios

- The bot uses fuzzy matching to find relevant scenarios
- Matches with >70% confidence will return the full scenario
- Lower confidence matches will ask for clarification

### Database Management

View scenarios in the database:
bash
Connect to PostgreSQL
docker-compose exec db psql -U postgres -d scenarios_db
List all scenarios
SELECT FROM scenarios;

## Development

### Local Development Setup

1. Install dependencies:
   bash
   pip install -r requirements.txt
2. Run PostgreSQL locally or via Docker:
   bash
   docker-compose up db

### Docker Commands

bash
Start services
docker-compose up
Rebuild services
docker-compose up --build
Stop services
docker-compose down
View logs
docker-compose logs -f
Remove volumes (will delete database)
docker-compose down -v

## Troubleshooting

### Common Issues

1. Database Connection Issues:

   - Check if database container is running: `docker-compose ps`
   - Verify database credentials in `.env`
   - Check database logs: `docker-compose logs db`

2. Slack Bot Not Responding:

   - Verify bot is in the channel
   - Check Slack tokens in `.env`
   - Check bot logs: `docker-compose logs slackbot`

3. Upload Issues:
   - Ensure correct file path inside container
   - Check file permissions
   - Verify database connection

## Dependencies

- `slack-bolt`: Slack API integration
- `sqlalchemy`: Database ORM
- `psycopg2`: PostgreSQL adapter
- `fuzzywuzzy`: String matching
- `python-dotenv`: Environment variable management
- `click`: CLI tool creation

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security Notes

- Never commit `.env` file
- Keep Slack tokens secure
- Use strong database passwords in production
- Consider adding rate limiting for production use
