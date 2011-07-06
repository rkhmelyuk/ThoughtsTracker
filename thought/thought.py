from bson.objectid import ObjectId
from pymongo.errors import OperationFailure
from pymongo import DESCENDING

__author__ = 'ruslan'

from datetime import datetime
from pymongo import Connection

class Thought:
    def __init__(self, id=None, text=None, date=None):
        self.id = id
        self.text = text
        self.date = date is not None and date or datetime.now()

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def get_date(self):
        return self.date


class ThoughtDao:
    def __init__(self):
        self.db = Connection().thoughts

    def create(self, thought):
        id = self.db.thoughts.insert({
            "text": thought.get_text(),
            "date": thought.get_date()
        })
        
        thought.set_id(id)

    def save(self, thought):
        self.db.thoughts.update({"_id": thought.get_id()}, {
            "$set": {
                "text": thought.get_text(),
                "date": thought.get_date()
            }
        }, upsert = True)

    def deleteById(self, id):
        try:
            self.db.thoughts.remove(ObjectId(id), safe=True)
            return True
        except OperationFailure:
            print "Error to remove thought by id " + id
            return False

    def get(self, id):
        found = self.db.thoughts.find_one({"_id": ObjectId(id)})
        return Thought(found['_id'], found['text'], found['date'])

    def latest(self, num):
        cursor = self.db.thoughts.find().sort("date", DESCENDING).limit(num)
        latestThoughts = []
        for doc in cursor:
            thought = Thought(doc.get("_id"), doc.get("text"), doc.get("date"))
            latestThoughts.append(thought)

        return latestThoughts
