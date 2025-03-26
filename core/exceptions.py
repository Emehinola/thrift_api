from rest_framework import response, status
from rest_framework.exceptions import APIException


class UnauthorizedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized access'
    default_code = 'unathorized'

class AdminAccessOnly(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Only admins can perform this action'
    default_code = 'unathorized'

def exception_handler(exception, context):
    try:
        return response.Response({
            'status_code': exception.status_code,
            'message': exception.default_detail,
            'error': exception.default_detail
        }, status=exception.status_code)
    
    except Exception as e:
        print('exc: ', exception)
        return response.Response({
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Something went wrong',
            'error': 'Server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
