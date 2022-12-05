from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if 'username' not in validated_data:
            if 'email' not in validated_data and 'phone' not in validated_data:
                raise ValidationError(_('Email or phone should be provided'))

        return validated_data



class PasswordValidationSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as ex:
            raise ValidationError(ex.messages)
        return password


class BaseUserSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'uuid', 'first_name', 'last_name', 'fullname', 'email', 'phone', 'about', 'photo',
            'gender', 'password',
        )
        read_only_fields = ('uuid',)

    def get_photo(self, obj):
        photo = obj.photo
        if not photo:
            return
        return UserPhotoSerializer(obj).data

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)

        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user


class UserStatisticSerializerMixin:
    filters_amount = serializers.ReadOnlyField()

    class Meta:
        fields = ('filters_amount',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data['old_password'] == validated_data['new_password']:
            raise ValidationError(_('Aww don\'t use the same password! For security reasons, please use a different '
                                    'password to your old one'))
        elif not self.context['request'].user.check_password(validated_data['old_password']):
            raise ValidationError(_('You\'ve entered an incorrect old password, please try again.'))

        return validated_data
