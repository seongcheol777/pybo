import markdown
from django import template
from django.utils.safestring import mark_safe

register=template.Library()

@register.filter
def sub(value,arg):
    return value - arg

@register.filter
def page_range_10(page_obj):
    """현재 페이지 기준 최대 10개의 페이지 번호 리스트 반환"""
    current = page_obj.number
    total = page_obj.paginator.num_pages
    half = 5
    start = max(1, current - (half - 1))
    end = min(total, start + 9)
    # end가 부족하면 start를 앞으로 당김
    start = max(1, end - 9)
    return range(start, end + 1)

@register.filter()
def mark(value):
    extensions = ["nl2br","fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
