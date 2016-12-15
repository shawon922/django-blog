from django.shortcuts import render, get_object_or_404, Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

from .forms import CommentForm

from .models import Comment


@login_required # (login_url='/login/')
def delete_comment(request, id=None):
    # if request.method == 'POST':
    # comment = get_object_or_404(Comment, id=id)
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    if comment.user != request.user:
        response = HttpResponse("You do not have permission to view this.")
        response.status_code = 403
        return response

    parent_url = comment.content_object.get_absolute_url()
    comment.delete()
    return HttpResponseRedirect(parent_url)


def comment_thread(request, id=None):
    # comment = get_object_or_404(Comment, id=id)
    try:
        comment = Comment.objects.get(id=id)
    except:
        raise Http404

    if not comment.is_parent:
        comment = comment.parent

    initial_data = {
        'content_type': comment.content_type,
        'object_id': comment.object_id
    }

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid() and request.user.is_authenticated():
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
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj
        )

        if created:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'page_title': 'Comment thread',
        'comment': comment,
        'comment_form': form,
    }
    return render(request, "comment_thread.html", context)
