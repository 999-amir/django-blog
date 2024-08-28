from rest_framework import serializers
from accounts.models import CostumeUser
from accounts.incs import check_signup_data, check_password_strength
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserAndSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = CostumeUser
        fields = ['name', 'email', 'password', 'confirm_password', 'is_verify', 'is_admin', 'last_login', 'updated', 'created']
        read_only_fields = ['is_verify', 'is_admin', 'last_login']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('password', None)
        return rep

    def validate(self, attrs):
        check_response = check_signup_data(attrs.get('name'), attrs.get('email'), attrs.get('password'), attrs.get('confirm_password'))
        if not check_response['mode']:
            raise serializers.ValidationError({'detail': check_response['message']})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        validated_data.pop('last_login', None)
        return CostumeUser.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=250)
    new_password1 = serializers.CharField(max_length=250)
    new_password2 = serializers.CharField(max_length=250)

    def validate(self, attrs):
        check_response = check_password_strength(attrs.get('new_password1'), attrs.get('new_password2'))
        if not check_response['mode']:
            raise serializers.ValidationError({'detail': check_response['message']})
        return super().validate(attrs)


# SESSION
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=250)
    password = serializers.CharField(max_length=250)


# TOKEN
class TokenLoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verify:
                raise serializers.ValidationError({'detail': 'account still not verified'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


# JWT
class JWTCreateSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verify:
            raise serializers.ValidationError({'detail': 'account still not verified'})
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data


# JWT - activate user
class SendActivateTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        user = CostumeUser.objects.filter(email=email)
        if not user.exists():
            raise serializers.ValidationError({'detail': 'user does not exist'})
        elif user.first().is_verify:
            raise serializers.ValidationError({'detail': 'user has been verified before'})
        attrs['user'] = user.first()
        return super().validate(attrs)


# JWT - forget password
class SendForgetPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        user = CostumeUser.objects.filter(email=attrs.get('email'))
        if not user.exists():
            raise serializers.ValidationError({'detail': 'user does not exist'})
        attrs['user'] = user.first()
        return super().validate(attrs)


class ConfirmForgetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=250)
    new_password2 = serializers.CharField(max_length=250)

    def validate(self, attrs):
        check_response = check_password_strength(attrs.get('new_password1'), attrs.get('new_password2'))
        if not check_response['mode']:
            raise serializers.ValidationError({'detail': check_response['message']})
        return super().validate(attrs)
