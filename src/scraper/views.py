from django.shortcuts import render, get_object_or_404
from .forms import ScraperForm
from django.views import View
# Create your views here.

def index(request):
    return render(request, 'scraper/index.html')


class ScraperView(View):
    def get(self, request):
        form = ScraperForm()
        return render(request, 'scraper/runscraper.html', {'form': form})

    def post(self, request):
        form = ScraperForm(request.POST)
        if form.is_valid():
            form.run_scraper()
            return render(request, 'scraper/runscraper.html', {'form': form, 'success': True})
        else:
            return render(request, 'scraper/runscraper.html', {'form': form, 'success': False})