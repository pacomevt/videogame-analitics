from django import forms
from scraper.tasks import get_data

class ScraperForm(forms.Form):
    def run_scraper(self):
        get_data.delay()
        return True