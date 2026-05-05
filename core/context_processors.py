from .models import CompanyProfile

def company_profile(request):
    """
    Makes the company profile available in all templates as 'company'.
    """
    return {
        'company': CompanyProfile.objects.first()
    }
