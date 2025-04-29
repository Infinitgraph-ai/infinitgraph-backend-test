"""
This module generates fake data for the Infinitgraph.ai technical test.
It should not be modified by the candidate.
"""

import datetime
import random
from typing import List, Tuple
import uuid

from faker import Faker
from app.models import UserOut, AnalysisHistoryOut, UserRole, AnalysisType

fake = Faker()


class DataGenerator:
    """
    Generator for fake test data.
    
    This class provides methods to generate users and analysis history records
    for testing the API.
    
    Args:
        data_size (int): Number of records to generate
    """
    
    def __init__(self, data_size: int):
        self.data_size = data_size
        self.users = []
        self.history = []
        
    def generate_data(self) -> Tuple[List[UserOut], List[AnalysisHistoryOut]]:
        """
        Generate fake users and analysis history.
        
        Returns:
            Tuple containing lists of users and analysis history records
        """
        # Generate fake users
        self.users = self._generate_users()
        
        # Generate fake analysis history
        self.history = self._generate_analysis_history()
        
        return self.users, self.history
    
    def _generate_users(self) -> List[UserOut]:
        """Generate fake user data"""
        users = []
        
        # First user is always admin
        admin = UserOut(
            id=1,
            username="admin",
            email="admin@infinitgraph.ai",
            role=UserRole.ADMIN,
            is_active=True,
            created_at=fake.date_time_between(start_date="-1y", end_date="-6m")
        )
        users.append(admin)
        
        # Second user is always regular
        regular = UserOut(
            id=2,
            username="user",
            email="user@example.com",
            role=UserRole.USER,
            is_active=True,
            created_at=fake.date_time_between(start_date="-1y", end_date="-6m")
        )
        users.append(regular)
        
        # Generate random users
        for i in range(3, self.data_size + 1):
            role = random.choice([UserRole.USER, UserRole.USER, UserRole.USER, UserRole.ADMIN, UserRole.GUEST])
            user = UserOut(
                id=i,
                username=fake.user_name(),
                email=fake.email(),
                role=role,
                is_active=random.random() > 0.1,  # 90% are active
                created_at=fake.date_time_between(start_date="-1y", end_date="now")
            )
            users.append(user)
            
        return users
    
    def _generate_analysis_history(self) -> List[AnalysisHistoryOut]:
        """Generate fake analysis history data"""
        history = []
        
        # Generate between 1-5 history items per user
        for user in self.users:
            num_entries = random.randint(1, 5)
            
            for _ in range(num_entries):
                analysis_type = random.choice(list(AnalysisType))
                status = random.choice(["completed", "completed", "completed", "failed", "processing"])
                
                history_item = AnalysisHistoryOut(
                    id=len(history) + 1,
                    user_id=user.id,
                    text_sample=fake.text(max_nb_chars=100),
                    analysis_type=analysis_type,
                    status=status,
                    created_at=fake.date_time_between(start_date="-6m", end_date="now")
                )
                history.append(history_item)
                
        return history