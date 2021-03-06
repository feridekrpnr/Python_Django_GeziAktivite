import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from aktivite.models import UserContents, AktiviteImages, Menu, Aktivite
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
from content.models import Content, Images, Category, Comment


def index(request):
    try:

        setting = Setting.objects.get(pk=1)
    except:
        setting = None
    sliderdata = Content.objects.all()[:4]
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
            messages.success(request, "Mesaj??n??z ba??ar?? ile g??nderilmi??tir! Te??ekk??r Ederiz")
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
            messages.warning(request, "Login hatas?? ! L??tfen bilgilerinizi kontrol ediniz")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category, }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Ho?? geldiniz " + current_user.first_name)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category,
               'form': form,
               'setting': setting,
               }

    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status='True').order_by('ordernumber')
    setting = Setting.objects.get(pk=1)
    context = {'faq': faq, 'category': category, 'setting': setting}
    return render(request, 'faq.html', context)

def menu(request, id):
    aktivite = Aktivite.objects.get(menu_id=id)
    if aktivite:
        link='/aktivite/'+str(aktivite.id)+'/menu'
        return HttpResponseRedirect(link)

    else:
        messages.warning(request, "hata ! ilgili i??erik bulunamad??")
        link='/'
        return HttpResponseRedirect(link)


def aktivitedetail(request,id, slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    aktivite = Aktivite.objects.get(pk=id)
    images = AktiviteImages.objects.filter(aktivite_id=id)
    comments = Comment.objects.filter(aktivite_id=id, status='True')
    context = {'aktivite': aktivite,
               'category': category,
               'menu': menu,
               'images': images,
               'comments': comments,

              }

    return render(request, 'content_detail.html', context)



def category_usercontents(request, id, slug):
    setting = Setting.objects.get(pk=1)
    categorydata = Category.objects.get(pk=id)
    usercontents = UserContents.objects.filter(category_id=id, status='True')
    category = Category.objects.all()
    context = {'setting': setting, 'usercontents': usercontents, 'category': category, 'categorydata': categorydata, }
    return render(request, 'contents.html', context)

