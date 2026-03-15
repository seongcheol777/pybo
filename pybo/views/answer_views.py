from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer, Notification


def _notify(recipient, sender, ntype, question, answer=None):
    if recipient != sender:
        Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=ntype,
            question=question,
            answer=answer,
        )


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            _notify(question.author, request.user, 'answer', question, answer)
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_accept(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question
    if request.user != question.author:
        messages.error(request, '채택 권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if question.accepted_answer == answer:
        # 채택 취소
        question.accepted_answer = None
    else:
        question.accepted_answer = answer
        _notify(answer.author, request.user, 'accept', question, answer)
    question.save()
    return redirect('{}#answer_{}'.format(
        resolve_url('pybo:detail', question_id=question.id), answer.id))
