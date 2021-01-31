from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Post, Group, User, Follow
from .forms import PostForm, CommentForm
import datetime as dt


@cache_page(20)
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator
    }
    return render(request, "main/index.html", context)


def group_posts(request, slug):
    """
    Сортирует данные 2х таблиц Post/Group. Выводить 12 последних
    сообщений сообщества.
    """
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "main/group.html",
                           {"group": group, "page": page,
                            "paginator": paginator})


@login_required
def new_post(request):
    """
    Записываем данные в базу.
    """
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("index")
    context = {"form": form}
    return render(request, "main/new_post.html", context)


def profile(request, username):
    """
    Производим поиск всех постов пользователя, передаем данные в шаблон
    profile.html
    """
    user = get_object_or_404(User, username=username)
    posts_list = user.posts.all()

    follower_count = Follow.objects.filter(user=user.id).count()
    following_count = Follow.objects.filter(author=user.id).count()

    following = Follow.objects.filter(user=request.user.id, author=user.id)

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {"profile": user, "page": page, "paginator": paginator,
               'follower_count': follower_count,
               'following_count': following_count,
               'following': following}
    return render(request, 'main/profile.html', context)


def post_view(request, username, post_id):
    """
    Производим поиск статьи автора, данные передаем в post.html
    """
    user = get_object_or_404(User, username=username)
    follower_count = Follow.objects.filter(user=user.id).count()
    following_count = Follow.objects.filter(author=user.id).count()
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm()
    comments = post.comments.all()
    context = {"post": post, "comments": comments, "form": form,
               "follower_count": follower_count, "profile": user,
               "following_count": following_count}

    return render(request, "main/post.html", context)


@login_required
def post_edit(request, username, post_id):
    """
    Метод проверяет является ли текущий пользователь автором статьи.
    Если True предоставляет возможность редактировать статью, после
    redirect на страницу поста.
    Если False, redirect на страницу поста без возможности редактировать
    """
    edit = True
    post = get_object_or_404(Post, pk=post_id, author__username=username)

    if post.author != request.user:
        return redirect("post", username, post_id)
    if request.method == "POST":
        form = PostForm(request.POST or None, files=request.FILES or None,
                        instance=post)
        instance = form.save(commit=False)
        instance.pub_date = dt.datetime.now()
        instance.save()
        return redirect("post", username, post_id)

    context = {
        "edit": edit,
        "form": PostForm(instance=post),
        "post": post}
    return render(request, 'main/new_post.html', context)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.post = post
            instance.save()
            return redirect("post", username=username, post_id=post_id)
    context = {"form": form, "post": post}
    return render(request, 'main/comments.html', context)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    # Вывлодим список статей любимых авторов
    # Шикарный запрос, его надо запомнить!!!
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "paginator": paginator
    }

    return render(request, "main/follow.html", context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    value = Follow.objects.filter(user=request.user, author=author).exists()
    if request.user.username == username or value:
        return redirect("profile", username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username=username)
