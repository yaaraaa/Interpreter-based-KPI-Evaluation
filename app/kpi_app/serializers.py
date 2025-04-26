from rest_framework import serializers
from .models import KPI, KPIAssetLink, EvaluationResult


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ['id', 'name', 'expression', 'description']


class KPIAssetLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIAssetLink
        fields = ['id', 'kpi', 'asset_id']


class EvaluationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationResult
        fields = ['id', 'asset_id', 'attribute_id', 'timestamp', 'value']
