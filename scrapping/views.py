from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from scrapping.youtube.scrapper import scrape_video_data

# Create your views here.

# Home view
def home(request):
    """
    Renders the home page.
    """
    print("Hello Rachit here")
    return render(request, 'index.html')

# Search view
def search(request):
    """
    Renders the search page.
    """
    print("Searching")
    return render(request, 'index1.html')

# Details view
@csrf_protect
def details(request):
    """
    Handles the details view, including form submission.
    """
    if request.method == 'POST':
        try:
            link = request.POST.get('query', '')  # Use POST to get the query from a form
            
            # Initialize the scraper and fetch video data
            scraper = scrape_video_data(link)
            result = scraper.scrape_video_data()
            
            return render(request, 'result.html', {'result': result})
        
        except Exception as e:
            return render(request, 'error.html', {'error_message': e})
        
    else:
        return render(request, 'error.html', {'error_message': "Did not get a POST request"})
