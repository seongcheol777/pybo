from django import forms
from pybo.models import Question, Answer, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'category', 'attachment']
        labels = {
            'subject': '제목',
            'content': '내용',
            'category': '카테고리',
            'attachment': '첨부파일',
        }
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'id': 'content'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('카테고리를 선택해주세요.')
        return category


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'attachment']
        labels = {
            'content': '답변내용',
            'attachment': '첨부파일',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'id': 'answer_content'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': '댓글내용'}
