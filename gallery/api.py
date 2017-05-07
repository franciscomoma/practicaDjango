import base64
import os

from PIL import Image
from rest_framework import views
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from museum.models import Picture
from gallery import tasks as gallery_tasks
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class ImageUploadView(views.APIView):
    parser_classes = (MultiPartParser,)
    allowed_content_types = ('image/png', 'image/jpeg', )

    def post(self, request, format=None):
        file_obj = request.data.get('file') or None

        if not file_obj:
            return Response({'error': _('Missing \'file\' parameter in request')}, status=400)

        if file_obj.content_type not in self.allowed_content_types:
            return Response({'error': _(u'File content type {0} not allowed'.format(file_obj.content_type)),
                             'file': file_obj.name}, status=400)

        file_path = os.path.join(settings.BASE_DIR, 'temp', file_obj.name)

        Image.open(file_obj).save(file_path)
        gallery_tasks.museum_create_picture_by_image.delay(file_path, request.user.pk)

        return Response({'success': _(u'Image uploaded succesfully')}, status=200)
