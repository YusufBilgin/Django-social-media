from PIL import Image
from  io import BytesIO
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User


# Yüklenen resimlerin azicik kalitelerini düsürüyoruzki sunucumuzun hafizasi hemen dolmasin ve sayfa daha hizli yüklensin diye
def compress(image):
    i = Image.open(image)
    i_io = BytesIO()
    i.save(i_io, 'JPEG', quality = 30)  # Buradaki quality degerini arttirdikca resimin kaliteside artar. Ben simdilik ideal olarak 30 degerini kullaniyorum.
                                        # Acikcasi bir sosyal medya uygulamasinda asiri kaliteli resimlere gerek yok. Kimse bunlari alip zoomlamiyacak.                        
    new_image = File(i_io, name = image.name)
    return new_image


class Post(models.Model):
    id = models.AutoField(auto_created = True,primary_key = True,serialize = False,verbose_name = 'ID')
    user = models.ForeignKey("auth.User",on_delete = models.CASCADE, verbose_name = "Paylaşan Kullanıcı")
    post_image = models.ImageField(blank = False, null = False, verbose_name = "Resim", upload_to = 'imgs/')
    description = models.CharField(blank = True, null = False, verbose_name = "Açıklama", max_length = 300, default = "#")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Oluşturulma Tarihi")
    modal_width = models.CharField(blank = True, null =  True, max_length = 2, verbose_name = "Genişlik Bilgisi", default = 'lg') # xl or lg 

    def __str__(self):
        return "Resim id.{}  |  Yükleyen kullanıcı {}".format(self.id, self.user.username)

    def save(self, *args, **kwargs):
        new_image = compress(self.post_image)
        self.post_image = new_image
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_date']
        verbose_name = "Gönderi"
        verbose_name_plural = "Gönderiler"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = "Yorumun yazıldığı gönderi", related_name="comments")
    comment_author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Kullanıcı")
    comment_content = models.CharField(max_length = 300, verbose_name="Yorum")
    comment_like = 0
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="begenen kullanici")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="begenilen gönderi")
    created = models.DateTimeField(auto_now_add=True)


class Archive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="kaydeden kullanıcı")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="gönderi")
    created = models.DateTimeField(auto_now_add=True)