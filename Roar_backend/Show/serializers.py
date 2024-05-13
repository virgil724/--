from rest_framework import serializers

from .models import ShowInfo, ShowTime, Performer, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["id"]


class ShowTimeSerializer(serializers.ModelSerializer):
    location_id = LocationSerializer()

    class Meta:
        model = ShowTime
        exclude = ["id", "show_uid"]


class ShowUnitSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Performer

        fields = ["name", "country"]


class ShowSerializer(serializers.ModelSerializer):
    master_unit = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    sub_unit = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    support_unit = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    other_unit = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    source_web_name = serializers.SlugRelatedField(read_only=True, slug_field="name")
    showTime = ShowTimeSerializer(many=True, read_only=True)
    show_unit = ShowUnitSerializer(many=True, read_only=True)

    class Meta:
        model = ShowInfo
        exclude = ["id", "category", "version"]


class ShowGeneralSerializer(serializers.ModelSerializer):
    source_web_name = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = ShowInfo
        fields = [
            "id",
            "show_uid",
            "title",
            "web_sales",
            "source_web_promote",
            "image_url",
            "source_web_name",
            "discount_info",
            "description_filter_html",
            'comment',
            "hit_rate",
        ]
