from django.db import models


class Meat(models.Model):
    """
    肉类（任务）
    """
    # 天鹅肉
    content = models.TextField(
        default=None,
        null=True,
    )
    # 天鹅肉所有者
    toad = models.ForeignKey(
        'User.User',
        related_name='toad_user',
        on_delete=models.CASCADE,
    )
    # 目标时间
    target_time = models.DateTimeField(
        null=True
    )
    # 创建时间
    create_time = models.DateTimeField(
        auto_now_add=True

    )
    # 肉质及状态
    # 0还没熟
    # 1熟了（已到时间）
    # 2吃上了
    # 3下次一定
    status = models.IntegerField(
        default=0
    )
    # 短信提醒开关
    notification = models.BooleanField(
        # 是否开启短信提醒功能
        default=False
    )
    # 标记
    achieve = models.BooleanField(
        default=False
    )
# Create your models here.
