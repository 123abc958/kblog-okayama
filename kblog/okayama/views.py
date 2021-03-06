# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag
from .forms import PostAddForm 
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
   posts = Post.objects.all().order_by('-created_at')
   return render(request, 'okayama/index.html', {'posts': posts})

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'okayama/detail.html', {'post': post})

@login_required
def add(request):
   if request.method == "POST":
      form = PostAddForm(request.POST, request.FILES)
      if form.is_valid():
         post = form.save(commit=False)
         post.user = request.user
         post.save()
         return redirect('okayama:index')
   else:   
       form = PostAddForm()
   return render(request, 'okayama/add.html', {'form': form})

@login_required
def edit(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   if request.method == "POST":
       form = PostAddForm(request.POST, request.FILES, instance=post)
       if form.is_valid():
           form.save()
           return redirect('okayama:detail', post_id=post.id)
   else:
       form = PostAddForm(instance=post)
   return render(request, 'okayama/edit.html', {'form': form, 'post':post })

@login_required
def delete(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   post.delete()
   return redirect('okayama:index')