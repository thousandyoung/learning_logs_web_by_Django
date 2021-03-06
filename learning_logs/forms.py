from django import forms
from .models import Topic, Entry
from mdeditor.fields import MDTextFormField



class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}





class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = {'title','text','tags'}
        labels = {'text': ''}
        widgets = {'text': forms.Textarea()}

