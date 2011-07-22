from django.http import HttpResponse
from thought.dicontainer import CONTAINER

def searchTags(request, keyword):
    tags = CONTAINER.getTagManager().searchTags(keyword)
    tagNames = [tag.name for tag in tags]
    return HttpResponse(",".join(tagNames), content_type="text/plain")
