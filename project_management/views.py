from django.http import JsonResponse

def api_root(request):
    """
    API root endpoint with information about available endpoints
    """
    return JsonResponse({
        'message': 'Welcome to Project Management API! 🚀',
        'version': '1.0.0',
        'endpoints': {
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'admin': '/admin/',
            'projects': '/api/projects/',
            'auth': '/auth/',
        },
        'status': 'API is working correctly! ✅'
    })