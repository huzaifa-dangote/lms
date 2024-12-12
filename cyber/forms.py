from django import forms
from django.forms import ModelForm, widgets
from .models import Content, Course

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["title", "content"]
        
        widgets = {
            "title": forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "content": forms.Textarea(attrs={"class": "w3-input w3-border", "rows": "12"})    
        }
        
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["title", "content", "assigned_to", "skill_level", "description", "image", "start_date", "end_date"]
        
        widgets = {
            "title": forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "content": forms.Select(attrs={}),
            "assigned_to": forms.CheckboxSelectMultiple(attrs={}),
            "skill_level": forms.Select(attrs={}),
            "description": forms.TextInput(attrs={"class": "w3-input w3-border"}),
            "image": forms.ClearableFileInput(attrs={}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"})
        }