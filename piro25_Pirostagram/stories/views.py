from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Story

from django.shortcuts import get_object_or_404, redirect


@login_required
def create_story(request):
    if request.method == 'POST':
        image = request.FILES.get('image')

        if image:
            Story.objects.create(
                author=request.user,
                image=image
            )

    return redirect('posts:feed')

@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if story.author == request.user:
        story.delete()

    return redirect('posts:feed')