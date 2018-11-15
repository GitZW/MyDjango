# -*- coding: utf-8 -*

from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST

from core_user.service import userservice
from utils.common.decorators import validate_form, require_login
from .userform import UserListForm
from django.utils.decorators import method_decorator


class UserList(View):
    @method_decorator(validate_form(UserListForm))
    def get(self, request, cleaned_data):
        total, users = userservice.get_user_list(**cleaned_data)
        return dict(total=total, users=users)


class UserDetail(View):
    def get(self, request, user_id):
        user_id = int(user_id)
        user = userservice.get_user_info(user_id=user_id)
        user['total_recharge'] = 0
        return user

    def put(self, request, user_id, cleaned_data):
        """修改用户"""
        pass
