from .models import Comment, Chapter
from django import forms


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Напишите комментарий',
        'class': 'rate__textarea',
        'id': 'rateTextarea'
    }), label='', max_length=1024)

    class Meta:
        model = Comment
        fields = ('text',)


class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ('title', 'novel', 'number', 'content')