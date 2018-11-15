# -*- coding: utf-8 -*-

"""
  ErrorCode定义
~~~~~~~~~~~~~~~~~~~~~

errorcode module定义了Errorcode

usage:

   平常情况下:
   from utils.common import errorcode
   from utils.common import APIException

   raise APIException(errorcode.SYSTEM_BUSY)

   前端/客户端参数校验不成功时:
   from utils.common import errorcode
   from utils.common import APIException

   if not form.is_valid():
      raise APIException(errorcode.INVALID_ARGS, msg=form.errors)

tips:

   定义errorcode时注意区分哪些msg是会显示给平台用户的,哪些是给接口调用者看的.
   因为在同一个errorcode命名空间下,有些ErrorCode的名字注意加前缀, 比如ID_NOT_EXIST要指明USER_ID_NOT_EXIST.
"""

import collections

# 定义ErrorCode类对象
ErrorCode = collections.namedtuple('ErrorCode', 'id msg')

# 全局返回码定义
SYSTEM_BUSY = ErrorCode(id=600, msg="系统繁忙,请稍后再试")
INVALID_ARGS = ErrorCode(id=601, msg="不合法的参数")  # 联调时常用,建议使用时,用form.errors替换掉默认msg.
INVALID_METHOD = ErrorCode(id=602, msg="不合法的http方法")  # 现阶段不合法的方法由django的require_http_methods自动控制,还用不上.
HTTPS_NEEDED = ErrorCode(id=603, msg="需要HTTPS请求")
INVALID_RES_TYPE = ErrorCode(id=604, msg="不合法的资源类型")
API_LOGIN_REQUIRED = ErrorCode(id=605, msg="登录后才能使用此功能")
OPERATION_NOT_AUTHORIZED = ErrorCode(id=606, msg="该用户没有权限执行此项操作")
LOGIN_TOKEN_INVALID = ErrorCode(id=608, msg="登录信息已过期, 请重新登录")
CALL_OUT_LIMIT = ErrorCode(id=609, msg="您当前操作太过频繁, 请休息下再操作")
GLOBAL_BLACK_USER = ErrorCode(id=611, msg="您已被禁用, 请联系我们")
RESOURCE_UPLOAD_FAIlED = ErrorCode(id=613, msg="资源上传失败")
RESOURCE_KEY_INVALID = ErrorCode(id=614, msg="资源的key不合法")
INNER_ADMINS_ONLY = ErrorCode(id=615, msg="内部资源, 拒绝访问")
IP_LIMITED = ErrorCode(id=618, msg="非法网络请求, 请联系我们")
ATTACK_ACTION = ErrorCode(id=619, msg="出错了")  # 恶意访问
DUPLICATE_POST = ErrorCode(id=620, msg="请不要重复发布")

# 控制台用户管理
CONSOLE_LOGIN_REQUIRED = ErrorCode(id=700, msg="访问此接口需要登录, 请跳转到登录页面让用户登录")
CONSOLE_NEED_CHANGE_DEFAULT_PWD = ErrorCode(id=701, msg="请修改初始密码后再使用")
CONSOLE_NEED_CHANGE_PWD = ErrorCode(id=702, msg="请修改密码后再使用")
CONSOLE_PWD_SHORTER = ErrorCode(id=703, msg="密码最少是8位")
CONSOLE_PWD_NO_LOWER = ErrorCode(id=704, msg="密码必需包含小写字母")
CONSOLE_PWD_NO_UPPER = ErrorCode(id=705, msg="密码必需包含大写字母")
CONSOLE_PWD_NO_SPECIAL = ErrorCode(id=706, msg="密码必需包含特殊字符")
CONSOLE_PWD_NO_NUMBER = ErrorCode(id=707, msg="密码必需包含数字")

# 用户模块返回码定义
USER_NICKNAME_INVALID = ErrorCode(id=1003, msg='昵称由4-9个中英文、数字组成')
USER_WRONG_PASSWORD = ErrorCode(id=1004, msg='用户名或密码错误')
USER_DISABLE = ErrorCode(id=1005, msg='您已被禁用')
USER_DIFF_PWD_AGAIN = ErrorCode(id=1006, msg='两次密码不一致')
USER_NICKNAME_DUPLICATION = ErrorCode(id=1007, msg='该昵称已被占用')
USER_NICKNAME_DIRTY_WORD = ErrorCode(id=1008, msg='用户名只能使用数字字母汉字')
USER_PASSWORD_INVALID_WORD = ErrorCode(id=1009, msg='密码含有非法字符')
USER_DONT_EXISTS = ErrorCode(id=1010, msg='用户不存在')
