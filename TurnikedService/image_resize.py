from PIL import Image, ImageOps
from io import BytesIO
import piexif
import os

def prepare_hikvision_face_image(input_path: str, output_path: str) -> str:
    """
      Hikvision turniket uchun optimal suratni tayyorlaydi:
      - 400x500 px
      - RGB
      - 96 DPI
      - JPEG, 4:4:4 (no subsampling), no EXIF
      """
    try:
        img = Image.open(input_path).convert("RGB")

        # Center crop 4:5 proportion
        target_size = (400, 500)
        cropped = ImageOps.fit(img, target_size, method=Image.LANCZOS, centering=(0.5, 0.5))

        # White background if needed
        background = Image.new("RGB", target_size, (255, 255, 255))
        background.paste(cropped, (0, 0))

        # Save image without EXIF and optimized for Hikvision
        background.save(output_path, format="JPEG", dpi=(96, 96), quality=95, subsampling=0, optimize=True)
        return output_path
    except Exception as e:
        print(f"❌ Surat tayyorlashda xatolik: {e}")
        return None
if __name__ == "__main__":
    prepare_hikvision_face_image("20251212.jpg", "20251212_ready.jpg")