from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question, Category   # ← Category import 추가


@login_required(login_url='common:login')
def question_create(request, slug=None):  # ← slug 파라미터 추가
    """
    pybo 질문 등록 (카테고리 페이지에서 들어오면 해당 카테고리로 기본 선택)
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()

            # 카테고리 페이지에서 폼에 카테고리를 비워 제출하면 slug로 보정
            if slug and not question.category:
                question.category = get_object_or_404(Category, slug=slug)

            question.save()

            # 저장 후 리다이렉트: 카테고리가 있으면 해당 카테고리 목록으로
            if question.category:
                return redirect('pybo:question_list_by_category', question.category.slug)
            return redirect('pybo:index')
    else:
        initial = {}
        # 카테고리 페이지에서 들어온 경우 기본값 세팅
        if slug:
            initial['category'] = get_object_or_404(Category, slug=slug)
        form = QuestionForm(initial=initial)

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
