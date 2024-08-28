from django.shortcuts import render
from django.views import View
from .models import BlogModel, BlogContentModel
from django.shortcuts import get_object_or_404


class BlogView(View):
    def get(self, request):
        blog_data = BlogModel.objects.all()
        context = {
            'blog_data': blog_data
        }
        return render(request, 'blog/BLOG.html', context)


class BlogDetailView(View):
    def get(self, request, blog_pk):
        blog = get_object_or_404(BlogModel, pk=blog_pk)
        data = BlogContentModel.objects.filter(blog=blog)
        context = {
            'blog': blog,
            'data': data
        }
        return render(request, 'blog/BLOG-detail.html', context)
