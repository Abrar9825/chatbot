import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from .models import Product

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def home(request):
    return render(request, 'chatbot_app/index.html')

def get_gemini_response(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        source = request.POST.get('source')  # Get source selection

        product_data = []

        # If user selects "Database", fetch from database
        if source == "database":
            try:
                products = Product.objects.filter(name__icontains=product_name)
                if products.exists():
                    for product in products:
                        product_data.append({
                            "name": product.name,
                            "price": str(product.price),
                            "details": product.details
                        })
                else:
                    product_data = None
            except Exception as e:
                return JsonResponse({'error': f"Database Error: {str(e)}"})

        # If user selects "World Data", fetch from Gemini
        if not product_data and source == "world":
            try:
                model = genai.GenerativeModel('gemini-1.5-pro-latest')
                response = model.generate_content(f"Give me world knowledge about: {product_name}")
                reply = response.text.strip() if hasattr(response, 'text') else "No valid response from Gemini."
                return JsonResponse({'not_found': True, 'reply': reply})
            except Exception as e:
                return JsonResponse({'error': f"Error: {str(e)}"})

        if not product_data:
            return JsonResponse({'not_found': True, 'reply': 'No product found.'})

        return JsonResponse({'not_found': False, 'products': product_data})

    return JsonResponse({'error': "Invalid request."})