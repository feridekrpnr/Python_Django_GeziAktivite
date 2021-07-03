from pyexpat.errors import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from aktivite.models import Aktivite, AktiviteImageForm, AktiviteForm
from content.models import Category, Comment, Content, Images, ContentForm

# Create your views here.
from home.models import UserProfile, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user
    try:
        profile = UserProfile.objects.get(user_id=current_user.id)
    except:
        profile =None
    context = {'category': category,
               'profile': profile,
               }
    return render(request, 'user_profile.html', context)



def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        try:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        except:
            profile_form =None
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #messages.success(request, 'ok')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,

        }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
          #  messages.success(request, 'şifreniz başarı bir şekilde kaydedilmiştir')
            return HttpResponseRedirect('/user')
        else:
           # messages.error(request, 'ERROR<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')

    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form,
            'category': category,

        })



def comments(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user)
    context = {
        'category': category,
        'comments': comments,
        'setting': setting,
    }
    return render(request, 'user_comments.html', context)



@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'comment deleted')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def aktivities(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    aktivite = Aktivite.objects.filter(user_id=current_user.id)
    checked = Aktivite.objects.filter(status='Evet')
    obj_all = Aktivite.objects.all()

    print('___________________')
    print(checked)
    print(obj_all)
    context = {
        'category': category,
        'setting': setting,
        'aktivite': aktivite,
        'checked':checked,

    }
    return render(request, 'user_aktivities.html', context)



@login_required(login_url='/login')
def addaktivite(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.category = form.cleaned_data['category']
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.konum = form.cleaned_data['konum']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
           # messages.success(request, 'Başarılı bir şekilde eklenmiştir')
            return HttpResponseRedirect('/user/aktivities')
        else:
           # messages.error(request, 'Aktivite Form Error: ' + str(form.errors))
            return HttpResponseRedirect('/user/addaktivite')
    else:
        category = Category.objects.all()
        setting = Setting.objects.all()
        form = ContentForm()
        context = {
            'setting': setting,
            'category': category,
            'form': form,
        }
        return render(request, 'user_addaktivite.html', context)

@login_required(login_url='/login')
def aktiviteedit(request, id):
    content = Content.objects.get(id=id)
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
           # messages.success(request, 'Başarılı bir şekilde değiştirilmiştir')
            return HttpResponseRedirect('/user/contents')
        else:
            #messages.error(request, 'Aktivite Form Error: ' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit/' + str(id))
    else:
        category = Category.objects.all()
        form = ContentForm(instance=content)
        context = {
            'setting': setting,
            'category': category,
            'form': form,
        }
        return render(request, 'user_addaktivite.html', context)



def aktivitedelete(request, id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Aktivite deleted.')
    return HttpResponseRedirect('/user/aktivities')

def aktiviteaddimage(request,id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = AktiviteImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.content_id = id
            data.title = form.cleaned_data['title']
            data.image = form.cleaned_data['image']
            data.save()
           # messages.success(request, 'your image has been successfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
           # messages.warning(request, 'Form Error: ' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        content = Content.objects.get(id=id)
        images = Images.objects.filter(place_id=id)
        form = AktiviteImageForm()
        context = {
            'content': content,
            'images': images,
            'form': form,
        }
        return render(request, 'aktivite_gallery.html', context)


def aktiviteimagedelete(request,id):
    content = Content.objects.filter(id=id)
    lasturl = request.META.get('HTTP_REFERER')
    Images.objects.filter(id=id, place_id=id).delete()
   # messages.success(request,'Image Deleted')
    return HttpResponseRedirect(lasturl)
