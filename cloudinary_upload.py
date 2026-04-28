import cloudinary
import cloudinary.uploader
CLOUDINARY_URL = "dayygto4l"
API_KEY = "976457723419674"
API_SECRET = "DdsEFat4HOOGNrdbSGcuRjylflk"

cloudinary.config(
    cloud_name=CLOUDINARY_URL,
    api_key=API_KEY,
    api_secret=API_SECRET
)


def upload_pdf(pdf_file):
    res = cloudinary.uploader.upload(f"receipts/{pdf_file}.pdf")
    print(res["secure_url"])
    return "success"


upload_pdf("myimage")
