import requests

from django.conf import settings
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View

from json.decoder import JSONDecodeError

from rest_framework import status

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from dj_rest_auth.registration.views import SocialLoginView
from users.serializers import UserSerializer

from users.models import User
from rest_framework import viewsets

BASE_URL = "http://127.0.0.1:8000/"
# BASE_URL = "http://3.34.245.245:8000/"
# BASE_URL = "https://andn.co.kr/"
KAKAO_LOGIN_URI = BASE_URL + "users/kakao/login/"
KAKAO_CALLBACK_URI = BASE_URL + "users/kakao/callback"
REST_API_KEY = "00da61755b3457017e230221d87e2cd5"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class KakaoCallbackViewSet(View):
    def get(self, request):
        auth_code = request.GET.get("code")
        REDIRECT_URI = KAKAO_CALLBACK_URI
        client_id = "80087b6e7ff6d1252e9f6fb8c5b55eb8"
        kakao_token_api = "https://kauth.kakao.com/oauth/token"

        """
        Access Token Request
        """
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirection_uri": REDIRECT_URI,
            "code": auth_code,
        }
        token_response = requests.post(kakao_token_api, data=data)
        token_response_json = token_response.json()
        error = token_response_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        kakao_access_token = token_response_json.get("access_token")

        """
        Email Request
        """
        kakao_user_info_api = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer ${kakao_access_token}"}
        profile_request = requests.get(
            kakao_user_info_api,
            headers=headers,
        )

        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")

        """
        kakao_account에서 이메일 외에
        카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
        print(kakao_account) 참고
        """
        email = kakao_account.get("email")

        """
        Signup or Signin Request
        """
        try:
            user = User.objects.get(email=email)
            # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
            # 가입은 되어있으나 소셜로그인이 아닌 계정
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return JsonResponse(
                    {"err_msg": "email exists but not social user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # 소셜로그인은 맞으나 kakao가 아닌 sns계정으로 가입된 유저
            if social_user.provider != "kakao":
                return JsonResponse(
                    {"err_msg": "no matching social type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # 기존에 kakao로 가입된 유저
            data = {"access_token": kakao_access_token, "code": auth_code}
            accept = requests.post(KAKAO_LOGIN_URI, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signin"}, status=accept_status
                )
            accept_json = accept.json()
            # accept_json.pop("user", None)
            return JsonResponse(accept_json)

        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            data = {"access_token": kakao_access_token, "code": auth_code}
            accept = requests.post(KAKAO_LOGIN_URI, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signup"},
                    status=accept_status,
                )
            # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
            accept_json = accept.json()
            # accept_json.pop("user", None)
            return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
