from django.urls import path
from .views import schema
from strawberry.django.views import GraphQLView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class CustomGraphQLView(GraphQLView):

    def get_context(self, request, response):
        jwt_authenticator = JWTAuthentication()
        try:
            user, _ = jwt_authenticator.authenticate(request)
        except Exception:
            user = AnonymousUser()

        request.user = user
        return {"request": request, "response": response}

urlpatterns = [
    path('graphql/', CustomGraphQLView.as_view(schema=schema)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]