# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from core_user.service import userservice


class Command(BaseCommand):
    help = "check user member status"

    def handle(self, *args, **options):
        userservice.check_user_member_status()
