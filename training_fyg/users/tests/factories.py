from typing import Any, Sequence

from django.contrib.auth import get_user_model

from factory import post_generation
from factory.django import DjangoModelFactory
from faker import Faker

fake = Faker("es_MX")


class UserFactory(DjangoModelFactory):
    username = fake.email()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
