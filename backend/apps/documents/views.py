"""
MotherCare — Document Management & Nextcloud Integration Views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .nextcloud_service import upload_to_nextcloud


class NextcloudSyncView(APIView):
    """
    POST /api/v1/documents/export-to-nextcloud/
    Saves a clinical report or patient document directly into Nextcloud via WebDAV.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        title = request.data.get("title", "Clinical_Report")
        content = request.data.get("content", "")
        patient_name = request.data.get("patient_name", "General Patient")
        doctor_name = request.data.get("doctor_name", "Attending Clinician")
        
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        sanitized_title = title.replace(" ", "_")
        filename = f"{sanitized_title}_{timestamp}.txt"

        # Format full clinical report body
        formatted_report = (
            f"====================================================\n"
            f" MOTHERCARE MATERNITY HOSPITAL — CLINICAL DOCUMENT\n"
            f"====================================================\n"
            f"Document Title : {title}\n"
            f"Generated Date : {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"Patient Name   : {patient_name}\n"
            f"Doctor/Staff   : {doctor_name}\n"
            f"Sync Target    : Nextcloud Private Cloud (/Project-Team/Reports)\n"
            f"----------------------------------------------------\n"
            f"CLINICAL NOTES & DETAILS:\n"
            f"{content}\n"
            f"====================================================\n"
            f"Authenticated via MotherCare WebDAV Bridge Service\n"
        )

        result = upload_to_nextcloud(filename, formatted_report.encode("utf-8"))

        if result.get("success"):
            return Response(
                {
                    "message": "Document successfully synced to Nextcloud Private Cloud!",
                    "details": result,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "error": "Failed to sync document to Nextcloud.",
                    "details": result,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )
