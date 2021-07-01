from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from aktivite.models import Aktivite, AktiviteImages, Menu, UserContents, AktiviteImagess


# Register your models here.


class AktiviteImageInline(admin.TabularInline):
    model = AktiviteImages
    extra = 3

class MenuAktiviteInline(admin.TabularInline):
    model = Aktivite
    extra = 1

class AktiviteAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'image_tag', 'status', 'create_at']
    list_filter = ['status', 'type']
    inlines = [AktiviteImageInline]
    prepopulated_fields = {'slug': ('title',)}

class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title', 'status')
    list_filter = ['status']
    inlines = [MenuAktiviteInline]



admin.site.register(Aktivite, AktiviteAdmin)
admin.site.register(Menu, MenuAdmin)



class UserContentsImageInline(admin.TabularInline):
    model = AktiviteImagess
    extra = 3

class UserContentsInline(admin.TabularInline):
    model = UserContents
    extra = 1

class UserContentsAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'image_tag', 'status', 'create_at']
    list_filter = ['status', 'type']
    inlines = [UserContentsImageInline]
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(UserContents, UserContentsAdmin)