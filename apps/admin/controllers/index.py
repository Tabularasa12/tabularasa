
from flask import url_for
from .. import app
from utils.html import *
from utils.functions import labelize

@app.route('/')
@app.route('/index')
@app.to_page()
def index():
    # app.page.navbar_position = 'top'
    body = A(
        Image(url=app.page.logo['_href'], replace="Logo", size=300),
        _href=url_for('index'),
        _title = labelize("recharger la page"),
    )
    return locals()




# msg = Message("Hello",
#     sender = 'locauxmotives@gmail.com',
#     recipients=['etienne@semou.fr'],
#     body = 'ok, merci',
#     html = default.page.content.xml(),
# )
# options = {
#     # 'page-size': 'A4',
#     # 'dpi': 100,
#     # 'orientation' : 'Portrait',
#     # 'disable-smart-shrinking': True,
#     # 'page-height' : 300,
#     # 'page-width' : 300,
# }
# pdfkit.from_url('http://127.0.0.1:5000/pdf', 'static/out.pdf', options=options)
# # with default.open_resource(url_for('static', filename='out.pdf')) as fp:
# #     msg.attach(url_for('static', filename='out.pdf'), "file/pdf", fp.read())

# # mail.send(msg)


# @default.route('/pdf')
# @default.to_page()
# def pdf():
#     logo = A(
#         IMG(_src=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), _alt="Logo", _style='max-width:300px;'),
#         _href=url_for('index'),
#         _title = labelize("recharger la page"),
#     )
#     body = Buttons(logo, _class='is-centered')
#     return locals()
