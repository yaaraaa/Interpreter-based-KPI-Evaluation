from django.urls import path
from .views import (
    KPIListView,
    KPICreateView,
    KPIAssetLinkCreateView,
    EvaluateLinkedAssetsView,
    EvaluationResultListView,
)


urlpatterns = [
    path('list/', KPIListView.as_view(), name='kpi-list'),
    path('create/', KPICreateView.as_view(), name='kpi-create'),
    path('link-asset/', KPIAssetLinkCreateView.as_view(), name='kpi-asset-link-create'),
    path('evaluate/', EvaluateLinkedAssetsView.as_view(), name='evaluate-linked-assets'),
    path('evaluations/', EvaluationResultListView.as_view(), name='evaluation-list'),

]
