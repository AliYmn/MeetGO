from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField

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
        # dönüş değeri
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
                             null=True, unique=True, verbose_name="title",
                             help_text="please write title")

    # event tags
    tags = models.CharField(max_length=500, null=True,
                            verbose_name="Keywords",
                            help_text="sperate with comma (,)")
    # description                        
    description = RichTextField()

    # event image
    image = ProcessedImageField(upload_to='staticfiles/uploads/event/',
                                           format='JPEG',
                                           options={'quality': 80},verbose_name="Image",
                                           help_text="Image")

    # event categories
    category_list = models.ForeignKey(Category, null=True, blank=True,
                                   db_index=True,verbose_name="Categories",on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now=False, null=True)
    modefied_time = models.DateTimeField(auto_now=False, null=True)
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
