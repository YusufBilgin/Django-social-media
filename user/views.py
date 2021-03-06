import urllib
from post.models import Post
from post.models import Comment, Like, Archive
from user.models import UserFollowing, Profile
from post.forms import PostForm
from user.forms import UpdateUser, UpdateProfile, RegisterForm, LoginForm
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect


def register_user(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()

        login(request, newUser)
        return HttpResponseRedirect("index")
    else:
        context = {
            "form": form
        }

        return render(request, "register.html", context)


def login_user(request):
    form = LoginForm(request.POST or None)

    data = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)

        if user is None:
            # messages.error(request, "Kullanıcı adı veya şifre hatalı")
            return render(request, "login.html", data)

        # messages.success(request, "Başarıyla giriş yaptınız")
        login(request, user)

        return HttpResponseRedirect("index")
    
    return render(request, "login.html", data)


def logout_user(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız")
    return redirect("index")


@login_required(login_url = "user:login")
def user_profile(request, username):
    form = PostForm(request.POST or None)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user

            # print(post.post_image.width / post.post_image.height)
            # print(post.modal_width)

            if post.post_image.width / post.post_image.height > 1.6:
                post.modal_width = 'xl'
            else:
                post.modal_width = 'lg'
            post.save()
            
            return HttpResponseRedirect(reverse('profile', kwargs={"username": username}))
    else:
        form = PostForm()

    user = User.objects.filter(username = username).first()
    profile = user.profile
    posts = Post.objects.filter(user = user)
    
    # Giris yapmis olan kullanicinin takip verileri
    query = UserFollowing.objects.filter(user_id_id = request.user.id).all().values_list('following_user_id_id')
    list_of_user_follows = list(list(query))
    output_list = [i[0] for i in list_of_user_follows]  # Kullanicinin takip ettigi hesaplari id bilgilerini iceren liste

    query = UserFollowing.objects.filter(following_user_id = request.user.id).all().values_list('user_id_id')
    list_of_user_followers = list(list(query))
    output_list2 = [i[0] for i in list_of_user_followers]  # Kullaniciyi takip edenlerin id bilgisini iceren liste

    # Kullanicinin girdigi profil kendisine mi ait (Cünkü ayarlar buttonunu göstermek icin)
    if user.id == request.user.id:
        is_user_profile = True
    else:
        is_user_profile = False


    # Eger kullanici baska birinin profilini ziyaret ediyorsa (takip edip etmedigini kontrol et)
    is_following = False
    if is_user_profile == False:
        if user.id in output_list:
            is_following = True
            # print("evet bu kullanici bu id yi takip ediyor")
        else:
            is_following = False
            # print("Hayir takip etmiyor")

    comments = Comment.objects.all()

    # Kullanicinin begendigi resimler
    query = Like.objects.filter(user_id = request.user.id).all().values_list('post_id')
    list_of_user_liked_posts = list(list(query))
    liked_posts = [i[0] for i in list_of_user_liked_posts]

    # Kullanicinin arsivledigi resimler
    query = Archive.objects.filter(user_id = request.user.id).all().values_list('post_id')
    list_of_archived_posts = list(list(query))
    archived_posts_as_list = [i[0] for i in list_of_archived_posts]

    data = {
        "user": user,
        "profile": profile,
        "posts": posts,
        "is_user_profile": is_user_profile,
        "is_following": is_following,
        "takip": len(output_list),
        "takipciler": len(output_list2),
        "form": form,
        "comments": comments,
        "user_liked_posts": liked_posts,
        "archived_posts": archived_posts_as_list,
    }

    messages.success(request, "Başarıyla Kayıt oldunuz")
    return render(request, "profile.html", data)


def follow_user(request, username):
    user = User.objects.filter(username = username).first()
    current_user = request.user
    a = UserFollowing.objects.filter(user_id_id = request.user.id).all().values_list('following_user_id_id')
    list_of_user_follows = list(list(a))
    output_list = [i[0] for i in list_of_user_follows]

    if user.id != current_user.id:
        if not (user.id in output_list):
            print("Takip edilmeye musait")
            UserFollowing.objects.create(user_id=current_user, following_user_id=user)
            return redirect(reverse('profile', kwargs={"username": username}))
        else:
            print("Anladigim kadariyla kullanici zaten takip ediliyor")
            # flash 
            return redirect(reverse('profile', kwargs={"username": username}))
    else:
        # Burda bir flash mesaji patlatacagiz.
        return redirect(reverse('profile', kwargs={"username": username}))


def unfollow(request, username):
    user = User.objects.filter(username = username).first()
    current_user = request.user
    query = UserFollowing.objects.filter(user_id_id = request.user.id).all().values_list('following_user_id_id')
    list_of_user_follows = list(list(query))
    output_list = [i[0] for i in list_of_user_follows]

    if user.id != current_user.id:
        if user.id in output_list:
            print("Takip edilmeye musait")
            UserFollowing.objects.filter(user_id=current_user, following_user_id=user).delete()
            return redirect(reverse('profile', kwargs={"username": username}))
        else:
            print("Anladigim kadariyla kullanici zaten takip ediliyor")
            # flash 
            return redirect(reverse('profile', kwargs={"username": username}))
    else:
        # Burda bir flash mesaji patlatacagiz.
        return redirect(reverse('profile', kwargs={"username": username}))


def user_update_profile(request):
    if request.method == "POST":
        user_form = UpdateUser(request.POST, instance=request.user)
        profile_form = UpdateProfile(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse("user:profile", kwargs = {"username": request.user.username}))
        else:
            print("Hata var")
    else:
        user_form = UpdateUser(instance=request.user)
        profile_form = UpdateProfile(instance=request.user.profile)
    
    return render(request, 'updateprofile.html', {
        'username': request.user.username,
        'user_form': user_form,
        'profile_form': profile_form,
    })

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def settings(request):
    return render(request, "settings.html")


def archive(request):

    user_archive = Archive.objects.filter(user = request.user).all()

    data = {
        "archives": user_archive,
    }

    return render(request, "archive.html", data)
