def is_ajax(request):
    """
    Verifica si la solicitud es de tipo AJAX.

    Esta función es una alternativa a request.is_ajax() que ha sido 
    desaprobada en Django versiones superiores a la 3.1.

    Args:
        request (HttpRequest): El objeto de solicitud para comprobar.

    Returns:
        bool: True si la solicitud es AJAX, False de lo contrario.
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'