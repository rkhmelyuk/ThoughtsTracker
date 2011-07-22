from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.conf import settings
from thought.thought import *
from thought.dicontainer import CONTAINER

def index(request):
    tags = CONTAINER.getTagManager().getTags()
    tagMax = tags and max([tag.count for tag in tags]) or 0
    thoughts = CONTAINER.getThoughtManager().latest(settings.THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("latestPage", args=[1])

    return render(request, "thought/index.html",
            {'thoughts': thoughts, 'tags': tags, 'tagMax': tagMax,
             'showMore': showMore, 'loadMoreUrl': loadMoreUrl})


def latestPage(request, page):
    page = int(page)
    thoughts = CONTAINER.getThoughtManager().latest(
        settings.THOUGHTS_PER_PAGE,
        skip=page * settings.THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("latestPage", args=[page + 1])

    return render(request, "thought/thoughts_page.html", {
        'thoughts': thoughts, "showMore": showMore,
        'loadMoreUrl': loadMoreUrl
    })


def post(request):
    error = None
    thought = Thought()

    if request.method == 'POST':
        thought.text = request.POST.get('text')

        if thought.text:
            thought.date = datetime.now()
            thought.tags = getTagsList(request.POST.get('tags'))
            CONTAINER.getThoughtManager().create(thought)

            return redirect('index')
        else:
            error = "Thought shouldn't be empty, otherwise who may need it?"

    return render(request, "thought/post.html", {'thought': thought, 'error': error})


def edit(request, id):
    error = None
    thought = CONTAINER.getThoughtManager().get(id)

    if thought is None:
        raise Http404()

    if request.method == 'POST':
        thought.text = request.POST.get('text')
        if thought.text:
            thought.tags = getTagsList(request.POST.get('tags'))
            CONTAINER.getThoughtManager().save(thought)

            return redirect('index')
        else:
            error = "Thought shouldn't be empty, otherwise who may need it?"

    tags = (thought.get_tags() and ", ".join(thought.get_tags()) or "")
    return render(request, "thought/edit.html", {'thought': thought, 'tags': tags, 'error': error})


def thought(request, id):
    thought = CONTAINER.getThoughtManager().get(id)
    return render(request, "thought/thought.html", {'thought': thought})


def remove(request, id):
    CONTAINER.getThoughtManager().deleteById(id)
    return HttpResponseRedirect(reverse('index'))


def tag(request, tag):
    tags = CONTAINER.getTagManager().getTags()
    tagMax = tags and max([each.count for each in tags]) or 0
    thoughts = CONTAINER.getThoughtManager().searchByTag(tag, settings.THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("tagPage", args=[tag, 1])

    return render(request, "thought/tag.html", {
        "tag": tag, 'thoughts': thoughts, 'tags': tags,
        'tagMax': tagMax, 'showMore': showMore,
        'loadMoreUrl': loadMoreUrl
    })


def tagPage(request, tag, page):
    page = int(page)
    thoughts = CONTAINER.getThoughtManager().searchByTag(
        tag, settings.THOUGHTS_PER_PAGE,
        skip=page * settings.THOUGHTS_PER_PAGE)

    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("tagPage", args=[tag, page + 1])

    return render(request, "thought/thoughts_page.html", {
        'thoughts': thoughts,
        'showMore': showMore,
        'loadMoreUrl': loadMoreUrl
    })

def appSettings(request):
    return render(request, "thought/settings.html")


def getTagsList(tagsText):
    tags = parseTags(tagsText)
    removeEmptyTag(tags)
    tags.sort()

    return tags


def parseTags(tagsText):
    tags = [tag.strip().lower() for tag in tagsText.split(",")]
    return prepareTags(tags)

def prepareTags(tags):
    return [tag.lower().replace("/", "") for tag in tags]

def removeEmptyTag(tags):
    try:
        tags.remove("")
    except ValueError:
        pass
