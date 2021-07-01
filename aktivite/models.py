from lib2to3.fixes.fix_idioms import TYPE
from unicodedata import category

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Select
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from content.models import Category


class Menu(MPTTModel):

    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Aktivite(models.Model):
    TYPE = (

        ('menu', 'menu'),
        ('content', 'content'),

    )
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    menu = models.OneToOneField(Menu, null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(blank=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})




class AktiviteImages(models.Model):
    aktivite = models.ForeignKey(Aktivite, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class AktiviteForm(ModelForm):
    class Meta:
        model = Aktivite
        fields = ['type', 'title', 'slug', 'keywords', 'description', 'image', 'detail']
        widgets = {
            'title'   :TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'title'}),
            'slug'    : TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'description'}),
            'type'    : Select(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'city'}, choices=TYPE),
            'detail'  : CKEditorWidget(),
        }


class AktiviteImageForm(ModelForm):
    class Meta:
        model = AktiviteImages
        fields = ['title', 'image']






########################################################33
class UserContents(models.Model):
    TYPE = (

        ('menu', 'menu'),
        ('content', 'content'),

    )
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)  # category tablosuyla ilişkisi
    type = models.CharField(max_length=10, choices=TYPE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    location = models.CharField(max_length=225)
    detail = RichTextUploadingField()
    slug = models.SlugField(blank=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})


class AktiviteImagess(models.Model):
    usercontents = models.ForeignKey(UserContents, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserContentsForm(ModelForm):
    class Meta:
        model = UserContents
        fields = ['type', 'title', 'city', 'country', 'location', 'slug', 'keywords', 'description', 'image', 'detail']
        widgets = {
            'title'   :TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'title'}),
            'city': TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'city'}),
            'country': TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'country'}),
            'location': TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'location'}),
            'slug'    : TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'description'}),
            'type'    : Select(attrs={'style': 'width: 830px', 'class': 'input', 'placeholder': 'city'}, choices=TYPE),
            'detail'  : CKEditorWidget(),
        }


class UserContentsImageForm(ModelForm):
    class Meta:
        model = AktiviteImages
        fields = ['title', 'image']