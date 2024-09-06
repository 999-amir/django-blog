from rest_framework import serializers
from private_data.models import PrivateDataModel
from private_data.cryptography import encrypt, decrypt


class PrivateDataSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(
        method_name="get_abs_url"
    )

    class Meta:
        model = PrivateDataModel
        fields = (
            "pk",
            "user",
            "title",
            "username",
            "password",
            "updated",
            "created",
            "absolute_url",
        )
        read_only_fields = ("user", "updated", "created")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("absolute_url")
            rep["username"] = decrypt(rep["username"])
            rep["password"] = decrypt(rep["password"])
        else:
            rep.pop("username", None)
            rep.pop("password", None)
        return rep

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        validated_data["username"] = encrypt(validated_data["username"])
        validated_data["password"] = encrypt(validated_data["password"])
        return super().create(validated_data)
