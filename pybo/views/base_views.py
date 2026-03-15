from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question, Category, Tag, Notification

# 로그인 필요 카테고리 이름 목록
LOGIN_REQUIRED_CATEGORIES = {'공지', '자료실', 'Q&A'}


def index(request, slug=None):
    page = request.GET.get('page', '1')
    kw   = request.GET.get('kw', '')
    so   = request.GET.get('so', 'recent')

    active_category = None
    qs = Question.objects.all()
    if slug:
        active_category = get_object_or_404(Category, slug=slug)
        if active_category.name in LOGIN_REQUIRED_CATEGORIES and not request.user.is_authenticated:
            return redirect('common:login')
        qs = qs.filter(category=active_category)

    if so == 'recommend':
        qs = qs.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        qs = qs.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        qs = qs.order_by('-create_date')

    if kw:
        qs = qs.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw) |
            Q(tags__name__icontains=kw)
        ).distinct()

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'so': so,
        'active_category': active_category,
    }
    return render(request, 'pybo/question_list.html', context)


def tag_index(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    page = request.GET.get('page', '1')
    so   = request.GET.get('so', 'recent')

    qs = Question.objects.filter(tags=tag)
    if so == 'recommend':
        qs = qs.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        qs = qs.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        qs = qs.order_by('-create_date')

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': '',
        'so': so,
        'active_tag': tag,
        'active_category': None,
    }
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 카테고리별 로그인 접근 제어
    if question.category and question.category.name in LOGIN_REQUIRED_CATEGORIES:
        if not request.user.is_authenticated:
            messages.error(request, '로그인이 필요한 게시판입니다.')
            return redirect('common:login')
    # 조회수 증가 (본인 제외)
    if not request.user.is_authenticated or request.user != question.author:
        Question.objects.filter(pk=question_id).update(view_count=question.view_count + 1)
        question.refresh_from_db()
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def mypage(request):
    my_questions = Question.objects.filter(author=request.user).order_by('-create_date')
    from ..models import Answer
    my_answers = Answer.objects.filter(author=request.user).order_by('-create_date')
    context = {
        'my_questions': my_questions,
        'my_answers': my_answers,
    }
    return render(request, 'pybo/mypage.html', context)


@login_required(login_url='common:login')
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications.filter(is_read=False).update(is_read=True)
    context = {'notifications': notifications}
    return render(request, 'pybo/notification_list.html', context)
