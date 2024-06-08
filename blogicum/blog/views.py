from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from blog.models import Post, Category


def get_posts(queryset=Post.objects):
    return queryset.select_related(
        'author',
        'category',
        'location',
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True
    )


def index(request: HttpRequest) -> HttpResponse:
    posts = get_posts()[:settings.POSTS_BY_PAGE]
    context = {"post_list": posts}
    return render(request, "blog/index.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(get_posts(), id=post_id)
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_posts(category.posts)
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)
