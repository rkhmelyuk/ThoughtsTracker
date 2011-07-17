from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.conf import settings
from thought import *
from tag import *

def index(request):
    tags = TagManager().getTags()
    tagMax = tags and max([tag.count for tag in tags]) or 0
    thoughts = ThoughtManager().latest(settings.THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("latestPage", args=[1])

    return render(request, "thought/index.html",
            {'thoughts': thoughts, 'tags': tags, 'tagMax': tagMax,
             'showMore': showMore, 'loadMoreUrl': loadMoreUrl})


def latestPage(request, page):
    page = int(page)
    thoughts = ThoughtManager().latest(
        settings.THOUGHTS_PER_PAGE,
        skip=page * settings.THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("latestPage", args=[page + 1])

    return render(request, "thought/thoughts_page.html", {
        'thoughts': thoughts, "showMore": showMore,
        'loadMoreUrl': loadMoreUrl
    })


def post(request):
    thought = Thought()

    if request.method == 'POST':
        thought.text = request.POST.get('text')
        thought.date = datetime.now()
        thought.tags = getTagsList(request.POST.get('tags'))
        ThoughtManager().create(thought)

        return redirect('index')

    return render(request, "thought/post.html", {'thought': thought})


def edit(request, id):
    thought = ThoughtManager().get(id)

    if thought is None:
        raise Http404()

    if request.method == 'POST':
        thought.text = request.POST.get('text')
        thought.tags = getTagsList(request.POST.get('tags'))
        ThoughtManager().save(thought)

        return redirect('index')

    tags = (thought.get_tags() and ", ".join(thought.get_tags()) or "")
    return render(request, "thought/edit.html", {'thought': thought, 'tags': tags})


def thought(request, id):
    thought = ThoughtManager().get(id)
    return render(request, "thought/thought.html", {'thought': thought})


def remove(request, id):
    ThoughtManager().deleteById(id)
    return HttpResponseRedirect(reverse('index'))


def tag(request, tag):
    tags = TagManager().getTags()
    tagMax = tags and max([each.count for each in tags]) or 0
    thoughts = ThoughtManager().searchByTag(tag, settings.THOUGHTS_PER_PAGE)
    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("tagPage", args=[tag, 1])

    return render(request, "thought/tag.html", {
        "tag": tag, 'thoughts': thoughts, 'tags': tags,
        'tagMax': tagMax, 'showMore': showMore,
        'loadMoreUrl': loadMoreUrl
    })


def tagPage(request, tag, page):
    page = int(page)
    thoughts = ThoughtManager().searchByTag(
        tag, settings.THOUGHTS_PER_PAGE,
        skip=page * settings.THOUGHTS_PER_PAGE)

    showMore = len(thoughts) == settings.THOUGHTS_PER_PAGE
    loadMoreUrl = reverse("tagPage", args=[tag, page + 1])

    return render(request, "thought/thoughts_page.html", {
        'thoughts': thoughts,
        'showMore': showMore,
        'loadMoreUrl': loadMoreUrl
    })


def removeEmptyTag(tags):
    try:
        tags.remove("")
    except ValueError:
        pass


def parseTags(tagsText):
    tags = [tag.strip().lower() for tag in tagsText.split(",")]
    return tags


def getTagsList(tagsText):
    tags = parseTags(tagsText)
    removeEmptyTag(tags)
    tags.sort()

    return tags
