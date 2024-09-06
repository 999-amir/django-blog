from rest_framework.viewsets import ModelViewSet
from blog.models import BlogModel, BlogContentModel, CategoryModel
from .serializers import (
    BlogSerializer,
    BlogDetailSerializer,
    CategorySerializer,
)
from .permissions import IsOwnerOrReadonly
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status


class CategoryAPIView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()


class BlogAPIView(ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = BlogModel.objects.all()


class BlogContentAPIView(GenericAPIView):
    serializer_class = BlogDetailSerializer
    permission_classes = [IsOwnerOrReadonly]

    def get(self, request, blog_title):
        blog = get_object_or_404(BlogModel, title=blog_title)
        items = BlogContentModel.objects.filter(blog=blog)
        serializer = self.serializer_class(items, many=True)
        if blog.user:
            author = blog.user.name
        else:
            author = "deleted_account"
        data = {
            "blog": {
                "title": blog.title,
                "author": author,
                "snippet": blog.snippet,
                "content": serializer.data,
            }
        }
        return Response(data)

    def post(self, request, blog_title):
        blog = get_object_or_404(BlogModel, title=blog_title)
        if blog.user != request.user:
            return Response(
                {"detail": "only author can add content"},
                status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        try:
            file = request.FILES["file"]
        except MultiValueDictKeyError:
            if serializer_data["text"] == "":
                return Response(
                    {"detail": "at least one field should be filled"},
                    status.HTTP_400_BAD_REQUEST,
                )
            file = None
        BlogContentModel.objects.create(
            blog=blog, text=serializer_data["text"], file=file
        )
        return Response({"detail": "new content added"})


class EditBlogContentView(GenericAPIView):
    serializer_class = BlogDetailSerializer
    permission_classes = [IsOwnerOrReadonly]

    def get(self, request, content_id):
        item = get_object_or_404(BlogContentModel, id=content_id)
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    def put(self, request, content_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        try:
            file = request.FILES["file"]
        except MultiValueDictKeyError:
            if serializer_data["text"] == "":
                return Response(
                    {"detail": "at least one field should be filled"},
                    status.HTTP_400_BAD_REQUEST,
                )
            file = None
        content = get_object_or_404(BlogContentModel, id=content_id)
        content.file = file
        content.text = serializer_data["text"]
        content.save()
        return Response({"detail": "content updated"})
