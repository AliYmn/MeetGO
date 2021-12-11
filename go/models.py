from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # user description
    description = models.CharField(max_length=500, null=True,
                                verbose_name="Açıklama",
                                help_text="Kullanıcı hakkında açıklama")
    # profile url
    url = models.CharField(max_length=500, null=True, blank=True)

    start_time = models.DateTimeField(auto_now=False, null=True)
    modefied_time = models.DateTimeField(auto_now=False, null=True)

    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

class Category(models.Model):
    # Kategori adı
    title = models.CharField(max_length=500,
                             null=True, unique=True, verbose_name="Kategori Adı",
                             help_text="Kategori adını belirleyin.")

    description = models.CharField(max_length=500, null=True,
                                   verbose_name="Açıklama",
                                   help_text="Kategori hakkında kısa açıklama belirtin.")
    # Kategori slug url oluşturma.
    url = models.CharField(max_length=500, null=True, blank=True)

    # Kategori icon
    icon = models.CharField(max_length=500, verbose_name="Icon",help_text="Icon")

    start_time = models.DateTimeField(auto_now=False, null=True)
    modefied_time = models.DateTimeField(auto_now=False, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/category/{}".format(self.url)

    def save(self, *args, **kwargs):
        self.url = slugify(self.title.lower(), allow_unicode=False)
        super(Category, self).save(*args, **kwargs)


class Events(models.Model):
    """ Events Models """
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    # event title
    title = models.CharField(max_length=500,
                             null=True, unique=False, verbose_name="title",
                             help_text="please write title")

    # event type
    event_type = models.CharField(max_length=500,
                             null=True, unique=False, verbose_name="type",
                             help_text="event type")
    # event tags
    tags = models.CharField(max_length=500, null=True,
                            verbose_name="Keywords",
                            help_text="sperate with comma (,)")
    # description                        
    description = RichTextField()

    # event image
    image = models.CharField(max_length=500, null=True, blank=True)
    # event address
    address = models.CharField(max_length=500, null=True, blank=True)

    # event image
    url = models.CharField(max_length=500, null=True, blank=True)

    # event categories
    category_list = models.ForeignKey(Category, null=True, blank=True,
                                   db_index=True,verbose_name="Categories",on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now=False, null=True)
    modefied_time = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/event/{}".format(self.url)

    def save(self, *args, **kwargs):
        self.url = slugify(self.title.lower(), allow_unicode=False)
        super(Events, self).save(*args, **kwargs)

class Follow(models.Model):
    event = models.ManyToManyField(Events)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return  self.user.first_name

    def save(self, *args, **kwargs):
        super(Follow, self).save(*args, **kwargs)

class Subscription(models.Model):
    organizer = models.ManyToManyField(Profile,related_name="organizer")
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return  self.user.first_name

    def save(self, *args, **kwargs):
        super(Subscription, self).save(*args, **kwargs)