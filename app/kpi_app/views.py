from .utils import evaluate_and_store_result
from .models import KPI, KPIAssetLink, EvaluationResult
from .serializers import KPISerializer, KPIAssetLinkSerializer, EvaluationResultSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView


# List KPIs
class KPIListView(generics.ListAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer


# Create KPI
class KPICreateView(generics.CreateAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer


# Link an Asset to a KPI
class KPIAssetLinkCreateView(APIView):
    def post(self, request):
        serializer = KPIAssetLinkSerializer(data=request.data)

        if serializer.is_valid():
            kpi_id = serializer.validated_data['kpi'].id
            asset_id = serializer.validated_data['asset_id']

            # Check if the KPI with the given ID exists
            try:
                KPI.objects.get(id=kpi_id)
            except KPI.DoesNotExist:
                return Response(
                    {"error": "KPI not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if this asset is already linked to any KPI
            if KPIAssetLink.objects.filter(asset_id=asset_id).exists():
                return Response(
                    {"error": "This asset is already linked to another KPI."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the link if validations pass
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EvaluateLinkedAssetsView(APIView):
    def post(self, request):
        # Retrieve the asset ID from the message data
        message = request.data.get("message", {})
        asset_id = message.get("asset_id")

        if not asset_id:
            return Response({"error": "Asset ID is required in the message data."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the linked KPI based on the asset ID
        try:
            link = KPIAssetLink.objects.get(asset_id=asset_id)
            kpi = link.kpi
        except KPIAssetLink.DoesNotExist:
            return Response({"error": "No KPI linked to this asset."}, status=status.HTTP_404_NOT_FOUND)

        # Evaluate and store the result for this asset and linked KPI
        evaluate_and_store_result(message, kpi.expression)

        return Response({"status": "Evaluation completed"}, status=status.HTTP_200_OK)


class EvaluationResultListView(generics.ListAPIView):
    queryset = EvaluationResult.objects.all()
    serializer_class = EvaluationResultSerializer
