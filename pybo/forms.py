from django import forms
from pybo.models import Question, Answer, Comment
# from .models import Question, Answer, Comment  # ← 앱 내부라면 이렇게 써도 OK

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'category']  # ← category 추가
        labels = {
            'subject': '제목',
            'content': '내용',
            'category': '카테고리',                    # ← 라벨 추가
        }
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # ← 셀렉트 박스
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {'content': '답변내용'}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': '댓글내용'}
