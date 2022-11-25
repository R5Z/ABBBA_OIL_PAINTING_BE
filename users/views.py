from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from users.models import User
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, ProfileEditSerializer, ProfileSerializer
from rest_framework.pagination import PageNumberPagination
from painters.models import Painting
from users.pagination import PaginationHandlerMixin


class ListPagination(PageNumberPagination) :
    page_size_query_param = "limit"
    



class UserView(APIView):  
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if user:
            user.delete()
            return Response({"message":"지금까지 저희 서비스를 이용해 주셔서 감사합니다."}, status=status.HTTP_200_OK)
        return Response({"message":"이런... 탈퇴에 실패하셨습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView, PaginationHandlerMixin) :
    permission_classes = [IsAuthenticated]
    
    pagination_class = ListPagination
    serializer_class = ProfileSerializer
    
    # 프로필 보기
    def get(self, request, format=None, *args, **kwargs) :
        paintings = Painting.objects.filter(user=request.user.id)
        page = self.paginate_queryset(paintings)
        # serializer = self.serializer_class(paintings, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        if page is not None : 
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else :
            serializer = self.serializer_class(paintings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 닉네임과 비밀번호 변경
    def put(self, request) :
        user = get_object_or_404(User, id=request.user.id)
        if user == request.user :
            serializer = ProfileEditSerializer(user, data=request.data, context={"request":request})
            if serializer.is_valid() :
                serializer.save()
                return Response({"message":"변경 완료!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"본인만 수정할 수 있습니다"}, stauts=status.HTTP_403_FORBIDDEN)