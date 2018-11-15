# -*- coding: utf-8 -*

from django.views.decorators.http import require_GET, require_POST

from core_user.service import feedbackservice
from utils.common.decorators import validate_form, require_login
from .feedbacksform import *
from django.utils.decorators import method_decorator
from django.views.generic import View
from core_operator.service.operatorservice import get_operator_id_and_name_dict


class FeedbackView(View):
    @method_decorator(require_login)
    @method_decorator(validate_form(GetFeedbacksForm))
    def get(self, request, cleaned_data):
        user_id = request.user_id
        feedbacks = feedbackservice.get_feedback_history(user_id, **cleaned_data, is_read=True)
        return dict(history=wrap_feedback(feedbacks))

    @method_decorator(require_login)
    @method_decorator(validate_form(PostFeedbacksForm))
    def post(self, request, cleaned_data):
        user_id = request.user_id
        feedback_id = feedbackservice.add_feedback(user_id, **cleaned_data)
        return dict(id=feedback_id)


def wrap_feedback(feedbacks):
    result = []
    for feedback in feedbacks:
        feedback['from_user'] = not feedback['operator_id']
        feedback['operator'] = get_operator_id_and_name_dict(feedback['operator_id'], with_name=False)
        result.append(feedback)
    return result
