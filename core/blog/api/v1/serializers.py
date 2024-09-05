from rest_framework import serializers
from blog.models import BlogModel, BlogContentModel, CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id', 'name', 'color', 'created')


class BlogSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    content_url = serializers.SerializerMethodField(method_name='get_content_url')

    class Meta:
        model = BlogModel
        fields = ('id', 'user', 'title', 'snippet', 'category', 'created', 'updated', 'absolute_url', 'content_url')
        read_only_fields = ('user', 'created', 'updated')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep['user']:
            rep['user'] = instance.user.name
        else:
            rep['user'] = 'user_deleted'
        rep['category'] = [c.name for c in instance.category.all()]
        request = self.context.get('request')
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('absolute_url', None)
            rep.pop('content_url', None)
        return rep

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def get_content_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'detail/{obj.title}')


class BlogDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogContentModel
        fields = ('id', 'text', 'filename', 'is_image', 'file', 'updated', 'created')
