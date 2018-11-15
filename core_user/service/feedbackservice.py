# -*- coding: utf-8 -*
import logging

from django.db import transaction

from ..models import *

logger = logging.getLogger(__name__)


def get_feedback_history(user_id, load_before=None, load_after=None, is_read=False, limit=10, offset=0, ):
    mfeedbacks = MFeedbackHistory.objects.filter(user_id=user_id)
    if load_before:
        mfeedbacks = mfeedbacks.filter(id__lt=load_before).order_by('-id')
    elif load_after:
        mfeedbacks = mfeedbacks.filter(id__gt=load_after).order_by('id')
    else:
        mfeedbacks = mfeedbacks.order_by('-id')

    feedbacks = list(mfeedbacks[:limit])
    feedbacks = sorted(feedbacks, key=lambda x: x.id)

    if is_read:
        update_user_feedback_read_status(user_id)
    return [mfeedback.to_dict() for mfeedback in feedbacks]


def add_feedback(user_id, content, is_reply=False, operator_id=None):
    assert user_id
    assert content
    if is_reply:
        assert operator_id

    with transaction.atomic():
        defaults = dict(content=content, operator_id=operator_id, is_replied=is_reply)

        mfeedback, created = MFeedback.objects.update_or_create(user_id=user_id,
                                                                defaults=defaults)

        m = MFeedbackHistory(user_id=user_id, content=content, operator_id=operator_id)
        m.save()
    return m.id


def update_user_feedback_read_status(user_id):
    mfeedback = MFeedback.objects.filter(user_id=user_id)
    if not mfeedback:
        return
    mfeedback = mfeedback.first()
    mfeedback.is_read = True
    mfeedback.save(update_fields=['is_read'])


def get_feedback_list(user_id=None, is_replied=None, operator_id=None, limit=20, offset=0):
    mfeedbacks = MFeedback.objects.all().order_by('-update_at')
    total = mfeedbacks.count()
    if user_id:
        mfeedbacks = mfeedbacks.filter(user_id=user_id)
    if is_replied is not None:
        mfeedbacks = mfeedbacks.filter(is_replied=is_replied)
    if operator_id:
        mfeedbacks = mfeedbacks.filter(operator_id=operator_id)

    return total, [mfeedback.to_dict() for mfeedback in mfeedbacks[offset:offset + limit]]
