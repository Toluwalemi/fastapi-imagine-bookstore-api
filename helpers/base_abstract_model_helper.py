from tortoise import fields, manager, models, timezone
from tortoise.queryset import QuerySet

from auth.models import User


class BaseQuerySet(QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())


class BaseManager(manager.Manager):
    def get_queryset(self):
        return BaseQuerySet(self._model).filter(deleted_at=None)


class BaseAbstractModel(models.Model):
    """Base Abstract Model"""

    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True, default=None)
    RECORD_STATE = [("ACTIVE", "ACTIVE"), ("DELETED", "DELETED")]
    state = fields.CharField(max_length=20, choices=RECORD_STATE, default="ACTIVE")
    created_by = fields.ForeignKeyField(
        User,
        on_delete=fields.CASCADE,
        description="created by",
        related_name="+",
        null=True,
    )
    all_objects = manager.Manager()

    class Meta:
        abstract = True
        manager = BaseManager()
        ordering = ["-created_at"]

    def delete(self, soft_delete: bool = True):
        if soft_delete:
            self.deleted_at = timezone.now()
            self.state = self.RECORD_STATE[1][0]
            return self.save()

    def hard_delete(self):
        return super().delete()

    def save(self, actor=None, *args, **kwargs):
        if not self.pk:
            self.created_by = actor
        super().save(*args, **kwargs)
