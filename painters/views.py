from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
import mimetypes
import os
from django.http import HttpResponse, Http404
import urllib
from .models import Painting
from painters.models import Painting, Painter
from painters.serializers import ImageCreateSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from uuid import uuid4
from PIL import Image
import os
from painters.serializers import ImageCreateSerializer

"""
def Download_view(request, pk):
    painting = get_object_or_404(Painting, pk=pk)
    url = painting.image.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            # quote_file_url = urllib.parse.quote(painting.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            # response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404
"""    
    
class ImageView(APIView) :
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        draft = Painting.objects.all()
        serializer = ImageCreateSerializer(draft, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ImageCreateSerializer(data=request.data)
        article = Painting()
        if serializer.is_valid():
            serializer.save()

        article.user = request.user
        article.painter = Painting.objects.get(id=request.data['painter'])
        article.style_id = serializer.data['id']
        
        image_uuid = uuid4().hex
        image_painter = Painter.objects.get(id=request.data['painter']).image.name
        print(image_painter)
        print(serializer.data)
        os.system('python style_transfer/cli.py media/'+ image_painter +' '+ serializer.data['image'][1:] +' -s 156 -ii 1 -o media/image/'+ image_uuid +'.png')
        os.system('rembg i media/painting/'+ image_uuid +'.png media/painting/'+ image_uuid +'.png')
        
        image = Image.open('media/uploads/painting/' + image_uuid + '.png')
        article.image = 'result/' + image_uuid + '.png' #cv2
        article.save()

        

        return Response(article.data, status=status.HTTP_200_OK)