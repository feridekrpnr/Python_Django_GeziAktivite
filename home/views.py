import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactFormu, ContactFormMessage
from content.models import Content, Images, Category, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Content.objects.all()[:3]
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
            catid = form.cleaned_data['catid']
            if catid == 0:
                content = Content.objects.filter(title__icontains=query)
            else:

                content = Content.objects.filter(title__icontains=query, category_id=catid)

            context = {'content': content,
                       'category': category,
                       }

            return render(request, 'content_search.html', context)

    return HttpResponseRedirect('/')

def content_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    content = Content.objects.filter(title__icontains=q)
    results = []
    for rs in content:
      content_json = {}
      content_json = rs.title
      results.append(content_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login hatası ! Lütfen bilgilerinizi kontrol ediniz")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category, }
    return render(request, 'login.html', context)