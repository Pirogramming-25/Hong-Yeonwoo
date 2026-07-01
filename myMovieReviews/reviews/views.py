from django.shortcuts import render, get_object_or_404, redirect
from .models import Review


def review_list(request):
    sort = request.GET.get('sort', 'latest')

    if sort == 'title':
        reviews = Review.objects.all().order_by('title')
    elif sort == 'rating':
        reviews = Review.objects.all().order_by('-rating')
    elif sort == 'running_time':
        reviews = Review.objects.all().order_by('running_time')
    else:
        reviews = Review.objects.all().order_by('-id')

    for review in reviews:
        review.running_time_text = format_running_time(review.running_time)

    return render(request, 'reviews/review_list.html', {'reviews': reviews, 'sort': sort,})


def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.running_time_text = format_running_time(review.running_time)
    return render(request, 'reviews/review_detail.html', {'review': review})


def review_create(request):
    if request.method == 'POST':
        Review.objects.create(
            title=request.POST.get('title'),
            director=request.POST.get('director'),
            actor=request.POST.get('actor'),
            genre=request.POST.get('genre'),
            rating=request.POST.get('rating'),
            running_time=request.POST.get('running_time'),
            content=request.POST.get('content'),
            release_year=request.POST.get('release_year'),
        )
        return redirect('review-list')
    return render(request, 'reviews/review_form.html')


def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor')
        review.genre = request.POST.get('genre')
        review.rating = request.POST.get('rating')
        review.running_time = request.POST.get('running_time')
        review.content = request.POST.get('content')
        review.release_year = request.POST.get('release_year')
        review.save()
        return redirect('review-detail', pk=pk)

    return render(request, 'reviews/review_form.html', {'review': review})


def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        review.delete()
        return redirect('review-list')

    return render(request, 'reviews/review_delete.html', {'review': review})

def format_running_time(minutes):
    hours = minutes // 60
    mins = minutes % 60

    if hours and mins:
        return f'{hours}시간 {mins}분'
    if hours:
        return f'{hours}시간'
    return f'{mins}분'
