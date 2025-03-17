from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Add this for the homepage
    path('get-gemini-response/', get_gemini_response, name='get_gemini_response'),
    # path('list-models/', list_models, name='list_models'),

]
# Compare this snippet from chatbot_app/urls.py: