from bson.objectid import ObjectId
from datetime import datetime
from django.db.models import permalink
from pymongo.errors import OperationFailure
from pymongo import DESCENDING

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

    @permalink
    def get_absolute_url(self):
        return "thought", None, {'id': str(self.id)}
        

class ThoughtManager:
    def __init__(self, mongoConnection, tagManager, study):
        self.db = mongoConnection.getDatabase()
        self.tagManager = tagManager
        self.study = study

    def create(self, thought):
        id = self.db.thoughts.insert({
            "text": thought.get_text().strip(),
            "date": thought.get_date(),
            "tags": thought.get_tags()
        })

        thought.set_id(id)
        self.tagManager.pushTags(thought.get_tags())
        self.study.learn(thought.get_tags(), thought.get_text())

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
                "text": thought.get_text().strip(),
                "date": thought.get_date(),
                "tags": thought.get_tags()
            }
        }, upsert=True)

        if addTags:
            self.tagManager.pushTags(addTags)
        if removeTags:
            self.tagManager.removeTags(removeTags)

        if existing_thought:
            self.study.forget(
                existing_thought.get_tags(),
                existing_thought.get_text())

        self.study.learn(thought.get_tags(), thought.get_text())

    def deleteById(self, id):
        try:
            thought = self.get(id)
            if thought is not None:
                self.db.thoughts.remove(ObjectId(id), safe=True)
                self.tagManager.removeTags(thought.get_tags())
                self.study.forget(thought.get_tags(), thought.get_text())
                return True
        except OperationFailure:
            print "Error to remove thought by id " + id

        return False

    def get(self, id):
        found = self.db.thoughts.find_one({"_id": ObjectId(id)})
        return found and self._readThought(found) or None

    def latest(self, limit, skip = 0):
        cursor = self.db.thoughts.find().sort("date", DESCENDING).skip(skip).limit(limit)
        return [self._readThought(doc) for doc in cursor]

    def searchByTag(self, tag, limit, skip = 0):
        cursor = self.db.thoughts.find({"tags": tag})
        cursor = cursor.sort("date", DESCENDING).skip(skip).limit(limit)
        return [self._readThought(doc) for doc in cursor]

    def _readThought(self, found):
        return Thought(
            found.get('_id'), found.get('text'),
            found.get('date'), found.get('tags'))
