from functools import partial
from itertools import groupby
from operator import attrgetter
from django.forms.models import ModelChoiceIterator, ModelChoiceField


from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
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

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Content(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # relation with Category table one to many
    title = models.CharField(max_length=100)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    konum = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)



    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('contentdetail', kwargs={'slug': self.slug})


class Images(models.Model):

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

class Comment(models.Model):
        STATUS = (
            ('New', 'Yeni'),
            ('True', 'Evet'),
            ('False', 'Hayır')
        )
        content = models.ForeignKey(Content, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        subject = models.CharField(max_length=50)
        comment = models.TextField(max_length=250)
        rate = models.IntegerField(blank=True)
        status = models.CharField(max_length=10, choices=STATUS, default='New')
        ip = models.CharField(blank=True, max_length=20)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.subject

class CommentForm(ModelForm):
        class Meta:
            model = Comment
            fields = ['subject', 'comment', 'rate']


class GroupedModelChoiceIterator(ModelChoiceIterator):
        def __init__(self, field, groupby):
            self.groupby = groupby
            super().__init__(field)

        def __iter__(self):
            if self.field.empty_label is not None:
                yield ("", self.field.empty_label)
            queryset = self.queryset
            # Can't use iterator() when queryset uses prefetch_related()
            if not queryset._prefetch_related_lookups:
                queryset = queryset.iterator()
            for group, objs in groupby(queryset, self.groupby):
                yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(ModelChoiceField):
        def __init__(self, *args, choices_groupby, **kwargs):
            if isinstance(choices_groupby, str):
                choices_groupby = attrgetter(choices_groupby)
            elif not callable(choices_groupby):
                raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
            self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
            super().__init__(*args, **kwargs)



class ContentForm(ModelForm):
    category = GroupedModelChoiceField(
        queryset=Category.objects.all(),
        choices_groupby='parent'
    )

    class Meta:
        model = Content
        fields = ['category','title','slug','keywords','description','image','city','country','konum','detail']
        widgets = {
            'title':TextInput(attrs={'class':'input','placeholder':'title'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'city'}),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'country'}),
            'konum': TextInput(attrs={'class': 'input', 'placeholder': 'konum'}),
            'detail': CKEditorWidget(),
        }


class AktiviteImageForm(ModelForm):
        class Meta:
            model = Images
            fields=['title','image']
