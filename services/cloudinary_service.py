import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Optional

# Configure Cloudinary from environment variables
def configure_cloudinary():
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    api_key = os.getenv("CLOUDINARY_API_KEY", "")
    api_secret = os.getenv("CLOUDINARY_API_SECRET", "")
    
    if cloud_name and api_key and api_secret:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        return True
    return False


class CloudinaryService:
    """Handles image upload/download via Cloudinary."""
    
    def __init__(self):
        self.is_configured = configure_cloudinary()
        self.folder = "rts_game_designer/heroes"
    
    def upload_image(self, file_path: str, hero_id: str, image_type: str = "portrait") -> Optional[str]:
        """Upload image to Cloudinary and return URL."""
        if not self.is_configured:
            return None
        try:
            public_id = f"{self.folder}/{hero_id}_{image_type}"
            result = cloudinary.uploader.upload(
                file_path,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            return result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            return None
    
    def upload_image_bytes(self, file_bytes: bytes, filename: str, hero_id: str, image_type: str = "portrait") -> Optional[str]:
        """Upload image bytes to Cloudinary."""
        if not self.is_configured:
            return None
        try:
            public_id = f"{self.folder}/{hero_id}_{image_type}_{filename}"
            result = cloudinary.uploader.upload(
                file_bytes,
                public_id=public_id,
                overwrite=True,
                resource_type="image"
            )
            return result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            return None
    
    def delete_image(self, hero_id: str, image_type: str = "portrait"):
        """Delete image from Cloudinary."""
        if not self.is_configured:
            return
        try:
            public_id = f"{self.folder}/{hero_id}_{image_type}"
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            print(f"Cloudinary delete error: {e}")
    
    def get_image_url(self, public_id: str) -> str:
        """Get Cloudinary URL for an image."""
        if not self.is_configured:
            return ""
        return cloudinary.CloudinaryImage(public_id).build_url()
