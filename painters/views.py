from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
import mimetypes
from uuid import uuid4
from PIL import Image
import os
from django.http import FileResponse, HttpResponse, Http404
import urllib
from painters.models import Painting, Painter
from painters.serializers import ImageCreateSerializer
from painters.serializers import ImageCreateSerializer, ConvertSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from uuid import uuid4
from PIL import Image
import os
from painters.serializers import ImageCreateSerializer


def Download_view(request, pk):
    painting = get_object_or_404(Painting, pk=pk)
    url = painting.painting.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            # quote_file_url = urllib.parse.quote(painting.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            # response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
        return HttpResponse({"response":response, "href" : painting.painting})
    raise Http404

    
class ConvertView(APIView) :

    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save(user_id=request.user.id) # save시에는 데이터베이스의 테이블의 필드명으로 들어간다. request로 보낼 때는 모델링의 필드명 기준으로 들어간다.
  
        
        paint = Painting.objects.get(id=serializer.data["id"])
        
        painter_id = paint.painter_id
        painter = Painter.objects.get(id=painter_id)
        style = painter.style
        

        image_painter = str(style)
        
      
        os.system(f"python3 /Users/lgb/Desktop/ABBBA_OIL_PAINTING_BE/painters/style_transfer/cli.py /Users/lgb/Desktop/ABBBA_OIL_PAINTING_BE/{serializer.data['picture'][1:]} /Users/lgb/Desktop/ABBBA_OIL_PAINTING_BE/media/{image_painter} -s 156 -ii 100")
        
        paint.painting = "/Users/lgb/Desktop/ABBBA_OIL_PAINTING_BE/out.png"
        paint.save()
        return Response({"message" : "변환이 완료되었습니다!"}, status=status.HTTP_200_OK)


class ImageView(APIView) :
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id):
        painting = Painting.objects.filter(id=id)
        serializer = ImageCreateSerializer(painting, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)