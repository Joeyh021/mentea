from people.models import Notification, User


class NotificationManager:
    def send(title, message, to: "list[User]", link=None):
        for user in to:
            notif = Notification(
                user=user,
                title=title,
                content=message,
                link=link,
            )
            notif.save()

    def send(title, message, to: User, link=None):

        notif = Notification(
            user=to,
            title=title,
            content=message,
            link=link,
        )
        notif.save()
