from .models import Category

def categories_nav(request):
    # 사이드바에 쓸 카테고리 목록 전역 주입
    return {"categories": Category.objects.all().order_by('order','name')}