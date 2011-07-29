import math
from django.http import HttpResponse
from thought.dicontainer import CONTAINER

def searchTags(request, keyword):
    tags = CONTAINER.getTagManager().searchTags(keyword)
    tagNames = [tag.name for tag in tags]
    return HttpResponse(",".join(tagNames), content_type="text/plain")

def detectTags(request):
    text = request.POST.get("text")
    tagsCount = CONTAINER.getTagManager().tagsCount()
    minPart = calculateMinPart(tagsCount)
    tags = CONTAINER.getTagDetector().detect(text, limit=5, minPart = minPart)
    tagsNames = [tag.name for tag in tags]
    return HttpResponse(", ".join(tagsNames), content_type="text/plain")

def calculateMinPart(tagsCount):
    return float(math.sqrt(tagsCount)) / 15