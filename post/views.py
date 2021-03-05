import json
from user.models import User
from .models import Post, Comment, Like, Archive
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


def addComment(request, id, redirectTo):
    post = get_object_or_404(Post, id = id)
    if request.method == "POST":
        comment_author = request.user
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)

        newComment.post = post
        newComment.save()

    user_id = post.user_id 
    user = User.objects.filter(id = user_id).first()
    username = user.username

    if redirectTo == 'index':
        return HttpResponseRedirect('index')
    elif redirectTo == 'profile':
        return HttpResponseRedirect(reverse('user:profile', args = {"username": username}))
    elif redirectTo == 'explore':
        return HttpResponseRedirect('explore')
    elif redirectTo == 'detail':
        return HttpResponseRedirect('/gönderi/%d/'%id)


def detail(request, id):
    post = get_object_or_404(Post, id = id)
    comments = post.comments.all()
    user = User.objects.filter(id = post.user_id).first()
    data = {
        "post": post,
        "comments": comments,
        "user": user,
    }
    return render(request, "detail.html", data)


def like(request, post_id):
    data = {
        'modalid': 'a{}'.format(post_id)
    }
    
    new_like, created = Like.objects.get_or_create(user = request.user, post_id = post_id)

    if not created:
        Like.objects.filter(post_id = post_id, user_id = request.user.id).delete()
    else:
        pass
    
    return JsonResponse(data)


def save_post_to_archive(request, post_id):
    data = {
        'modalid': 'a{}'.format(post_id)
    }

    post, created = Archive.objects.get_or_create(user = request.user, post_id = post_id)
    
    if not created:
        Archive.objects.filter(post_id = post_id, user_id = request.user.id).delete()
        data['durum'] = 'silindi'
    else:
        data['durum'] = 'eklendi'
    # print(data['modalid'])

    return JsonResponse(data)
