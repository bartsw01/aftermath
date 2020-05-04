from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Challenge, Post, Category

from .forms import CommentForm


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')    

@login_required
def challenges_index(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/index.html', {'challenges': challenges})

@login_required
def posts_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

@login_required
def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/detail.html', { 'post': post})


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'topic', 'content']

    def form_valid(self, form):
      form.instance.user = self.request.user  
      return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['topic', 'content']

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/posts/'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again' 
    form = UserCreationForm()
    context = { 'form': form, 'error_message': error_message} 
    return render(request, 'registration/signup.html', context)      


def list_of_post(request):
    post = Post.objects.filter(status = 'published')
    template = 'main_app/blog/list_of_post.html'
    context = { 'post': post }
    return render(request, template, context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    template = 'main_app/blog/post_detail.html'
    context = { 'post': post }
    return render(request, template, context)


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', slug=post.slug)
        else:
            form = CommentForm()
        
        template = 'blog/add_comment.html'
        contex = { 'form': form }
        return render(request, template, context)           
