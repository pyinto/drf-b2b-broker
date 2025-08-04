from datetime import UTC
from datetime import tzinfo
from zoneinfo import ZoneInfo

from django.conf import settings
import factory

TEST_PWD: str = "abcdefg123!"


class AbsUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"
        abstract = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.django.Password(TEST_PWD)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_joined = factory.Faker("date_time", tzinfo=ZoneInfo(settings.TIME_ZONE))
    is_staff: bool
    is_superuser: bool


class UserFactory(AbsUserFactory):
    is_staff = False
    is_superuser = False

    def __new__(cls, *args, **kwargs) -> "AbsUserFactory.Meta.model":
        return super().__new__(*args, **kwargs)


class AdminFactory(AbsUserFactory):
    is_staff = True
    is_superuser = True

    def __new__(cls, *args, **kwargs) -> "AbsUserFactory.Meta.model":
        return super().__new__(*args, **kwargs)
