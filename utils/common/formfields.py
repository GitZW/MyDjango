# -*- coding: utf-8 -*-
import re
from datetime import datetime

from django import forms
from django.utils import six
from django.forms import MultipleHiddenInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class ArrayField(forms.Field):
    """自定义的arrayField, 借鉴至http://slacy.com/blog/2012/04/array-valued-form-fields-in-django/"""

    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        self.base_type = kwargs.pop('base_type')
        self.widget = MultipleHiddenInput
        self.min_length = min_length
        self.max_length = max_length
        super(ArrayField, self).__init__(*args, **kwargs)

    def validate(self, value):
        # super(ArrayField, self).validate(value)  # 为了兼容,先不加required的校验.
        if self.min_length:
            if not value or len(value) < self.min_length:
                raise ValidationError("这个字段至少传%s个值" % self.min_length)
        if self.max_length:
            if value and len(value) > self.max_length:
                raise ValidationError("这个至多传%s个值" % self.max_length)

    def clean(self, value):
        value = [self.base_type.clean(subvalue) for subvalue in value[0].split(',')] if value else []
        return super(ArrayField, self).clean(value)


class EnumField(forms.Field):
    default_error_messages = {
        'invalid_enum': _('%(value)s 不是合法值, 有效值列表: %(enum_type)s.'),
    }

    def __init__(self, *args, **kwargs):
        self.base_type = kwargs.pop('base_type')
        super(EnumField, self).__init__(*args, **kwargs)

    def validate(self, value):
        super(EnumField, self).validate(value)
        if value is None or value == '':
            return
        enum_values = [str(value.value) for name, value in self.base_type.__members__.items()]
        if str.lower(value) not in enum_values:
            raise ValidationError(
                self.error_messages['invalid_enum'],
                code='invalid_enum',
                params={'value': value, "enum_type": enum_values},
            )

    def clean(self, value):
        self.validate(value)

        if value is None or value == '':
            return None
        try:
            value = int(value)
        except ValueError:
            value = str.lower(value)
        return self.base_type(value)


class BooleanField(forms.Field):
    def to_python(self, value):
        if value is None or value == '':
            return None
        if isinstance(value, six.string_types) and value.lower() in ('false', '0'):
            value = False
        else:
            value = bool(value)
        return super(BooleanField, self).to_python(value)

    def validate(self, value):
        if value is None and self.required:
            raise ValidationError(self.error_messages['required'], code='required')

    def has_changed(self, initial, data):
        # Sometimes data or initial could be None or '' which should be the
        # same thing as False.
        if initial == 'False':
            # show_hidden_initial may have transformed False to 'False'
            initial = False
        return bool(initial) != bool(data)


class NoneCharField(forms.CharField):
    """与django自带的forms.CharField的区别, 如果不传参数, 则值为None"""

    def to_python(self, value):
        if value is None:
            return None
        else:
            return super(NoneCharField, self).to_python(value)


class OptionField(NoneCharField):
    """本质上是NoneCharField, 接受可选值的列表, 校验值必须为可选值"""
    default_error_messages = {
        'invalid_value': _('%(value)s 不是合法值, 有效值列表: %(option_values)s.'),
    }

    def __init__(self, *args, **kwargs):
        self.option_values = kwargs.pop('option_values')
        assert isinstance(self.option_values, list)
        super(OptionField, self).__init__(*args, **kwargs)

    def validate(self, value):
        super(OptionField, self).validate(value)
        if value is not None and value not in self.option_values:
            raise ValidationError(
                self.error_messages['invalid_value'],
                code='invalid_value',
                params={'value': value, "option_values": self.option_values},
            )


class DateTimeField(forms.DateTimeField):
    """
    扩展datetime field, 支持timestamp(int/float)
    10位: 单位为s
    13位: 单位为ms
    """

    def to_python(self, value):
        if value is None:
            return None
        try:
            value = float(value)
            int_value = int(value)
            length = len(str(int_value))
            if length <= 11:  # 秒
                return datetime.fromtimestamp(value)
            else:
                return datetime.fromtimestamp(value / 1000)
        except ValueError:
            return super(DateTimeField, self).to_python(value)


pic_pattern = re.compile(r'^\w{8}-(\w{4}-){3}\w{12}$')


def check_media_format_valid(media):
    """
    校验图片或视频key基本格式是否合法,符合uuid基本格式
    """
    result = False if pic_pattern.match(media) is None else True
    return result
