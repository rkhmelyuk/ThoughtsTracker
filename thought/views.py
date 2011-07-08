from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from thought import *
from tag import *

def index(request):
    tags = TagManager().getTags()
    thoughts = ThoughtManager().latest(10)
    return render_to_response("thought/index.html",
            {'thoughts': thoughts, 'tags': tags})


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


def remove(request, id):
    ThoughtManager().deleteById(id)
    return HttpResponseRedirect(reverse('index'))


def tag(request, tag):
    tags = TagManager().getTags()
    thoughts = ThoughtManager().searchByTag(tag, 10)
    return render_to_response("thought/tag.html", {"tag": tag, 'thoughts': thoughts, 'tags': tags})


def getTagsList(tagsText):
    tags = [tag.strip().lower() for tag in tagsText.split(",")]
    tags.sort()

    return tags
