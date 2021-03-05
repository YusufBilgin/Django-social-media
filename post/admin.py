from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.StackedInline):
    verbose_name = "Yorum"
    verbose_name_plural = "Yorumlar"
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Gönderi detayları',
            {
                'fields': ['user', 'post_image', 'description']
            }
        )
    ]
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)
