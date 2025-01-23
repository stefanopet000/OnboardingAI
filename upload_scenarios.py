import click
import os
from dotenv import load_dotenv
from scenario_parser import ScenarioParser
from scenario_manager import ScenarioManager
from database import DatabaseManager

# Load environment variables from .env file
load_dotenv()

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--circle', prompt='Circle name', help='Circle responsible for these scenarios')
@click.option('--project', prompt='Project name', help='Project these scenarios belong to')
@click.option('--db-user', envvar='DB_USER', help='Database username')
def upload_scenarios(file_path, circle, project, db_user):
    """
    Upload scenarios from a Ruby file to the database.
    
    FILE_PATH: Path to the Ruby file containing scenarios
    """
    try:
        if not db_user:
            raise click.UsageError("Database username not provided. Set DB_USER environment variable or use --db-user option")
            
        # Initialize parser and database connection
        parser = ScenarioParser()
        db_manager = DatabaseManager()
        
        # Read and parse file
        click.echo(f"Reading file: {file_path}")
        with open(file_path, 'r') as f:
            content = f.read()
        
        scenarios = parser.parse_ruby_scenarios(content)
        click.echo(f"Found {len(scenarios)} scenarios")
        
        # Upload to database
        with next(db_manager.get_session()) as session:
            manager = ScenarioManager(session)
            added_scenarios = []
            
            with click.progressbar(scenarios) as scenario_bar:
                for scenario in scenario_bar:
                    scenario['circle'] = circle
                    added = manager.add_scenario(scenario, f"CLI Upload - {project}")
                    added_scenarios.append(added)
        
        click.echo(f"Successfully uploaded {len(added_scenarios)} scenarios")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    upload_scenarios() 