from send_email import email
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
    # res = cloudinary.uploader.upload(f"receipts/{pdf_file}.jpg")
    print(res["secure_url"])
    m = f"Hello, thank you we have received your payment.Click on the link below to find your receipt {res['secure_url']}"
    email("collinsboseko2005@gmail.com", "Payment Received", m)
    return "success"


# print(upload_pdf("UDTHA2HCSG"))
# print(upload_pdf("myimage"))
