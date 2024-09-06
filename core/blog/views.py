from django.shortcuts import render, redirect
from django.views import View
from .models import BlogModel, BlogContentModel, CategoryModel
from django.shortcuts import get_object_or_404
from .forms import CreateBlogTitleForm, CreateBlogContentForm
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError


class BlogView(View):
    def get(self, request):
        blog_data = BlogModel.objects.all()
        category_names = [str(i) for i in request.GET.getlist("category")]
        if category_names:
            blog_data = blog_data.filter(category__name__in=category_names)
        context = {
            "category": CategoryModel.objects.all(),
            "blog_data": blog_data,
        }
        return render(request, "blog/BLOG.html", context)


class BlogDetailView(View):
    def get(self, request, blog_title):
        blog = get_object_or_404(BlogModel, title=blog_title)
        data = BlogContentModel.objects.filter(blog=blog)
        context = {"blog": blog, "data": data}
        return render(request, "blog/BLOG-detail.html", context)


class CreateBlogTitleView(View):
    form_class = CreateBlogTitleForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "blog/BLOG-detail.html",
                {"notif": "need registration"},
            )
        elif not request.user.is_verify:
            return render(
                request,
                "blog/BLOG-detail.html",
                {"notif": "please activate your account"},
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        forms = self.form_class()
        category = CategoryModel.objects.all()
        context = {"forms": forms, "category": category}
        return render(request, "blog/create_blog/title.html", context)

    def post(self, request):
        forms = self.form_class(request.POST)
        category = CategoryModel.objects.all()
        context = {"forms": forms, "category": category}
        if forms.is_valid():
            cd = forms.cleaned_data
            if BlogModel.objects.filter(title=cd["title"]).exists():
                messages.warning(request, "title already exist", "amber-600")
                return render(request, "blog/create_blog/title.html", context)
            blog = BlogModel.objects.create(
                title=cd["title"], snippet=cd["snippet"], user=request.user
            )
            for c in cd["category"]:
                blog.category.add(c)
            blog.save()
            messages.success(request, "title created", "green-600")
            return render(
                request,
                "blog/create_blog/content.html",
                {"blog_title": blog.title},
            )


class CreateBlogContentView(View):
    form_class = CreateBlogContentForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "blog/BLOG-detail.html",
                {"notif": "need registration"},
            )
        elif not request.user.is_verify:
            return render(
                request,
                "blog/BLOG-detail.html",
                {"notif": "please activate your account"},
            )
        self.blog = get_object_or_404(
            BlogModel, title=self.kwargs["blog_title"], user=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, blog_title):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            try:
                file = request.FILES["file"]
            except MultiValueDictKeyError:
                if cd["text"] == "":
                    messages.warning(
                        request,
                        "at least one field should be filled",
                        "amber-600",
                    )
                    context = {"forms": forms, "blog_title": blog_title}
                    return render(
                        request, "blog/create_blog/content.html", context
                    )
                file = None
            BlogContentModel.objects.create(
                blog=self.blog, text=cd["text"], file=file
            )
            messages.success(request, "new content added", "green-600")
            return render(
                request,
                "blog/create_blog/content.html",
                {"blog_title": blog_title},
            )


class EditBlogContentView(View):
    form_class = CreateBlogContentForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "blog/BLOG-detail.html",
                {"notif": "need registration"},
            )
        elif not request.user.is_verify:
            return render(
                request,
                "blog/BLOG-detail.html",
                {"notif": "please activate your account"},
            )
        content = BlogContentModel.objects.filter(
            blog__user=request.user, id=self.kwargs["blog_content_pk"]
        )
        if not content.exists():
            return render(
                request,
                "blog/BLOG-detail.html",
                {"notif": "unavailable content"},
            )
        self.content = content.first()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, blog_content_pk):
        return render(
            request,
            "blog/create_blog/edit_content.html",
            {"blog_content_pk": blog_content_pk},
        )

    def post(self, request, blog_content_pk):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            try:
                file = request.FILES["file"]
            except MultiValueDictKeyError:
                if cd["text"] == "":
                    messages.warning(
                        request,
                        "at least one field should be filled",
                        "amber-600",
                    )
                    context = {
                        "forms": forms,
                        "blog_content_pk": blog_content_pk,
                    }
                    return render(
                        request, "blog/create_blog/edit_content.html", context
                    )
                file = None
            self.content.text = cd["text"]
            self.content.file = file
            self.content.save()
            return redirect("blog:detail", self.content.blog.title)
