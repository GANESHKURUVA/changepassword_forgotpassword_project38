from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')



def rigistration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            nufo=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            nufo.set_password(password)
            nufo.save()
            nupo=pfd.save(commit=False)
            nupo.username=nufo
            nupo.save()

            send_mail('send mail',
                      " successfully done",
                      'ganesh.kuruva0407@gmail.com',
                      [nufo.email],
                      fail_silently=True
                      )
            return HttpResponse('rigister successfully')
        else:
            return HttpResponse('invalid data')
    return render(request,'rigistration.html',d)



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        auo=authenticate(username=username,password=password)
        if auo and auo.is_active:
            login(request,auo)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid usename or password entered')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
   
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        uo.set_password(password)
        uo.save()
        return HttpResponse('password changed successfully.....!!')
    return render(request,'change_password.html')


def forgotpassword(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        luo=User.objects.filter(username=username)
        if luo:
            uo=luo[0]
            uo.set_password(password)
            uo.save()
            return HttpResponse('reset password successfully...')
        else:
            return HttpResponse('invalid username!!!')
    return render(request,'forgot.html')








def about(request):
    return render(request,'about.html')
def family(request):
    return render(request,'family.html')
def powers(request):
    return render(request,'powers.html')