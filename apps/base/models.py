# import uuid
# from django.contrib.auth import get_user_model

# from django.db import models

# # Create your models here.

# class BaseModel(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#     created_at = models.DateTimeField(verbose_name=_("Created Date"), auto_now_add=True)
#     update_at = models.DateTimeField(verbose_name=_("Last Updated Date"), auto_now=True)
    # created_by = models.ForeignKey(
    #     get_user_model(),
    #     related_name="%(app_label)s_%(class)s_created_related",
    #     on_delete=models.SET_NULL,
    #     null=True,
    # )
    # updated_by = models.ForeignKey(
    #     get_user_model(),
    #     related_name="%(app_label)s_%(class)s_updated_related",
    #     on_delete=models.SET_NULL,
    #     null=True,
    # )
    # is_active = models.BooleanField(default=True)
    # is_deleted = models.BooleanField(default=False)
    # objects = BaseManager()
    # all_objects = BaseManager(alive_only=False)

    # class Meta:
    #     abstract = True

    # def delete(self, **kwargs):
    #     self.is_deleted = True
    #     self.save()

    # def hard_delete(self):
    #     super(BaseModel, self).delete()

    # def save(self, *args, **kwargs):
    #     super(BaseModel, self).save(*args, **kwargs)