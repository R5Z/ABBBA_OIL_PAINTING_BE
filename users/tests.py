from django.urls import reverse # 함수 거꾸로 불러오기
from rest_framework.test import APITestCase # 테스트 케이스 임포트 함수 생성
from rest_framework import status # 상태코드 함수 생성


class UserRegistrationAPIViewTestCase(APITestCase):     
    def test_registration(self):                        # 회원가입 성공 테스트 함수 작성
        url = reverse("user_view")                      # urls.py에서 거꾸로 name='user_view' > views.UserView.as_view() > path('') 함수 순서대로 불러온다
        user_data = {                                   
        "nickname": "nickname1",                        
        "email": "test@testuser.com",                   
        "password": "password1",                        
        "password_check": "password1",                  
        }                                               
        response = self.client.post(url, user_data)     # url 및 user 데이터 가져오기
        self.assertEqual(response.status_code, 201)     # 상태코드가 201이 맞는지 주장하기 (테스트 실행 시작)
        
        
    def test_registration_failed(self):                 # 회원가입 실패 테스트 함수 생성
        url = reverse("user_view")                      # urls.py에서 거꾸로 name='user_view' > views.UserView.as_view() > path('') 함수 순서대로 불러온다
        user_data = {                                   
        "nickname": "nickname1",                        
        "email": "test@testuser.com",                   
        "password": "password1",                        
        "password_check": "password!",                  # 다른 비밀번호 입력
        }                                               
        response = self.client.post(url, user_data)     # url 및 user 데이터 가져오기
        self.assertEqual(response.status_code, 400)     # 상태코드가 400이 맞는지 주장하기 (테스트 실행 시작)