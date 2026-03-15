from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question, Category, Tag


def _save_tags(question, tag_str):
    question.tags.clear()
    for name in [t.strip() for t in tag_str.split(',') if t.strip()]:
        tag, _ = Tag.objects.get_or_create(name=name)
        question.tags.add(tag)


@login_required(login_url='common:login')
def question_create(request, slug=None):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()

            if slug and not question.category:
                question.category = get_object_or_404(Category, slug=slug)

            question.save()
            _save_tags(question, request.POST.get('tags', ''))

            if question.category:
                return redirect('pybo:question_list_by_category', question.category.slug)
            return redirect('pybo:index')
    else:
        initial = {}
        if slug:
            initial['category'] = get_object_or_404(Category, slug=slug)
        form = QuestionForm(initial=initial)

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            _save_tags(question, request.POST.get('tags', ''))
            return redirect('pybo:detail', question_id=question.id)
    else:
        current_tags = ', '.join(t.name for t in question.tags.all())
        form = QuestionForm(instance=question)

    context = {
        'form': form,
        'current_tags': ', '.join(t.name for t in question.tags.all()),
    }
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
