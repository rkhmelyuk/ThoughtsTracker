from thought import ThoughtManager
from tag import TagManager
from mongo import MongoConnection
from django.conf import settings

class DIContainer:
    def __init__(self):
        self.mongoConnection = None
        self.tagManager = None
        self.thoughtManager = None

    def getThoughtManager(self):
        if self.thoughtManager is None:
            tagManager = self.getTagManager()
            mongoConnection = self.getMongoConnection()
            self.thoughtManager = ThoughtManager(mongoConnection, tagManager)

        return self.thoughtManager

    def getMongoConnection(self):
        if self.mongoConnection is None:
            self.mongoConnection = MongoConnection(
                host=settings.MONGODB_HOST,
                port=settings.MONGODB_PORT,
                database=settings.MONGODB_DATABASE)

        return self.mongoConnection

    def getTagManager(self):
        if self.tagManager is None:
            mongoConnection = self.getMongoConnection()
            self.tagManager = TagManager(mongoConnection)

        return self.tagManager


CONTAINER = DIContainer()

