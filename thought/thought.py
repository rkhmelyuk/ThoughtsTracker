from bson.objectid import ObjectId
from datetime import datetime
from pymongo.errors import OperationFailure
from pymongo import DESCENDING
from pymongo import Connection
from tag import *

class Thought:
    def __init__(self, id=None, text=None, date=None, tags=None):
        self.id = id
        self.text = text
        self.date = date is not None and date or datetime.now()
        self.tags = tags

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

    def get_tags(self):
        return self.tags

    def set_tags(self, tags):
        self.tags = tags
        

class ThoughtManager:
    def __init__(self):
        self.db = Connection().thoughts
        self.tagManager = TagManager()

    def create(self, thought):
        id = self.db.thoughts.insert({
            "text": thought.get_text(),
            "date": thought.get_date(),
            "tags": thought.get_tags()
        })

        thought.set_id(id)
        self.tagManager.pushTags(thought.get_tags())

    def save(self, thought):
        existing_thought = self.get(thought.get_id())
        if existing_thought and existing_thought.get_tags():
            thoughtTagsSet = set(thought.get_tags())
            existingThoughtTagsSet = set(existing_thought.get_tags())

            addTags = thoughtTagsSet - existingThoughtTagsSet
            removeTags = existingThoughtTagsSet - thoughtTagsSet
        else:
            addTags = thought.get_tags()
            removeTags = None

        self.db.thoughts.update({"_id": thought.get_id()}, {
            "$set": {
                "text": thought.get_text(),
                "date": thought.get_date(),
                "tags": thought.get_tags()
            }
        }, upsert=True)

        addTags and self.tagManager.pushTags(addTags)
        removeTags and self.tagManager.removeTags(removeTags)

    def deleteById(self, id):
        try:
            thought = self.get(id)
            if thought is not None:
                self.db.thoughts.remove(ObjectId(id), safe=True)
                self.tagManager.removeTags(thought)
                return True
        except OperationFailure:
            print "Error to remove thought by id " + id

        return False

    def get(self, id):
        found = self.db.thoughts.find_one({"_id": ObjectId(id)})
        return self._readThought(found)

    def latest(self, limit):
        cursor = self.db.thoughts.find().sort("date", DESCENDING).limit(limit)
        return [self._readThought(doc) for doc in cursor]

    def searchByTag(self, tag, limit):
        cursor = self.db.thoughts.find({"tags": tag})
        cursor = cursor.sort("date", DESCENDING).limit(limit)
        return [self._readThought(doc) for doc in cursor]

    def _readThought(self, found):
        return Thought(
            found.get('_id'), found.get('text'),
            found.get('date'), found.get('tags'))
