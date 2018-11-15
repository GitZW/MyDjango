# -*- coding: utf-8 -*

from django.views.decorators.http import require_GET, require_POST

from core_user.service import feedbackservice, userservice
from utils.common.decorators import validate_form, require_login
from .feedbacksform import *
from django.utils.decorators import method_decorator
from django.views.generic import View
from core_operator.service import operatorservice


class FeedbackView(View):
    @method_decorator(validate_form(GetFeedbacksForm))
    def get(self, request, cleaned_data):
        total, feedbacks = feedbackservice.get_feedback_list(**cleaned_data)
        return dict(total=total, history=wrap_feedback(feedbacks))


class FeedbackHistoryView(View):
    @method_decorator(validate_form(GetFeedbackHistoryForm))
    def get(self, request, user_id, cleaned_data):
        user_id = int(user_id)
        feedbacks = feedbackservice.get_feedback_history(user_id, **cleaned_data)
        return dict(history=wrap_feedback(feedbacks))


@require_POST
@validate_form(PostFeedbacksForm)
def reply_user(request, user_id, cleaned_data):
    operator_id = request.user.id
    user_id = int(user_id)
    id = feedbackservice.add_feedback(user_id, **cleaned_data, is_reply=True, operator_id=operator_id)
    return dict(id=id)


def wrap_feedback(feedbacks):
    result = []
    for feedback in feedbacks:
        feedback['user'] = userservice.get_user_info(user_id=feedback['user_id'])
        feedback['operator'] = operatorservice.get_operator_id_and_name_dict(feedback['operator_id'])
        feedback['from_user'] = not feedback['operator_id']

        result.append(feedback)
    return result
