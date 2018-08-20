from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import DeleteView
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm

def index(request):
    boards = Board.objects.all()
    return render(request, "index.html", {"boards": boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by("-last_updated").annotate(replies=Count("posts") - 1)
    return render(request, "topics.html", {"board": board, "topics": topics})


@login_required
def new_topic(request, pk):
	board = get_object_or_404(Board, pk=pk)
	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = request.user
			topic.save()
			Post.objects.create(
				message=form.cleaned_data.get("message"),
				topic=topic,
				created_by=request.user
			)
			return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
	else:
		form = NewTopicForm()
	return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, "topic_posts.html", {"topic": topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            return redirect("topic_posts", pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, "reply_topic.html", {"topic": topic, "form": form})

def delete_post(request, pk, topic_pk, post_pk):
    #post = get_object_or_404(Post, post.topic.board.pk=pk, post.topic.pk=topic_pk, pk=post_pk) 

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post successfully deleted!")
        return HttpResponseRedirect("index")

    return render(request, "post_delete.html")

