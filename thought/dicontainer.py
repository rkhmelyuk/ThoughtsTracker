from tagdetector.detector import TagDetector
from tagdetector.reader import TextReader
from tagdetector.storage.storage import Storage
from tagdetector.tagstudy import TagStudy
from thought import ThoughtManager
from tag import TagManager
from mongo import MongoConnection
from django.conf import settings

class DIContainer:
    
    def __init__(self):
        self.mongoConnection = None
        self.tagManager = None
        self.thoughtManager = None
        self.tagstudy = None
        self.tagDetector = None

    def getThoughtManager(self):
        if self.thoughtManager is None:
            tagManager = self.getTagManager()
            mongoConnection = self.getMongoConnection()
            calculator = self.getTagStudy()
            self.thoughtManager = ThoughtManager(mongoConnection, tagManager, calculator)

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

    def getTagStudy(self):
        if self.tagstudy is None:
            mongoConnection = self.getMongoConnection()
            storage = Storage(mongoConnection)
            self.tagstudy = TagStudy(storage, TextReader())

        return self.tagstudy

    def getTagDetector(self):
        if self.tagDetector is None:
            mongoConnection = self.getMongoConnection()
            storage = Storage(mongoConnection)
            self.tagDetector = TagDetector(storage, TextReader())

        return self.tagDetector


CONTAINER = DIContainer()

