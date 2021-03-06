from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_imgs/defaultprofile.png',
                              upload_to='profile_imgs/', verbose_name='Profil resmi')
    bio = models.TextField(max_length=350, blank=True,
                           verbose_name='Biyografi (bio)')
    location = models.CharField(
        max_length=50, blank=True, verbose_name='Konum')
    birth_date = models.DateField(
        null=True, blank=True, verbose_name='Doğum Tarihi')

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = "Kullanıcı Profilli"
        verbose_name_plural = "Kullanıcı Profilleri"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserFollowing(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following",
                                on_delete=models.CASCADE, verbose_name="takip eden")
    following_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE, verbose_name="takip edilen")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Takip eyleminin gerçekleştiği tarih')

    def __str__(self):
        return str(self.user_id) + " -> " + str(self.following_user_id)

    class Meta:
        verbose_name = "Kullanıcı Takipçileri"
        verbose_name_plural = "Kullanıcı Takipçileri"
