from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from settings import THOUGHTS_PER_PAGE
from thought import *
from tag import *


def index(request):
    tags = TagManager().getTags()
    tagMax = tags and max([tag.count for tag in tags]) or 0
    thoughts = ThoughtManager().latest(THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("latestPage", args=[1])

    return render_to_response("thought/index.html",
            {'thoughts': thoughts, 'tags': tags, 'tagMax': tagMax,
             'showMore': showMore, 'loadMoreUrl': loadMoreUrl})


def latestPage(request, page):
    page = int(page)
    thoughts = ThoughtManager().latest(
        THOUGHTS_PER_PAGE, skip=page * THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("latestPage", args=[page + 1])

    return render_to_response("thought/thoughts_page.html",
            {'thoughts': thoughts, "showMore": showMore,
             'loadMoreUrl': loadMoreUrl})


def post(request):
    thought = Thought()

    if request.method == 'POST':
        thought.text = request.POST.get('text')
        thought.date = datetime.now()
        thought.tags = getTagsList(request.POST.get('tags'))
        ThoughtManager().create(thought)

        return HttpResponseRedirect(reverse('index'))

    return render_to_response("thought/post.html", {'thought': thought})


def edit(request, id):
    thought = ThoughtManager().get(id)

    if request.method == 'POST':
        thought.text = request.POST.get('text')
        thought.tags = getTagsList(request.POST.get('tags'))
        ThoughtManager().save(thought)

        return HttpResponseRedirect(reverse('index'))

    tags = (thought.get_tags() and ", ".join(thought.get_tags()) or "")
    return render_to_response("thought/edit.html", {'thought': thought, 'tags': tags})


def thought(request, id):
    thought = ThoughtManager().get(id)
    return render_to_response("thought/thought.html", {'thought': thought})


def remove(request, id):
    ThoughtManager().deleteById(id)
    return HttpResponseRedirect(reverse('index'))


def tag(request, tag):
    tags = TagManager().getTags()
    tagMax = tags and max([each.count for each in tags]) or 0
    thoughts = ThoughtManager().searchByTag(tag, THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("tagPage", args=[tag, 1])

    return render_to_response("thought/tag.html", {
        "tag": tag, 'thoughts': thoughts, 'tags': tags,
        'tagMax': tagMax, 'showMore': showMore,
        'loadMoreUrl': loadMoreUrl})


def tagPage(request, tag, page):
    page = int(page)
    thoughts = ThoughtManager().searchByTag(
        tag, THOUGHTS_PER_PAGE, skip=page * THOUGHTS_PER_PAGE)

    showMore = len(thoughts) == THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("tagPage", args=[tag, page + 1])

    return render_to_response("thought/thoughts_page.html", {
        'thoughts': thoughts, 'showMore': showMore, 'loadMoreUrl': loadMoreUrl})


def getTagsList(tagsText):
    tags = [tag.strip().lower() for tag in tagsText.split(",")]
    tags.sort()

    return tags
