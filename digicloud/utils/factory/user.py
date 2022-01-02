import factory
from factory.django import DjangoModelFactory

from digicloud.user_management.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'digicloud%s' % n)
    mobile = '09366403388'
    password = factory.PostGenerationMethodCall('set_password', 'test12345')
    email = factory.Sequence(lambda n: 'havig%d@gmail.com' % n)
    first_name = factory.Sequence(lambda n: 'havig%d' % n)
    last_name = factory.Sequence(lambda n: 'havig%d' % n)
