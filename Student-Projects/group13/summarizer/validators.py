import re
from django.core.exceptions import ValidationError
from langdetect import detect, LangDetectException
from django.core.exceptions import ValidationError

def max_words_validator(value):
    """
    Validates that the input text does not exceed the allowed word limit.
    A 'word' is any sequence of alphanumeric characters.
    """
    words = re.findall(r'\b\w+\b', value)
    if len(words) > 500:
        raise ValidationError(f"Max 500 words allowed. You wrote {len(words)}.")

def english_only_validator(value):
    """
    Detects input language using langdetect.
    Requires the text to be English ('en').
    """
    try:
        detected = detect(value)
        if detected != 'en':
            raise ValidationError("Only English text is supported.")
    except LangDetectException:
        raise ValidationError("Unable to detect language. Please enter English text.")