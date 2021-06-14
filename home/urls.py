from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)