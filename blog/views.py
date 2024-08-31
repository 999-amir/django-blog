from django.shortcuts import render, redirect
from django.views import View
from .models import BlogModel, BlogContentModel
from django.shortcuts import get_object_or_404
from .forms import *
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError


class BlogView(View):
    def get(self, request):
        blog_data = BlogModel.objects.all()
        context = {
            'blog_data': blog_data
        }
        return render(request, 'blog/BLOG.html', context)


class BlogDetailView(View):
    def get(self, request, blog_title):
        blog = get_object_or_404(BlogModel, title=blog_title)
        data = BlogContentModel.objects.filter(blog=blog)
        context = {
            'blog': blog,
            'data': data
        }
        return render(request, 'blog/BLOG-detail.html', context)


class CreateBlogTitleView(View):
    form_class = CreateBlogTitleForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        elif not request.user.is_verify:
            messages.error(request, 'please activate your account', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        forms = self.form_class()
        return render(request, 'blog/create_blog/title.html', {'forms': forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            if BlogModel.objects.filter(title=cd['title']).exists():
                messages.warning(request, 'title already exist', 'amber-600')
                return render(request, 'blog/create_blog/title.html', {'forms': forms})
            blog = BlogModel.objects.create(title=cd['title'], snippet=cd['snippet'], user=request.user)
            messages.success(request, 'title created', 'green-600')
            return redirect('blog:create-content', blog.title)
        return render(request, 'blog/create_blog/title.html', {'forms': forms})


class CreateBlogContentView(View):
    form_class = CreateBlogContentForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        elif not request.user.is_verify:
            messages.error(request, 'please activate your account', 'amber-600')
            return redirect('home:main_page')
        self.blog = get_object_or_404(BlogModel, title=self.kwargs['blog_title'], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, blog_title):
        forms = self.form_class()
        return render(request, 'blog/create_blog/content.html', {'forms': forms})

    def post(self, request, blog_title):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            try:
                file = request.FILES['file']
            except MultiValueDictKeyError:
                if cd['text'] == '':
                    messages.warning(request, 'at least one field should be filled', 'amber-600')
                    return render(request, 'blog/create_blog/content.html', {'forms': forms})
                file = None
            BlogContentModel.objects.create(blog=self.blog, text=cd['text'], file=file)
            messages.success(request, 'new content added', 'green-600')
            return redirect('blog:create-content', self.blog.title)
        return render(request, 'blog/create_blog/content.html', {'forms': forms})

