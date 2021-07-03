from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),


    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),


    path('aktivities/', views.aktivities, name='aktivities'),
    path('addaktivite/', views.addaktivite, name='addaktivite'),
    path('aktiviteedit/<int:id>', views.aktiviteedit, name='aktiviteedit'),
    path('aktivitedelete/<int:id>', views.aktivitedelete, name='aktivitedelete'),
    path('aktiviteaddimage/<int:id>', views.aktiviteaddimage, name='aktiviteaddimge'),
    path('aktiviteimagedelete/<int:id>', views.aktiviteimagedelete, name='aktiviteimagedelete'),

    #path('<int:question_id>/', views.detail, name='detail'),
]