from django.urls import path
from . import views
# URL patterns for the summarizer app
urlpatterns = [
    # Main page where the user inputs text to summarize
    path('', views.summary_view, name='sum'),

    # Page that displays the summary result after processing
    path('result/', views.summary_result_view, name='summary_result'),

    # Page showing the user's saved summary history (paginated)
    path('history/', views.history_view, name='history'),
]