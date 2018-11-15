# -*- coding: utf-8 -*
import enum
from ..models import MPayWay


class PayType(enum.Enum):
    WX = 'wx'  # 微信
    AL = 'al'  # 支付宝


def get_pay_ways():
    return [m.to_dict() for m in MPayWay.objects.filter(disable=False)]


def add_pay_way(img, title, desc):
    mpayway = MPayWay(img=img, title=title, desc=desc)
    mpayway.save()
    return mpayway.id


def update_pay_way(way_id, img, title, desc):
    mpayway = MPayWay.objects.get(id=way_id)
    if img:
        mpayway.img = img
    if title:
        mpayway.title = title
    if desc:
        mpayway.desc = desc

    mpayway.save()


def delete_pay_way(way_id):
    MPayWay.objects.filter(id=way_id).update(disable=True)


def get_pay_way_by_id(way_id):
    mpayway = MPayWay.objects.get(id=way_id)
    return mpayway.to_dict()
