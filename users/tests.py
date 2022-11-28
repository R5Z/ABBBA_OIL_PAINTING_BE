from django.urls import reverse 
from rest_framework.test import APITestCase 


class UserRegistrationAPIViewTestCase(APITestCase):     
    def test_registration(self):                        # 회원가입 성공 테스트 함수 작성
        url = reverse("user_view")                      
        user_data = {                                   
        "nickname": "nickname1",                        
        "email": "test@testuser.com",                   
        "password": "password1",                        
        "password_check": "password1",                  
        }                                               
        response = self.client.post(url, user_data)     # url 및 user 데이터 가져오기
        self.assertEqual(response.status_code, 201)     # 상태코드가 201이 맞는지 (테스트 실행 시작)
        
        
    def test_registration_failed(self):                 # 회원가입 실패 테스트 함수 생성
        url = reverse("user_view")                     
        user_data = {                                   
        "nickname": "nickname1",                        
        "email": "test@testuser.com",                   
        "password": "password1",                        
        "password_check": "password!",                  # 다른 비밀번호 입력
        }                                               
        response = self.client.post(url, user_data)     # url 및 user 데이터 가져오기
        self.assertEqual(response.status_code, 400)     # 상태코드가 400이 맞는지 (테스트 실행 시작)