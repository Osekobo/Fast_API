from fpdf import FPDF


def generate_pdf(text, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(200, 10, txt=text, align='C')
    pdf.output(f"receipts/{file_name}.pdf")


# text = '<!doctype html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Document</title></head><body><h1>Lorem ipsum10</h1></body></html>'
text = "Lorem ipsum dolor sit amet, \n consectetur adipiscing elit. \n Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
# generate_pdf(text,)
