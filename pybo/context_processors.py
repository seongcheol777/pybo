from .models import Category, Notification, Banner


def categories_nav(request):
    ctx = {"categories": Category.objects.all().order_by('order', 'name')}
    if request.user.is_authenticated:
        ctx['unread_notification_count'] = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
    else:
        ctx['unread_notification_count'] = 0

    banner_dict = {b.slot: b for b in Banner.objects.filter(is_active=True)}
    ctx['banners'] = [banner_dict.get(i) for i in range(1, 21)]
    return ctx
