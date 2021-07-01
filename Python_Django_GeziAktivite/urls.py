"""Python_Django_GeziAktivite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    path('', include('home.urls')),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('home/', include('home.urls')),
    path('user/', include('user.urls')),
    path('content/', include('content.urls')),
    path('aktivite/', include('aktivite.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('referanslarimiz/', views.referanslarimiz, name='referanslarimiz'),
    path('category/<int:id>/<slug:slug>/', views.category_usercontents, name='category_usercontents'),
    path('category/<int:id>/<slug:slug>/', views.category_contents, name='category_contents'),
    path('content/<int:id>/<slug:slug>/', views.contentdetail, name='contentdetail'),
    path('search/', views.content_search, name='content_search'),
    path('search_auto/', views.content_search_auto, name='content_search_auto'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('faq/', views.faq, name='faq'),
    path('aktivite/<int:id>/<slug:slug>/', views.aktivitedetail, name='aktivitedetail'),
    path('menu/<int:id>', views.menu, name='menu'),


]
if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)