from .models import Notification

def send_notification(user, message):
    notification = Notification.objects.create(user=user, message=message)
    # Code to send notification to the user, e.g., sending an email, using a messaging service, etc.