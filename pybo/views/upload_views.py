import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


@login_required
@require_POST
def image_upload(request):
    image = request.FILES.get('image')
    if not image:
        return JsonResponse({'error': '이미지 파일이 없습니다.'}, status=400)

    ext = os.path.splitext(image.name)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        return JsonResponse({'error': '지원하지 않는 파일 형식입니다.'}, status=400)

    filename = uuid.uuid4().hex + ext
    save_dir = os.path.join(settings.MEDIA_ROOT, 'editor_images')
    os.makedirs(save_dir, exist_ok=True)

    filepath = os.path.join(save_dir, filename)
    with open(filepath, 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)

    url = settings.MEDIA_URL + 'editor_images/' + filename
    return JsonResponse({'url': url})
