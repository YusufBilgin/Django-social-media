from django.contrib import admin
from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path('', views.all_users, name = "all_users"),
    path('kayıt-ol/', views.register_user, name = "register"),
    path('giriş-yap/', views.login_user, name = "login"),
    path('çıkış-yap/', views.logout_user, name = "logout"),
    path('profil/<str:username>/', views.user_profile, name = "profile"),
    path('güncelle/', views.user_update_profile, name = "updateProfile"),
    path('ayarlar/', views.settings, name = "settings"),
    path('arşiv/', views.archive, name = "Archive"),
    path('takip-et/<str:username>/', views.follow_user, name = "followUser"),
    path('takipten-çık/<str:username>/', views.unfollow, name = "unfollow"),
    path('ajax/kullanıcı-adını-doğrula/', views.validate_username, name = "validate_username"),
]