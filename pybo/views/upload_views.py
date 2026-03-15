import base64
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
ALLOWED_MIME_TYPES = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
}
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

    data = image.read()
    if len(data) > MAX_SIZE_BYTES:
        return JsonResponse({'error': '파일 크기는 2MB 이하여야 합니다.'}, status=400)

    mime = ALLOWED_MIME_TYPES[ext]
    b64 = base64.b64encode(data).decode('utf-8')
    data_url = f'data:{mime};base64,{b64}'

    return JsonResponse({'url': data_url})
