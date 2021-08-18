from django import forms
from django.db import reset_queries
from django.shortcuts import render,redirect
from .form import SignUpForm, LoginForm, PostForm
from .models import Post
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'home/home.html', {'posts':posts})

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        full_name = request.user.get_full_name()
        gps = request.user.groups.all()
        return render(request, 'home/dashboard.html',{'posts':posts,'full_name':full_name, 'groups':gps})
    else:
        return redirect('/login/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                messages.success(request, "You Logged in Successfully!!")
                return redirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'home/login.html', {'form':form})
    else:
        return redirect('/dashboard/')

def user_singup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!! You have Become an Author")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['description']
                post = Post(title=title, description=desc)
                messages.success(request, "Post is Added SuccessFully!!")
                post.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'home/addpost.html', {'form':form})
    else:
        return redirect('/login/')

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'home/updatepost.html', {'form':form})
    else:
        return redirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
        return redirect('/dashboard/')
    else:
        return redirect('/login/')