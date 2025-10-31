from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count

from ..models import Question, Category   # ← Category 추가

def index(request, slug=None):            # ← slug 파라미터 추가
    """
    pybo 목록 출력 (카테고리 필터 + 정렬 + 검색 + 페이징)
    """
    # 입력 인자
    page = request.GET.get('page', '1')     # 페이지
    kw   = request.GET.get('kw', '')        # 검색어
    so   = request.GET.get('so', 'recent')  # 정렬 기준

    # 기본 쿼리셋 + 카테고리 필터
    active_category = None
    qs = Question.objects.all()
    if slug:
        active_category = get_object_or_404(Category, slug=slug)
        qs = qs.filter(category=active_category)

    # 정렬
    if so == 'recommend':
        qs = qs.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        qs = qs.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        qs = qs.order_by('-create_date')

    # 검색
    if kw:
        qs = qs.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'so': so,
        'active_category': active_category,   # ← 사이드바 활성표시용
    }
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
