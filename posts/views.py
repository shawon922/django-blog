from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm


def index(request):
    posts_list = Post.objects.all() #.order_by("-timestamp")

    paginator = Paginator(posts_list, 5)
    page_var = 'page1'
    page = request.GET.get(page_var)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'List of Posts',
        'posts': posts,
        'page_var': page_var
    }

    return render(request, 'posts/index.html', context)


def create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Created.')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'page_title': 'Create New Post',
        'form': form,
    }
    return render(request, 'posts/create.html', context)


def update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Successfully Updated.')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'page_title': 'Update Post',
        'instance': instance,
        'form': form,
    }
    return render(request, 'posts/update.html', context)


def detail(request, id=None):
    post = get_object_or_404(Post, id=id)

    context = {
        'page_title': 'Post Detail',
        'post': post
    }
    return render(request, 'posts/detail.html', context)


def delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Successfully Deleted.')
    return redirect('posts:index')
