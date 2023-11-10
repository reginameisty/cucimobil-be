from .models import Notification
from .serializers import UserSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

def send_notification(user, message):
    notification = Notification.objects.create(user=user, message=message)
    # Code to send notification to the user, e.g., sending an email, using a messaging service, etc.