from django.db import models

# Create your models here.

'''
地区模型创建
'''


class Area(models.Model):
    name = models.CharField(max_length=20, verbose_name='名称')
    # related_name 之后做介绍
    '''
    null: 代表当前数据库允许为空
    blank：网页中的表单可以为空
    '''
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subs',
        null=True,
        blank=True,
        verbose_name='上级行政区划'
    )

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name