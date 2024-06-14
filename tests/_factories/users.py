import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda index: f"user{index}")
    password = factory.PostGenerationMethodCall("set_password", "237")

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            instance.save()
