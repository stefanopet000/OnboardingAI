# Test Scenarios Bot

A Slack bot that helps teams access and query test scenarios stored in a database. The bot uses fuzzy matching to find and return relevant test scenarios based on user queries.

## System Requirements

1. Docker Engine

   - Linux: `sudo apt-get install docker-ce docker-ce-cli containerd.io`
   - Mac: Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
   - Windows: Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

2. Docker Compose

   - Usually comes with Docker Desktop
   - Linux: `sudo apt-get install docker-compose`

3. Python 3.12

   - Download from [python.org](https://www.python.org/downloads/)
   - Or use pyenv: `pyenv install 3.12`

4. pip (Python package manager)

   - Comes with Python installation
   - Upgrade: `python -m pip install --upgrade pip`

5. PostgreSQL client (optional, for direct database access)

   - Linux: `sudo apt-get install postgresql-client`
   - Mac: `brew install postgresql`
   - Windows: Included with PostgreSQL installation

6. Slack workspace with admin permissions & Slack Bot Token and App Token

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
