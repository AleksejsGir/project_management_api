from django.http import JsonResponse

def api_root(request):
    """
    Главная страница API с информацией о доступных endpoints
    """
    return JsonResponse({
        'message': 'Добро пожаловать в Project Management API! 🚀',
        'version': '1.0.0',
        'endpoints': {
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'admin': '/admin/',
            'projects': '/api/projects/',
            'auth': '/auth/',
        },
        'status': 'API работает корректно! ✅'
    })