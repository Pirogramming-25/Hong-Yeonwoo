from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .models import Follow

from django.db.models import Q

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from posts.models import Like


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    posts = profile_user.posts.all().order_by('-created_at')

    post_count = posts.count()
    follower_count = profile_user.follower_set.count()
    following_count = profile_user.following_set.count()

    is_me = request.user == profile_user

    is_following = False
    if request.user.is_authenticated and not is_me:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'is_me': is_me,
        'is_following': is_following,
        'liked_post_ids': liked_post_ids,
    })

def user_search(request):
    query = request.GET.get('q', '')

    users = User.objects.none()

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)

    following_ids = []
    if request.user.is_authenticated:
        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list('following_id', flat=True)

    return render(request, 'accounts/user_search.html', {
        'query': query,
        'users': users,
        'following_ids': following_ids,
    })

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'self_follow_not_allowed'}, status=400)
        return redirect('accounts:profile', username=username)

    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    )

    if follow.exists():
        follow.delete()
        is_following = False
    else:
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )
        is_following = True

    follower_count = target_user.follower_set.count()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'follower_count': follower_count,
        })

    return redirect('accounts:profile', username=username)