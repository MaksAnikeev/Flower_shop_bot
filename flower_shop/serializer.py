from rest_framework import serializers
from flower_shop.models import CategoryPrice


class CategoryPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryPrice
        fields = '__all__'
