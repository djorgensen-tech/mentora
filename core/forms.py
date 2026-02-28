from django import forms
from .models import Textbook


class TextbookUploadForm(forms.ModelForm):
    class Meta:
        model = Textbook
        fields = ['title', 'subject', 'grade_level', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Biology OpenStax 2e',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-400 text-sm',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'e.g. Biology, Algebra, History',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-400 text-sm',
            }),
            'grade_level': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-400 text-sm',
            }),
            'pdf_file': forms.FileInput(attrs={
                'accept': 'application/pdf',
                'class': 'hidden',
                'id': 'pdf-upload-input',
            }),
        }