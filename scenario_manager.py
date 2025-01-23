from datetime import datetime
from models import Scenario
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class ScenarioManager:
    def __init__(self, session: Session):
        self.session = session

    def add_scenario(self, data: dict, user: str) -> Scenario:
        """Add a new scenario"""
        try:
            scenario = Scenario(
                title=data['title'],
                category=data['category'],
                given=data['given'],
                when=data['when'],
                then=data['then'],
                circle=data['circle'],
                created_by=user
            )
            self.session.add(scenario)
            self.session.commit()
            logger.info(f"Added scenario: {scenario.title}")
            return scenario
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding scenario: {str(e)}")
            raise

    def get_scenarios(self, category: Optional[str] = None) -> List[Scenario]:
        """Get all scenarios with optional category filter"""
        query = self.session.query(Scenario)
        if category:
            query = query.filter(Scenario.category == category)
        scenarios = query.all()
        logger.info(f"Found {len(scenarios)} scenarios")
        return scenarios

    def update_scenario(self, scenario_id: int, data: dict, user: str) -> Scenario:
        """Update an existing scenario"""
        scenario = self.session.query(Scenario).filter(Scenario.id == scenario_id).first()
        if scenario:
            for key, value in data.items():
                setattr(scenario, key, value)
            scenario.last_updated = datetime.utcnow()
            self.session.commit()
        return scenario 