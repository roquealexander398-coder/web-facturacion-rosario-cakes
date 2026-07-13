from apps.company.models import CompanyConfig


def company_config(request):
    return {'company_config': CompanyConfig.get_config()}
