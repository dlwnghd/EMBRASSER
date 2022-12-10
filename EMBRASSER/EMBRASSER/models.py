from django.db import models

# 회원 테이블
class Members(models.Model):
    idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    p_code = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    addr = models.CharField(max_length=300, blank=True, null=True)
    religion = models.CharField(max_length=10, blank=True, null=True)
    scholar = models.CharField(max_length=15, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    job = models.CharField(max_length=20, blank=True, null=True)
    salary = models.BigIntegerField(blank=True, null=True)
    property = models.BigIntegerField(blank=True, null=True)
    debt = models.BigIntegerField(blank=True, null=True)
    re_marry = models.IntegerField(blank=True, null=True)
    drink = models.IntegerField(blank=True, null=True)
    smoke = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    family = models.CharField(max_length=100, blank=True, null=True)
    child = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    matching = models.IntegerField(blank=True, null=True, default=0)
    event = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'members'

# 관리자 테이블
class Admin(models.Model):
    a_idx = models.AutoField(primary_key=True)
    a_id = models.CharField(max_length=20, blank=True, null=True)
    a_pw = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin'