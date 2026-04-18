from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from pymongo import MongoClient

# Sample data
USERS = [
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
    {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "marvel"},
    {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
    {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
]

TEAMS = [
    {"name": "marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "spiderman@marvel.com"]},
    {"name": "dc", "members": ["batman@dc.com", "superman@dc.com", "wonderwoman@dc.com"]},
]

ACTIVITIES = [
    {"user_email": "ironman@marvel.com", "activity": "Running", "duration": 30},
    {"user_email": "batman@dc.com", "activity": "Cycling", "duration": 45},
]

LEADERBOARD = [
    {"team": "marvel", "points": 100},
    {"team": "dc", "points": 90},
]

WORKOUTS = [
    {"name": "Pushups", "difficulty": "easy"},
    {"name": "Squats", "difficulty": "medium"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient("mongodb://localhost:27017")
        db = client["octofit_db"]

        # Drop collections if exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
