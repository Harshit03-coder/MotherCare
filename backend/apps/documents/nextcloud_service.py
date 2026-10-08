"""
MotherCare — Nextcloud WebDAV Integration Service
Uploads clinical documents, lab reports, and patient summaries
directly from MotherCare into Nextcloud Cloud Storage.
"""
import logging
import os
import urllib.request
import urllib.error
import base64
from decouple import config

logger = logging.getLogger(__name__)

NEXTCLOUD_BASE_URL = config("NEXTCLOUD_URL", default="http://192.168.26.112:8080").rstrip("/")
NEXTCLOUD_USER = config("NEXTCLOUD_USER", default="student1")
NEXTCLOUD_PASSWORD = config("NEXTCLOUD_PASSWORD", default="Stud3nt@CC2026!")
NEXTCLOUD_FOLDER = config("NEXTCLOUD_FOLDER", default="Project-Team/Reports").strip("/")


def upload_to_nextcloud(filename: str, content_bytes: bytes, folder: str = NEXTCLOUD_FOLDER) -> dict:
    """
    Uploads a file to Nextcloud using WebDAV PUT.
    Returns metadata including status, path, and public/internal access URL.
    """
    # Construct WebDAV URL: /remote.php/dav/files/<user>/<folder>/<filename>
    dav_url = f"{NEXTCLOUD_BASE_URL}/remote.php/dav/files/{NEXTCLOUD_USER}/{folder}/{filename}"

    # Basic Auth header
    credentials = f"{NEXTCLOUD_USER}:{NEXTCLOUD_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/octet-stream",
    }

    req = urllib.request.Request(dav_url, data=content_bytes, headers=headers, method="PUT")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status_code = response.status
            logger.info("Uploaded %s to Nextcloud (HTTP %s)", filename, status_code)
            return {
                "success": True,
                "status_code": status_code,
                "filename": filename,
                "remote_path": f"/{folder}/{filename}",
                "nextcloud_url": dav_url,
                "owner": NEXTCLOUD_USER,
            }
    except urllib.error.HTTPError as e:
        logger.error("Nextcloud WebDAV HTTP error: %s %s", e.code, e.reason)
        return {
            "success": False,
            "status_code": e.code,
            "error": f"HTTP {e.code}: {e.reason}",
            "filename": filename,
        }
    except Exception as e:
        logger.error("Failed to upload to Nextcloud: %s", str(e))
        return {
            "success": False,
            "error": str(e),
            "filename": filename,
        }
