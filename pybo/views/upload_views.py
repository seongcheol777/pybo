import os
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB


@login_required
@require_POST
def image_upload(request):
    image = request.FILES.get('image')
    if not image:
        return JsonResponse({'error': '이미지 파일이 없습니다.'}, status=400)

    ext = ''
    if '.' in image.name:
        ext = '.' + image.name.rsplit('.', 1)[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return JsonResponse({'error': '지원하지 않는 파일 형식입니다. (jpg/png/gif/webp)'}, status=400)

    if image.size > MAX_SIZE_BYTES:
        return JsonResponse({'error': '파일 크기는 2MB 이하여야 합니다.'}, status=400)

    # 고유한 파일명으로 media/uploads/ 에 저장
    filename = uuid.uuid4().hex + ext
    save_path = os.path.join('uploads', filename)
    saved_name = default_storage.save(save_path, image)

    url = settings.MEDIA_URL + saved_name.replace('\\', '/')
    return JsonResponse({'url': url})
