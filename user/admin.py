from django.contrib import admin
from .models import Profile, UserFollowing


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ['user__date_joined']
    # Evet nasil calisti hic bir fikrim yok ama iyi bu kalsin.
    search_fields = ['user__username']


class UserFollowingAdmin(admin.ModelAdmin):
    list_filter = ['created']
    search_fields = ['user_id__username']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserFollowing, UserFollowingAdmin)
