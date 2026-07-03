from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Idea, DevTool, IdeaStar
from .forms import IdeaForm, DevToolForm


def idea_list(request):
    sort = request.GET.get('sort', 'latest')

    if sort == 'name':
        ideas = Idea.objects.all().order_by('title')
    elif sort == 'oldest':
        ideas = Idea.objects.all().order_by('created_at')
    elif sort == 'interest':
        ideas = Idea.objects.all().order_by('-interest')
    else:
        ideas = Idea.objects.all().order_by('-created_at')

    for idea in ideas:
        star = getattr(idea, 'star', None)
        idea.starred = star.is_starred if star else False

    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ideas/idea_list.html', {
        'page_obj': page_obj,
        'sort': sort,
    })


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    star = getattr(idea, 'star', None)
    idea.starred = star.is_starred if star else False

    return render(request, 'ideas/idea_detail.html', {
        'idea': idea,
    })


def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()

    return render(request, 'ideas/idea_form.html', {
        'form': form,
        'title': '아이디어 등록',
    })

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)

    return render(request, 'ideas/idea_form.html', {
        'form': form,
        'title': '아이디어 수정',
    })

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        idea.delete()
        return redirect('ideas:idea_list')

    return render(request, 'ideas/idea_delete.html', {
        'idea': idea,
    })

def devtool_list(request):
    devtools = DevTool.objects.all().order_by('name')
    return render(request, 'ideas/devtool_list.html', {
        'devtools': devtools,
    })

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    ideas = devtool.ideas.all()

    return render(request, 'ideas/devtool_detail.html', {
        'devtool': devtool,
        'ideas': ideas,
    })

def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('ideas:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm()

    return render(request, 'ideas/devtool_form.html', {
        'form': form,
        'title': '개발툴 등록',
    })


def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)

    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            devtool = form.save()
            return redirect('ideas:devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)

    return render(request, 'ideas/devtool_form.html', {
        'form': form,
        'title': '개발툴 수정',
    })


def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)

    if request.method == 'POST':
        devtool.delete()
        return redirect('ideas:devtool_list')

    return render(request, 'ideas/devtool_delete.html', {
        'devtool': devtool,
    })

def idea_toggle_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        star, created = IdeaStar.objects.get_or_create(idea=idea)
        star.is_starred = not star.is_starred
        star.save()

    next_url = request.POST.get('next', 'ideas:idea_list')
    return redirect(next_url)


def idea_interest(request, pk, action):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        if action == 'plus':
            idea.interest += 1
        elif action == 'minus':
            idea.interest -= 1

        idea.save()

    next_url = request.POST.get('next', 'ideas:idea_list')
    return redirect(next_url)