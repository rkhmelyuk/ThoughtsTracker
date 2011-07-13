
from pymongo import Connection
from pymongo import ASCENDING

class Tag:
    """
    The tag information: name and count
    """

    def __init__(self, name=None, count=None):
        self.name = name
        self.count = count


class TagManager:
    """
    Manager for tags. MongoDB is used to store tags.
    For tags collection the id is a tag (lowercase),
    while also have another attribute - 'count' - usage count of tag.
    """

    def __init__(self):
        self.db = Connection().thoughts
        self.db.tags.ensure_index("count")

    def pushTags(self, tags):
        """ Increment tags usage count """
        if tags: [self._incrementTagUsageCount(tag) for tag in tags if tag]


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

    def _readTag(self, found):
        return Tag(found.get('_id'), found.get('count'))
