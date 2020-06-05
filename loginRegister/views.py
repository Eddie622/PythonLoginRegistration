from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
import bcrypt

# Create your views here.


def index(request):
    if 'userid' in request.session:
        return redirect('/success/')
    return render(request, 'index.html')


def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        "this_user" : user.objects.get(id=request.session['userid']),
        "other_users" : user.objects.exclude(id=request.session['userid']),
        "all_messages" : message.objects.all(),
        "all_comments" : comment.objects.all()
    }
    return render(request, 'success.html', context)


def process(request):
    if request.method == "GET":
        return redirect('/')

    errors = user.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['pwd']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],
        email=request.POST['email'],password=pw_hash)

        return redirect('/success/')

def verify(request):
    if request.method == "GET":
        return redirect('/')
    
    this_user = user.objects.filter(email=request.POST['email'])
    if this_user:
        logged_user = this_user[0] 

        if bcrypt.checkpw(request.POST['pwd'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success/')

    messages.error(request, "invalid email/password")
    return redirect("/")

def logout(request):
    if 'userid' in request.session:
        del request.session['userid']
    return redirect('/')

def postMessage(request):
    if request.method == "GET":
        return redirect('/')

    message.objects.create(content=request.POST['message'],User_id=request.session['userid'])

    return redirect('/success/')

def postComment(request):
    if request.method == "GET":
        return redirect('/')

    comment.objects.create(content=request.POST['comment'],User_id=request.session['userid'],Message_id=request.POST['messageid'])

    return redirect('/success/')