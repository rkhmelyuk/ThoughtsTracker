from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from thought import *

def index(request):
    thoughts = ThoughtDao().latest(10)
    return render_to_response("thought/index.html", {'thoughts': thoughts})

def post(request):
    thought = Thought()

    if request.method == 'POST':
        thought.text = request.POST.get('text')
        thought.date = datetime.now()
        thought.tags = getTagsList(request.POST.get('tags'))
        ThoughtDao().create(thought)

        return HttpResponseRedirect(reverse('index'))

    return render_to_response("thought/post.html", {'thought': thought})

def edit(request, id):
    thought = ThoughtDao().get(id)

    if request.method == 'POST':
        thought.text = request.POST.get('text')
        thought.date = datetime.now()
        thought.tags = getTagsList(request.POST.get('tags'))
        ThoughtDao().save(thought)

        return HttpResponseRedirect(reverse('index'))

    tags = (thought.get_tags() and ", ".join(thought.get_tags()) or "")
    return render_to_response("thought/edit.html", {'thought': thought, 'tags': tags})

def remove(request, id):
    ThoughtDao().deleteById(id)
    return HttpResponseRedirect(reverse('index'))

def tag(request, tag):
    thoughts = ThoughtDao().searchByTag(tag, 10)
    return render_to_response("thought/tag.html", {'thoughts': thoughts})

def getTagsList(tagsText):
    return [tag.strip() for tag in tagsText.split(",")]
