# portfolio/utils.py
from imagekitio import ImageKit
from django.conf import settings
import re

def get_imagekit_client():
    return ImageKit(
        private_key  = settings.IMAGEKIT_PRIVATE_KEY,
        public_key   = settings.IMAGEKIT_PUBLIC_KEY,
        url_endpoint = settings.IMAGEKIT_URL_ENDPOINT,
    )

def upload_to_imagekit(image_file, project_title):
    """
    Uploads a file to ImageKit.
    Saves it in /projects/<project-slug>/ folder.
    Returns the CDN URL string.
    """
    ik = get_imagekit_client()

    # Turn "My Cool Project!" → "my-cool-project"
    slug = re.sub(r'[^a-z0-9]+', '-', project_title.lower()).strip('-')
    folder = f"/projects/{slug}/"

    result = ik.upload_file(
        file=image_file,            # accepts file object or base64
        file_name=image_file.name,
        options={
            "folder": folder,
            "use_unique_file_name": True,  # avoids name collisions
        }
    )
    return result.url