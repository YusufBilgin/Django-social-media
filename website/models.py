from django.db import models


class Questions(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name = 'ID'
    )
    title = models.TextField(
        verbose_name = 'soru başlık'
    )
    answer = models.TextField(
        verbose_name = 'soru cevap'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Soru"
        verbose_name_plural = "Sorular"


class WhatsNew(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name = 'ID'
    )
    news = models.CharField(
        null = True,
        max_length = 500, 
        verbose_name = "Siteye eklenen yeni özellikler"
    )

    def __str__(self):
        return str(self.news)

    class Meta:
        verbose_name = "Yeni özellik"
        verbose_name_plural = "Yeni özellikler"


class Message(models.Model):
    id = models.AutoField(
        auto_created = True, 
        primary_key = True, 
        serialize = False, 
        verbose_name = 'ID'
    )
    title = models.CharField(
        max_length = 100, 
        verbose_name = "Başlık"
    )
    message = models.TextField(
        verbose_name = "Mesaj"
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"
