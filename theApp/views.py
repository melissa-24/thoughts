from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['id'] = userLogin.id
            return redirect('/thoughts/')
        messages.error(request, "Invalid Credentials")
        return redirect('/')
    messages.error(request, "That email is not in our system please register for an account")
    return redirect('/')


def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['id'] = newUser.id
    return redirect('/thoughts/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    thoughts = Thought.objects.all()
    author = Thought.objects.all().values()
    context = {
        'user': user,
        'posts': thoughts,
        'author': author,
    }
    print(thoughts)
    return render(request, 'dashboard.html', context)

def createThought(request):
    Thought.objects.create(
        thought=request.POST['thought'],
        poster = User.objects.get(id=request.session['id']),
    )
    return redirect('/thoughts/')

def viewThought(request, thought_id):
    onePost = Thought.objects.get(id=thought_id)
    context = {
        'onePost': onePost,
    }
    return render(request, 'oneThought.html', context)

def editThought(request, thought_id):
    oneThought = Thought.objects.get(id=thought_id)
    context = {
        'edit': oneThought,
    }
    return render(request, 'editThought.html', context)

def updateThought(request, thought_id):
    toUpdate = Thought.objects.get(id=thought_id)
    toUpdate.thought = request.POST['thought']
    toUpdate.save()

    return redirect(f'/thought/{thought_id}/editThought/')

def deleteThought(request, thought_id):
    toDelete = Thought.objects.get(id=thought_id)
    toDelete.delete()

    return redirect('/thoughts/')

def likeThought(request):
    pass
