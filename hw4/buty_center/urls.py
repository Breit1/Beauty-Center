from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AddressViewSet,
    CenterViewSet,
    ServiceViewSet,
    CommentsViewSet,
    CenterServiceViewSet,
)
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r"addresses", AddressViewSet)
router.register(r"centers", CenterViewSet)
router.register(r"services", ServiceViewSet)
router.register(r"comments", CommentsViewSet)
router.register(r"center-services", CenterServiceViewSet)
router.register(
    r"centers/(?P<center_id>[^/.]+)/comments", CommentsViewSet, basename="comment"
)

urlpatterns = [
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("", include(router.urls)),
    path(
        "centers/<uuid:pk>/services/",
        CenterViewSet.as_view({"get": "services"}),
        name="center-services",
    ),
    path(
        "centers/<uuid:center_id>/comments/",
        CommentsViewSet.as_view({"get": "retrieve_comments"}),
        name="center-comments",
    ),
    path("create_comment/", CommentsViewSet.create, name="create-comment"),
]
