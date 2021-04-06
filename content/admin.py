from django.contrib import admin

# Register your models here.
from content.models import Category, Content


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'city', 'country', 'konum', 'status']
    list_filter = ['status', 'category']


admin.site.register(Category, CategoryAdmin)

admin.site.register(Content, ContentAdmin)
