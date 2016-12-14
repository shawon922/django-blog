from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.contenttypes.models import ContentType

from .models import Post
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm


def index(request):
    posts_list = Post.objects.all()  # .order_by("-timestamp")

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
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404

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


def update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
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


def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)

    initial_data = {
        'content_type': post.get_content_type,
        'object_id': post.id
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')

        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        parent_obj = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj
        )

        if created:
            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments # Comment.objects.filter_by_instance(post)

    context = {
        'page_title': 'Post Detail',
        'post': post,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'posts/detail.html', context)


def delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Successfully Deleted.')
    return redirect('posts:index')
