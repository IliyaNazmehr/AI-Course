from django import forms
from .validators import max_words_validator, english_only_validator


class SummaryForm(forms.Form):
    """
    Form used to collect text input from the user for summarization.
    Includes a custom validator to enforce a maximum word limit.
    """
    text = forms.CharField(
        label="Text to Summarize",
        widget=forms.Textarea(attrs={
            "placeholder": "Enter your text here...",
            "rows": 6,   
        }),
        validators=[max_words_validator,english_only_validator],
        help_text="Maximum 500 words allowed.",
    )