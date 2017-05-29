from django.conf.urls import url

from auth_api import views

urlpatterns = [
    url(r"^signup$", views.SignupView.as_view(), name="signup"),
]
