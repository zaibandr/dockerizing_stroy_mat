from haystack.forms import SearchForm
from django.forms import ModelForm, Textarea
from has_app.models import Comment


class OrderSearchForm(SearchForm):
    pass


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'cols': 40, 'rows': 4}),
        }
