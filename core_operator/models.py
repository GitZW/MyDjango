# -*- coding: utf-8 -*

from django.db import models


class MOperator(models.Model):
    username = models.CharField(unique=True, max_length=16)
    password = models.CharField(max_length=36)
    disable = models.BooleanField(default=False)

    role = models.CharField(max_length=16, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.username,
            disable=self.disable,
            role=self.role,
            create_at=self.create_at,
            update_at=self.update_at,
        )
