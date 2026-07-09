from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.models import Follow
from stories.models import Story
from .models import Post, Like, Comment

from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


def sort_posts(posts, sort):
    if sort == 'likes':
        return posts.annotate(like_total=Count('likes')).order_by('-like_total', '-created_at')

    if sort == 'name':
        return posts.order_by('author__username', '-created_at')

    return posts.order_by('-created_at')


@login_required
def feed(request):
    sort = request.GET.get('sort', 'latest')

    following_users = Follow.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    feed_user_ids = list(following_users) + [request.user.id]

    posts = Post.objects.filter(
        author__in=feed_user_ids
    )
    posts = sort_posts(posts, sort)

    story_user_ids = list(following_users) + [request.user.id]

    stories = Story.objects.filter(
        author__in=story_user_ids
    ).order_by('-created_at')

    recommended_users = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=following_users
    )[:4]

    liked_post_ids = Like.objects.filter(
        user=request.user
    ).values_list('post_id', flat=True)

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'stories': stories,
        'recommended_users': recommended_users,
        'liked_post_ids': liked_post_ids,
        'current_sort': sort,
    })

@login_required
def post_search(request):
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'latest')

    following_users = Follow.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    posts = Post.objects.none()
    if query:
        posts = Post.objects.filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()
        posts = sort_posts(posts, sort)

    story_user_ids = list(following_users) + [request.user.id]

    stories = Story.objects.filter(
        author__in=story_user_ids
    ).order_by('-created_at')

    recommended_users = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=following_users
    )[:4]

    liked_post_ids = Like.objects.filter(
        user=request.user
    ).values_list('post_id', flat=True)

    return render(request, 'posts/feed.html', {
        'posts': posts,
        'stories': stories,
        'recommended_users': recommended_users,
        'liked_post_ids': liked_post_ids,
        'post_query': query,
        'is_post_search': True,
        'current_sort': sort,
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(
        post=post,
        user=request.user
    )

    if like.exists():
        like.delete()
        is_liked = False
    else:
        Like.objects.create(
            post=post,
            user=request.user
        )
        is_liked = True

    return JsonResponse({
        'is_liked': is_liked,
        'like_count': post.likes.count(),
    })

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

            return JsonResponse({
                'success': True,
                'comment_count': post.comments.count(),
                'author': comment.author.username,
                'content': comment.content,
            })

    return JsonResponse({
        'success': False,
    }, status=400)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user:
        comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user and request.method == 'POST':
        content = request.POST.get('content', '').strip()

        if content:
            comment.content = content
            comment.save()

    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))

@login_required
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        content = request.POST.get('content', '').strip()

        if image:
            Post.objects.create(
                author=request.user,
                image=image,
                content=content
            )

    return redirect('posts:feed')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('accounts:profile', username=post.author.username)

    if request.method == 'POST':
        image = request.FILES.get('image')
        content = request.POST.get('content', '').strip()

        if image:
            post.image = image

        post.content = content
        post.save()

    return redirect('accounts:profile', username=request.user.username)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        post.delete()

    return redirect('accounts:profile', username=request.user.username)
