from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, ContentType, DELETION
from django.utils.translation import gettext as _

OPERATION_MESSAGE_MAP = {
    ADDITION: _('Created'),
    CHANGE: _('Updated'),
    DELETION: _('Deleted'),
}


class LoggingMethodMixin:
    """
    Adds methods that log changes made to users' data.
    To use this, subclass it and ModelViewSet.
    """

    def log(self, operation, instance):
        action_message = OPERATION_MESSAGE_MAP[operation]

        # noinspection PyUnresolvedReferences
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=operation,
            change_message=f'{action_message} {instance}')

    def _log_on_create(self, serializer):
        """Log the up-to-date serializer.data."""
        self.log(operation=ADDITION, instance=serializer.instance)

    def _log_on_update(self, serializer):
        """Log data from the updated serializer instance."""
        self.log(operation=CHANGE, instance=serializer.instance)

    def _log_on_destroy(self, instance):
        """Log data from the instance before it gets deleted."""
        self.log(operation=DELETION, instance=instance)


class LoggingViewSetMixin(LoggingMethodMixin):
    """
    A ViewSet that logs changes made to users' data.
    To use this, subclass it and ModelViewSet.
    corresponding _log_on_X method:
    - perform_create
    - perform_update
    - perform_destroy
    """

    def perform_create(self, serializer):
        """Create an object and log its data."""
        # noinspection PyUnresolvedReferences
        super().perform_create(serializer)
        self._log_on_create(serializer)

    def perform_update(self, serializer):
        """Update the instance and log the updated data."""
        # noinspection PyUnresolvedReferences
        super().perform_update(serializer)
        self._log_on_update(serializer)

    def perform_destroy(self, instance):
        """Delete the instance and log the deletion."""
        self._log_on_destroy(instance)
        # noinspection PyUnresolvedReferences
        super().perform_destroy(instance)
