import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "menutap.settings")
django.setup()

from django.conf import settings
from django.core.files import File
from menu.models import MenuItem

uploaded = 0
not_found = 0
errors = 0

for item in MenuItem.objects.all():
    if not item.image:
        continue

    try:
        # Database me stored image name
        image_name = item.image.name

        # Local media folder ka actual path
        local_path = os.path.join(
            settings.BASE_DIR,
            "media",
            image_name
        )

        if not os.path.exists(local_path):
            not_found += 1
            print(f"NOT FOUND: {item.name} -> {local_path}")
            continue

        filename = os.path.basename(local_path)

        with open(local_path, "rb") as f:
            item.image.save(filename, File(f), save=True)

        uploaded += 1
        print(f"UPLOADED: {item.name}")

    except Exception as e:
        errors += 1
        print(f"ERROR: {item.name} -> {e}")

print("\n====================")
print(f"Uploaded: {uploaded}")
print(f"Not Found: {not_found}")
print(f"Errors: {errors}")
print("====================")