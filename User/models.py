import re
import string
from SmartDjango import models, E
from django.utils.crypto import get_random_string


@E.register()
class UserError:
    PASSWORD_CHANGED = E("密码已改变，需要重新获取token")
    INVALID_PASSWORD = E("密码只能包含字母数字以及“!@#$%^&*()_+-=,.?;:”")
    INVALID_USERNAME_FIRST = E("用户名首字符只能是字母")
    INVALID_USERNAME = E("用户名只能包含字母数字和下划线")
    USERNAME_EXIST = E("已存在的用户名")
    NOT_FOUND_CODE = E("不存在的邀请码")
    CREATE_USER = E("存储用户错误")
    PASSWORD = E("错误的用户名或密码")
    NOT_FOUND_USER = E("不存在的用户")


class User(models.Model):
    """
    用户类
    根超级用户id=1
    """
    ROOT_ID = 1

    username = models.CharField(
        max_length=32,
        min_length=3,
        unique=True,
        blank=True,
        null=True,
        default=None,
    )
    password = models.CharField(
        max_length=32,
        min_length=6,
    )
    salt = models.CharField(
        max_length=10,
        default=None,
    )
    pwd_change_time = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    nickname = models.CharField(
        max_length=10,
        default=None,
    )
    phone = models.CharField(
        default=None,
        unique=True,
        max_length=20,
    )
    meat_quantity = models.IntegerField(
        # 已发布任务数目
        default=0,
    )

    def is_ancestor(self, user: 'User'):
        while user:
            if self == user:
                return True
            user = user.inviter
        return False

    @staticmethod
    def _valid_username(username):
        """验证用户名合法"""
        if username[0] not in string.ascii_lowercase + string.ascii_uppercase:
            raise UserError.INVALID_USERNAME_FIRST
        valid_chars = '^[A-Za-z0-9_]{3,32}$'
        if re.match(valid_chars, username) is None:
            raise UserError.INVALID_USERNAME

    @staticmethod
    def _valid_password(password):
        """验证密码合法"""
        valid_chars = '^[A-Za-z0-9!@#$%^&*()_+-=,.?;:]{6,16}$'
        if re.match(valid_chars, password) is None:
            raise UserError.INVALID_PASSWORD

    @staticmethod
    def hash_password(raw_password, salt=None):
        if not salt:
            salt = get_random_string(length=6)
        hash_password = User._hash(raw_password + salt)
        return salt, hash_password

    @classmethod
    def exist_with_username(cls, username):
        try:
            cls.objects.get(username=username)
        except cls.DoesNotExist:
            return
        raise UserError.USERNAME_EXIST

    @classmethod
    def inviterjsonArr(cls, data):
        rData = []
        for item in data:
            item.__dict__.pop("_state")
            rData.append(item.__dict__)
        return rData

    @classmethod
    def create(cls, username, password):
        """ 创建用户

        :param username: 用户名
        :param password: 密码
        :return: Ret对象，错误返回错误代码，成功返回用户对象
        """
        cls.validator(locals())

        salt, hashed_password = User.hash_password(password)

        User.exist_with_username(username)
        try:
            user = cls(
                username=username,
                password=hashed_password,
                salt=salt,
            )
            user.save()
        except Exception:
            raise UserError.CREATE_USER
        return user

    def change_password(self, password, old_password):
        """修改密码"""
        self.validator(locals())

        if self.password != User._hash(old_password):
            raise UserError.PASSWORD
        self.salt, self.password = User.hash_password(password)
        import datetime
        self.pwd_change_time = datetime.datetime.now().timestamp()
        self.save()

    @staticmethod
    def _hash(s):
        import hashlib
        md5_ = hashlib.md5()
        md5_.update(s.encode())
        return md5_.hexdigest()

    @staticmethod
    def get_user_by_username(username):
        """根据用户名获取用户对象"""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise UserError.NOT_FOUND_USER
        return user

    @staticmethod
    def get_user_by_id(user_id):
        """根据用户ID获取用户对象"""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise UserError.NOT_FOUND_USER
        return user

    @classmethod
    def authenticate(cls, username, password):
        """验证用户名和密码是否匹配"""
        cls.validator(locals())

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as err:
            raise UserError.NOT_FOUND_USER

        salt, hashed_password = User.hash_password(password, user.salt)
        if hashed_password == user.password:
            return user
        raise UserError.PASSWORD

    def change_talked(self):
        print(bool(1 - self.talked))
        self.talked = bool(1 - self.talked)
        self.save()

    def d(self):
        return self.dictor('pk->uid', 'username')

    def d_base(self):
        return self.dictor('pk->id', 'username')


class UserP:
    username, password = User.get_params('username', 'password')
