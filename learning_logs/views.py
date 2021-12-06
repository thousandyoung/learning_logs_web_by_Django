from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
import markdown
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
import re


# Create your views here.
def index(request):
    """主页"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def search_entry(request):
    entries = Entry.objects.order_by('date_added')
    search = request.GET.get('search')
    tag = request.GET.get('tag')

    # 标签查询集
    if tag and tag != 'None':
        entries = Entry.objects.filter(tags__name__in=[tag])

    if search:
        entries = Entry.objects.filter(
            Q(title__icontains=search) | Q(body__icontains=search) | Q(tags__in=[tag])
        ).order_by('date_added')
    else:
        search = ''



    paginator = Paginator(entries, 5)
    page = request.GET.get('page')
    entry_page = paginator.get_page(page)
    context = {'entries': entries, 'entry_page': entry_page, 'search': search, 'tag': tag}
    return render(request, 'learning_logs/search_result.html', context)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('date_added')
    paginator = Paginator(entries, 5)
    page = request.GET.get('page')
    entry_page = paginator.get_page(page)
    context = {'topic': topic, 'entries': entries, 'entry_page': entry_page}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """add new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            # save（） provides a new database object
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """在特定主题中添加条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm
    else:
        # POST
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            topic.entry_num += 1
            topic.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            # form.save_m2m()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def show_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    entry.text = markdown.markdown(entry.text, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',

    ])
    context = {'entry':entry}
    return render(request, 'learning_logs/show_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    result = entry.delete()
    topic.entry_num -= 1
    topic.save()
    if result:
        return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    else:
        return HttpResponse("failed to delete entry")


@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.entry_set.all().delete()
    result = topic.delete()
    if result:
        return HttpResponseRedirect(reverse('learning_logs:topics'))
    else:
        return HttpResponse("failed to delete topic")
