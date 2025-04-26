from django.contrib import admin
from .models import KPI, KPIAssetLink, EvaluationResult

admin.site.register(KPI)
admin.site.register(KPIAssetLink)
admin.site.register(EvaluationResult)
