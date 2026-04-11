import re, requests
from django.conf import settings

def upload_to_imagekit(django_image_field, project_title):
    slug = re.sub(r'[^a-z0-9]+', '-', project_title.lower()).strip('-')

    raw_name  = django_image_field.name or "upload.jpg"
    file_name = raw_name.split('/')[-1]

    django_image_field.seek(0)

    # ImageKit Upload REST API — no SDK needed
    response = requests.post(
        "https://upload.imagekit.io/api/v1/files/upload",
        auth=(settings.IMAGEKIT_PRIVATE_KEY, ""),  # private key as username, empty password
        data={
            "fileName": file_name,
            "folder"  : f"/projects/{slug}/",
        },
        files={
            "file": (file_name, django_image_field.read()),
        }
    )

    if response.status_code != 200:
        raise Exception(f"ImageKit upload failed: {response.text}")

    return response.json()["url"]