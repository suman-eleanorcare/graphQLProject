import strawberry.dataloader
from .models import Book
from strawberry.types import Info
from strawberry import auto
from .models import UserData
from django.contrib.auth.models import User
# Create your views here.
import strawberry

@strawberry.django.type(Book)
class BookType():
    id : auto
    title :auto
    author : auto


@strawberry.django.type(UserData)
class UserDataType:
    id: auto
    title: auto
    description: auto
    created_at: auto

@strawberry.type
class Query:
    @strawberry.field
    def my_data(self, info: Info) -> list[UserDataType]:
        user =info.context['request'].user
        if user.is_authenticated:
            return UserData.objects.filter(user=user)
        raise Exception("Authentication required")

    books : list[BookType] = strawberry.django.field()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_data(self, info: Info, title: str, description: str) -> UserDataType:

        user = info.context['request'].user
        if user.is_authenticated:
            new_data = UserData.objects.create(user=user, title=title, description=description)
            return new_data
        raise Exception("Authentication required")

schema = strawberry.Schema(query=Query, mutation=Mutation)

