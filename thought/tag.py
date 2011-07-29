from pymongo import ASCENDING

class Tag:
    """
    The tag information: name and count
    """

    def __init__(self, name=None, count=None, color=None):
        self.name = name
        self.count = count
        self.color = color


class TagManager:
    """
    Manager for tags. MongoDB is used to store tags.
    For tags collection the id is a tag (lowercase),
    while also have another attribute - 'count' - usage count of tag.
    """

    def __init__(self, mongoConnection):
        self.db = mongoConnection.getDatabase()
        self.db.tags.ensure_index("count")

    def searchTags(self, keyword, limit=10):
        """ Search tag that equal or starts with specified keyword """
        keywordReg = '^' + keyword.lower() + '.*$'
        cursor = self.db.tags.find({'_id': {'$regex': keywordReg}}).limit(limit)
        return [self._readTag(doc) for doc in cursor]

    def pushTags(self, tags):
        """ Increment tags usage count """
        if tags: [self._incrementTagUsageCount(tag) for tag in tags if tag]

    def setTagColor(self, tag, color):
        self.db.tags.update({"_id": tag}, {"$set": {"color": color}}, upsert=True)

    def removeTags(self, tags):
        """ Decrement tags usage count """
        if tags:
            [self._decrementTagUsageCount(tag) for tag in tags if tag]
            self._removeNotUsedTags()

    def _incrementTagUsageCount(self, tag):
        self.db.tags.update({"_id": tag}, {"$inc": {"count": 1}}, True)

    def _decrementTagUsageCount(self, tag):
        self.db.tags.update({"_id": tag}, {"$inc": {"count": -1}}, True)

    def _removeNotUsedTags(self):
        """ Remove tags with usage count <= 0 """
        self.db.tags.remove({"count": {"$lte": 0}})

    def getTags(self):
        cursor = self.db.tags.find().sort("_id", ASCENDING)
        return [self._readTag(doc) for doc in cursor]

    def tagsCount(self):
        return self.db.tags.count()

    def _readTag(self, found):
        return Tag(
            found.get('_id'),
            found.get('count'), 
            found.get('color'))
