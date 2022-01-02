from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
import logging

from digicloud.user_management.models import User

logger = logging.getLogger(__name__)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'mobile', 'email', 'password', 'username')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}},
            'email': {
                'validators': [
                    UniqueValidator(User.objects.all(), message=_('An account already exists with this email'))],
                'required': True
            },
        }

    def validate(self, data):
        data = super(CreateUserSerializer, self).validate(data)
        try:
            django_validate_password(data['password'], User(**data))
        except DjangoValidationError:
            raise ValidationError({'password': _('Password is not Strong Enough.')}, 'week')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        mobile=validated_data.get('mobile', None),
                                        )
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
