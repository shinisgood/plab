from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from users import views

app_name = "users"
urlpatterns = [
    # 회원가입
    path("/registration", views.RegisterView.as_view(), name="rest_register"),
    # 로그인
    path("/login", LoginView.as_view(), name="rest_login"),
    path("/logout", LogoutView.as_view(), name="rest_logout"),
    path("/password/change", PasswordChangeView.as_view(), name="rest_password_change"),
    # 소셜 로그인
    path("/kakao/login", views.KakaoLogin.as_view()),
    path(
        "/kakao/login/callback",
        views.KakaoCallbackViewSet.as_view(),
    ),
]
