from django.template.loader import get_template
from weasyprint import HTML

from wsgi import *


def printer_ticket():
    template = get_template('sale/invoice.html')
    context = {
        'title': 'Moises Marin Tantalean'
    }
    html = template.render(context)
    pdf_file = HTML(string=html).write_pdf(target='ticket.pdf')


printer_ticket()
