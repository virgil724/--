from django.db import models

# Create your models here.
from django.contrib import admin


class ShowInfo(models.Model):
    show_uid = models.CharField(unique=True, max_length=100)
    version = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    discount_info = models.CharField(blank=True, max_length=100)
    description_filter_html = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    web_sales = models.URLField(blank=True)
    source_web_promote = models.URLField(blank=True)
    comment = models.CharField(blank=True, max_length=100)
    edit_modify_date = models.DateTimeField(blank=True, auto_now=True)
    hit_rate = models.IntegerField(auto_created=True,default=0)
    master_unit = models.ManyToManyField("Unit", through="MasterUnit")
    support_unit = models.ManyToManyField(
        "Unit",
        through="SupportUnit",
        through_fields=("show_uid", "unit"),
        related_name="support_show",
    )
    sub_unit = models.ManyToManyField(
        "Unit", through="SubUnit", related_name="sub_show"
    )
    other_unit = models.ManyToManyField(
        "Unit", through="OtherUnit", related_name="other_show"
    )
    source_web_name = models.ForeignKey(
        "SourceWebName", on_delete=models.SET_NULL, null=True
    )
    show_unit = models.ManyToManyField("Performer", through="ShowUnit")


class Location(models.Model):
    address = models.TextField()
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)


class ShowTime(models.Model):
    show_uid = models.ForeignKey(
        to="ShowInfo",
        to_field="show_uid",
        related_name="showTime",
        on_delete=models.CASCADE,
    )
    location_id = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
    )

    time = models.DateTimeField()
    end_time = models.DateTimeField()
    on_sales = models.BooleanField()
    price = models.CharField(blank=True, max_length=100)


class Unit(models.Model):
    name = models.CharField(max_length=30)


class Tag(models.Model):
    name = models.CharField(max_length=10)


class MasterUnit(models.Model):
    show_uid = models.ForeignKey(
        to="ShowInfo", to_field="show_uid", on_delete=models.CASCADE
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


class SupportUnit(models.Model):
    show_uid = models.ForeignKey(
        to="ShowInfo", to_field="show_uid", on_delete=models.CASCADE
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


class SubUnit(models.Model):
    show_uid = models.ForeignKey(
        to="ShowInfo", to_field="show_uid", on_delete=models.CASCADE
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)


class OtherUnit(models.Model):
    show_uid = models.ForeignKey(
        to="ShowInfo", to_field="show_uid", on_delete=models.CASCADE
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Country(models.Model):
    name = models.CharField(max_length=20)


class Performer(models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)


class ShowUnit(models.Model):
    show_uid = models.ForeignKey(
        to="ShowInfo", to_field="show_uid", on_delete=models.CASCADE
    )
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE)


class SourceWebName(models.Model):
    name = models.CharField(max_length=100)


@admin.register(Location)
class ShowTimeAdmin(admin.ModelAdmin):
    pass
