import json
from unicodedata import category
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactFormu, ContactFormMessage
from content.models import Content, Images, Category, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Content.objects.all()[:1]
    category = Category.objects.all()
    daycontents =Content.objects.all()[:3]
    lastcontents = Content.objects.all().order_by('-id')[:3]
    randomcontents = Content.objects.all().order_by('?')[:3]
    context = {'setting': setting,
               'page': 'home',
               'category': category,
               'sliderdata': sliderdata,
               'daycontents': daycontents,
               'lastcontents': lastcontents,
               'randomcontents':  randomcontents,
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkimizda', 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslarimiz(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'referanslarimiz', 'category': category}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):


    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir! Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')



    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all()
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'iletisim.html', context)


def category_contents(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    contents =Content.objects.filter(category_id=id, status='True')
    context = { 'category': category,
                'contents': contents,
                'categorydata': categorydata
                }
    return render(request, 'contents.html', context)

def contentdetail(request, id, slug):
    category = Category.objects.all()
    content = Content.objects.get(pk=id)
    comments = Comment.objects.filter(content_id=id, status='True')
    images = Images.objects.filter(content_id=id)
    context = {'category': category,
               'content': content,
               'images': images,
               'comments': comments,
               }

    return render(request, 'contentdetail.html', context)


def content_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            content = Content.objects.filter(title__icontains=query)
            context = {'content': content,
                       'category': category,
                       }
            return render(request, 'content_search.html', context)

    return HttpResponseRedirect('/')


