# -*- coding: utf-8 -*

from django.db import models


class MPayWay(models.Model):
    title = models.CharField(max_length=36)
    img = models.CharField(max_length=36)
    desc = models.CharField(max_length=36)
    disable = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return dict(
            id=self.id,
            img=self.img,
            desc=self.desc,
            title=self.title,
            disable=self.disable,
            create_at=self.create_at,
            update_at=self.update_at,

        )
