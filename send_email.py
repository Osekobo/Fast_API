# import requests
# ELASTIC_API_KEY="95880A28123E1B13017D907DBCAB98A1B273E42F2802C80EBFB2CED403F9038D0C19CBE7825D537AAEF251A2F9EF3D2A"
import mailtrap as mt
MAILTRAP_API_KEY = "a0676f26230fffa2b4ba92a6447bd3d9"
# FROM_EMAIL="collinsrodent@gmail.com"
# url = "https://api.elasticemail.com/v2/email/send"

# def send_email(to, subject, message):
#     data={"apiKey":MAILTRAP_API_KEY,"subject":subject,"from":FROM_EMAIL,"to":to,"bodytext":message}
#     res=requests.post(url,data=data)
#     print(res)
#     return res.status_code

# send_email("collinsboseko2005@gmail.com","Testing email","I am testing from api")


def email(to, subject, message):
    mail = mt.Mail(
        sender=mt.Address(email="hello@demomailtrap.co", name="Flask API"),
        to=[mt.Address(email=to)],
        subject=subject,
        text=message,
        category="Integration Test",
    )
    client = mt.MailtrapClient(token=MAILTRAP_API_KEY)
    response = client.send(mail)
    print(response)

# email("collinsboseko2005@gmail.com", "Testing email", "I am testing from api")
