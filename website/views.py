from random import shuffle
from user.models import User
from post.forms import PostForm
from user.models import UserFollowing
from post.models import Post, Like, Comment, Archive
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.images import get_image_dimensions



@login_required(login_url = "user:login")
def index(request):
    form = PostForm(request.POST or None)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user
            
            if post.post_image.width / post.post_image.height > 1.6:
                post.modal_width = 'xl'
            else:
                post.modal_width = 'lg'
            post.save()
            
            return HttpResponseRedirect(reverse('index'))   # we should always return an HttpResponseRedirect after successfully dealing with POST data.
                                                            # it’s a good Web development practice in general.
    else:
        form = PostForm()

    # Get a list of what the user is following
    query = UserFollowing.objects.filter(user_id_id = request.user.id).all().values_list('following_user_id_id')
    list_of_user_follows = list(list(query))
    output_list = [i[0] for i in list_of_user_follows]
    output_list.append(request.user.id)

    # User-liked posts
    query = Like.objects.filter(user_id = request.user.id).all().values_list('post_id')
    list_of_user_liked_posts = list(list(query))
    output_list2 = [i[0] for i in list_of_user_liked_posts]   # Posts that will appear on the homepage

    # User archived images
    query = Archive.objects.filter(user_id = request.user.id).all().values_list('post_id')
    list_of_archived_posts = list(list(query))
    archived_posts_as_list = [i[0] for i in list_of_archived_posts]
    # print(archived_posts_as_list)

    posts = Post.objects.filter(are_the_categories_set = 1).all()

    user_liked_pictures = []

    id_list = []
    new_list = []
    for i in posts:
        if i.user_id in output_list:
            new_list.append(i)
    
    for i in new_list:
        id_list.append(i.id)

    for i in id_list:
        if i in output_list2:
            user_liked_pictures.append(i)

    user = request.user

    # print(id_list)
    # print(output_list2)
    # print(user_liked_pictures)

    data = {
        "user": user,
        "form": form,
        "posts": new_list,
        "user_liked_posts": user_liked_pictures,
        "archived_posts": archived_posts_as_list,
    }
    return render(request, "index.html", data)


def search(request):
    if request.method == "POST":
        user_keyword = request.POST["keyword"]

        data = {
            "user_keyword": user_keyword,
        }

        if user_keyword != "" :    
            users = User.objects.filter(username__contains = user_keyword).all()
            data["users"] = users
            
        return render(request, "usersearch.html", data)
    elif request.method == "GET":
        return redirect("index")


def explore(request):
    all_posts = Post.objects.all().values_list('id')
    all_posts = list(list(all_posts))
    all_posts = [i[0] for i in all_posts]
    shuffle(all_posts)

    posts = []

    for i in all_posts:
        post = Post.objects.filter(id = i).first()
        if post.are_the_categories_set == 1:
            posts.append(post)

    # User-liked posts
    query = Like.objects.filter(user_id = request.user.id).all().values_list('post_id')
    list_of_user_liked_posts = list(list(query))
    liked_posts = [i[0] for i in list_of_user_liked_posts]

    # User archived images
    query = Archive.objects.filter(user_id = request.user.id).all().values_list('post_id')
    list_of_archived_posts = list(list(query))
    archived_posts_as_list = [i[0] for i in list_of_archived_posts]
    
    # print(liked_posts)

    data = {
        "user": request.user,
        "profile": request.user.profile,
        "posts": posts,
        "comments": Comment.objects.all(),
        "user_liked_posts": liked_posts,
        "archived_posts": archived_posts_as_list,
    }

    return render(request, "explore.html", data)
