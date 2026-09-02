import os
import sqlite3
import cloudinary
import cloudinary.uploader

# 1. Yahan apni bilkul asli credentials quotes ("") ke andar paste karein
CLOUDINARY_CLOUD_NAME = "nvprwlkq"
CLOUDINARY_API_KEY = "287248521182818"
CLOUDINARY_API_SECRET = "Nzeb_MEwQL60oa6jxVSMv-gwL6E"

# Direct Cloudinary Configuration (Django ko bypass karke)
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

LOCAL_IMAGE_DIR = r"D:\Meenutap\menu_items"
DB_PATH = r"D:\Meenutap\db.sqlite3"  # Aapka sqlite database path

if not os.path.exists(DB_PATH):
    print(f"Error: Database file not found at {DB_PATH}")
    exit()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Database se saare items ki list nikalein (table name usually menu_menuitem hota hai)
try:
    cursor.execute("SELECT id, name, image FROM menu_menuitem")
    rows = cursor.fetchall()
except Exception as e:
    # Agar table name alag ho to check karein
    cursor.execute("SELECT id, name, image FROM menu_item")
    rows = cursor.fetchall()

uploaded = 0
errors = 0
not_found = 0

for item_id, name, image_path in rows:
    if not image_path:
        continue

    filename = os.path.basename(str(image_path))
    local_file_path = os.path.join(LOCAL_IMAGE_DIR, filename)

    if not os.path.exists(local_file_path):
        print(f"NOT FOUND: {name} -> {local_file_path}")
        not_found += 1
        continue

    try:
        # Direct Cloudinary Upload
        res = cloudinary.uploader.upload(
            local_file_path,
            folder="menu_items"
        )
        
        public_id = res.get("public_id")

        # Database direct update (Bina Django interference ke)
        cursor.execute("UPDATE menu_menuitem SET image=? WHERE id=?", (public_id, item_id))
        conn.commit()

        uploaded += 1
        print(f"SUCCESS UPLOADED: {name}")

    except Exception as e:
        errors += 1
        print(f"ERROR on {name}: {e}")

conn.close()

print("\n====================")
print(f"Uploaded: {uploaded}")
print(f"Not Found: {not_found}")
print(f"Errors: {errors}")
print("====================")