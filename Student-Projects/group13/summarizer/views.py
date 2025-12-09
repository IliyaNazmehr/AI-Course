from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from huggingface_hub import InferenceClient
from .forms import SummaryForm
from .models import SummaryHistory


def summary_view(request):
    """
    Main summarizer view.
    Handles:
    - Form submission
    - Calling the HuggingFace summarization model
    - Saving history (if the user is logged in)
    - Storing data temporarily in the session
    """
    if request.method == "POST":
        form = SummaryForm(request.POST)
        
        if form.is_valid():
            text = form.cleaned_data['text']

            # HuggingFace summarization API call
            client = InferenceClient(api_key=settings.HUGGINGFACE_API_KEY)
            result = client.summarization(
                text, model="facebook/bart-large-cnn")
            summary = result["summary_text"]
            
            # Store result temporarily in session
            request.session['summary'] = summary
            request.session['original_text'] = text
            
            # Save history for logged-in users
            if request.user.is_authenticated:
                SummaryHistory.objects.create(
                    user=request.user,
                    input_text=text,
                    summary_text=summary
                )
            messages.success(
                request, "Your summary has been generated successfully!")
            return redirect('summary_result')

    else:

        # When loading the page normally: clear leftover session data
        request.session.pop('summary', None)
        request.session.pop('original_text', None)
        form = SummaryForm()

    return render(request, "summarizer/home.html", {"form": form})


def summary_result_view(request):
    """
    Shows the final summary result after processing.
    Prevents direct access if no summary exists in the session.
    """
    summary = request.session.get('summary')
    original_text = request.session.get('original_text')
    
    # Protect the page from direct access
    if not summary:
        messages.warning(
            request, "No summary found. Please submit text first.")
        return redirect('sum')  

    return render(request, "summarizer/result.html", {
        "summary": summary,
        "original_text": original_text
    })

@login_required
def history_view(request):
    """
    Displays the logged-in user's summary history with pagination.
    """
    # Filter history by current user only
    histories = SummaryHistory.objects.filter(user=request.user).order_by('-created_at')
    
    # Clean pagination (handles invalid pages automatically)
    paginator = Paginator(histories, 2)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "summarizer/history.html", {"page_obj": page_obj})