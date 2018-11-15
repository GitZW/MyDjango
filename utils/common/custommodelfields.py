from django.db import models


# Create your models here.


class ListField(models.CharField):
    description = """自定义 list 字段,在CharField基础上扩展"""

    def __init__(self, base_type=str, separator="|", *args, **kwargs):
        """
        :param base_type: list 里的数据类型
        :param separator: 存入数据库的分隔符
        :param args:
        :param kwargs:
        """
        self.separator = separator
        self.base_type = base_type
        super(ListField, self).__init__(*args, **kwargs)

    def get_db_prep_save(self, value, connection):
        """
        自定义字段在保存时需要进行特殊转换
        :param value:
        :param connection:
        :return:
        """
        if not value:
            return None
        assert isinstance(value, list)
        for v in value:
            assert isinstance(v, self.base_type)
        return self.separator.join(str(v) for v in value)

    def to_python(self, value):
        if not value:
            return None

        return [self.base_type(v) for v in value.split(self.separator)]

    def get_prep_value(self, value):
        """
        Python对象转换回查询值
        :param value:
        :return:
        """
        return self.separator.join(str(v) for v in value) if value else None

    def from_db_value(self, value, expression, connection, context):
        """
        在从数据库加载数据（包括在聚合和values()调用）的所有情况下将调用from_db_value()
        :param value:
        :param expression:
        :param connection:
        :param context:
        :return:
        """
        return self.to_python(value)
