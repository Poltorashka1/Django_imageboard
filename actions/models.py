from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

Custom_user = get_user_model()


# Create your models here.
class Action(models.Model):
    user = models.ForeignKey(Custom_user, on_delete=models.CASCADE, db_index=True, related_name='actions')
    verb = models.CharField(max_length=250)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj',
                                  on_delete=models.CASCADE)  # указывает на модель, с которой связана текущая (внешний ключ на модель ContentType)
    target_id = models.PositiveIntegerField(null=True, blank=True,
                                            db_index=True)  # поле для хранения ID связанного объекта
    target = GenericForeignKey('target_ct',
                               'target_id')  # поле для определения связи и управления ей (поле для обращения к связанному объекту на основании его типа и ID)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
