from django.db import models


class KPI(models.Model):
    name = models.CharField(max_length=255, unique=True)
    expression = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class KPIAssetLink(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name="asset_links")
    asset_id = models.CharField(max_length=255)

    class Meta:
        unique_together = ('kpi', 'asset_id')

    def __str__(self):
        return f"{self.kpi.name} - {self.asset_id}"


class EvaluationResult(models.Model):
    asset_id = models.CharField(max_length=255)
    attribute_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    value = models.TextField()

    def __str__(self):
        return f"Result for Asset {self.asset_id}"
