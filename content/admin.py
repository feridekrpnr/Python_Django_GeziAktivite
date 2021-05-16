from django.contrib import admin

# Register your models here.
from content.models import Category, Content, Images

class ContentImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']



class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'city', 'country', 'konum', 'status']
    list_filter = ['status', 'category']
    inlines = [ContentImageInline]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'image']


admin.site.register(Category, CategoryAdmin)

admin.site.register(Content, ContentAdmin)
admin.site.register(Images, ImagesAdmin)
