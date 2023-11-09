from markupsafe import Markup
from wtforms import Form, StringField
from wtforms.validators import Required, InputRequired, DataRequired

from settings import DEFAULT_SIZE
from utils.functions import labelize

from .elements import *
from .taggers import *

class Control(Tagger):
    WIDGET_CLASSES = {
        'CheckboxInput' : 'input',
        'FileInput' : 'input',
        'HiddenInput' : 'input',
        'ListWidget' : 'select is-multiple',
        'PasswordInput' : 'input',
        'SubmitInput' : 'input',
        'Select' : 'select',
        'TableWidget' : '',
        'TextArea' : 'textarea',
        'TextInput' : 'input',
        'Option' : ''
    }
    def __init__(self, form, name, **attributes):
        self.field = form.form._fields[name]
        self.label = str_2_tagger(str(self.field.label))
        self.widget = str_2_tagger(str(self.field))
        self.widget._class += self.WIDGET_CLASSES[self.field.widget.__class__.__name__]
        if form.requette:
            self.widget.color = 'danger' if self.field.errors else 'success'
        attributes['_id'] = f'control_{name}'
        Tagger.__init__(self, 'DIV', self.widget, **attributes)
        self._class += 'control'

class Control_string(Control):
    def __init__(self, form, name, icon='user', **attributes):
        self.icon = Icon(icon, _class='is-left', _id='icon_left')
        Control.__init__(self, form, name)
        if not form.labelized:
            self.widget.attributes['_placeholder'] = labelize(self.label.children[0])
        self._class += 'has-icons-left has-icons-right'
        self.children.append(self.icon)
        if form.requette:
            self.children.append(Icon('check', _class='is-right', _id='icon_right', color='success'))
            if self.field.errors:
                color = 'danger'
                self.icon_left.color = color
                self.icon_right.color = color
                self.icon_right.code = 'exclamation-triangle'

class Control_select(Tagger):
    def __init__(self, form, name, icon='user', **attributes):
        select = Control(form, name)
        select._class.replace('control', 'select')
        select.attributes['_id'] = f'select_{name}'
        attributes['_id'] = f'control_{name}'
        icon = Icon(icon, _class='is-left', _id='icon_left')
        data = form.form._fields[name].data
        Tagger.__init__(self, 'div', select, icon, **attributes)
        self._class += 'control has-icons-left'

class Control_radio(Tagger):
    def __init__(self, form, name, **attributes):
        self.field = form.form._fields[name]
        self.widget = str_2_tagger(str(self.field))
        children = []
        for num, child in enumerate(self.widget.children):
            childrens = child.children
            input = childrens[0]
            label = childrens[1]
            text = label.children[0]
            label._class += 'radio mx-2'
            label._id = f'{name}_{num}_{text}'
            value = Text(text, case='capitalized', transform='italic', weight='normal', _class='ml-1')
            label.children = [input, value]
            children.append(label)
        attributes['_id'] = f'control_{name}'
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += 'control'

class Field(Tagger):
    def __init__(self, form, name, labelized=False, **attributes):
        self.field = form.form._fields[name]
        self.labelized = True if labelized else form.labelized
        required = False
        for validator in self.field.validators:
            if isinstance(validator, (Required, InputRequired, DataRequired)):
                required = True
        children = [attributes['control'] if 'control' in attributes.keys() else Control(form, name)]
        self.label = ''
        if self.labelized:
            self.label = str_2_tagger(str(self.field.label))
            self.label.children = [labelize(self.label.children[0])]
            self.label._class += 'label'
            if required:
                self.label.children.append(Icon('star-of-life', color='danger', size=7))
            children.insert(0, self.label)
        if self.field.errors:
            children.append(P(labelize(self.field.errors[0]), _class='help is-danger'))
        attributes['_id'] = f'field_{name}'
        Tagger.__init__(self, 'DIV', *children, **attributes)
        if not self.labelized:
            if required:
                self.children.insert(0, Icon('star-of-life', color='danger', size=7))
        self._class += 'field'

class Field_string(Field):
    def __init__(self, form, name, **attributes):
        if not 'control' in attributes.keys():
            attributes['control'] = Control_string(form, name)
        Field.__init__(self, form, name, **attributes)

class Field_name(Field_string):
    def __init__(self, form, name, **attributes):
        attributes['control'] = Control_string(form, name, 'user')
        Field_string.__init__(self, form, name, **attributes)

class Field_email(Field_string):
    def __init__(self, form, name, **attributes):
        attributes['control'] = Control_string(form, name, 'at')
        Field_string.__init__(self, form, name, **attributes)

class Field_select(Field):
    def __init__(self, form, name, icon='user', **attributes):
        control= attributes['control'] if 'control' in attributes.keys() else Control_select(form, name, icon)
        Field.__init__(self, form, name, control=control, **attributes)

class Field_color(Field_select):
    def __init__(self, form, name, **attributes):
        data = form.request.form[name] if form.requette else form.page.color if form.page.color else None
        if data: form.form._fields[name].data = str(data)
        Field_select.__init__(self, form, name, 'palette', labelized=True, **attributes)
        if data: self.icon_left.color = data

class Field_radio(Field):
    def __init__(self, form, name, **attributes):
        control= attributes['control'] if 'control' in attributes.keys() else Control_radio(form, name)
        Field.__init__(self, form, name, control=control, labelized=True, **attributes)

class Field_navbar_position(Field_radio):
    def __init__(self, form, name, **attributes):
        position = form.request.form[name] if form.requette else form.page.config[name]['position']
        form.form._fields[name].data = str(position)
        Field_radio.__init__(self, form, name, **attributes)

class Html_form(Tagger, type):
    def __init__(self, nom, bases, dict):
        self.html_fields = []
        self.flask_fields = {}
        for name, field in self.fields.items():
            self.flask_fields[name] = field['flask']
            self.html_fields.append((name, field['html']))
        children = [
            DIV(
                Text(
                    self.title,
                    _id = 'form_title',
                    _class="card-header-title is-centered",
                    size=4,
                    case='capitalized',
                    transform='italic',
                    weight='semibold'
                ),
                _class="card-header",
            ),
            DIV(
                'fields',
                _id = 'form_fields',
                _class = 'card-content'
            ),
            DIV(
                Buttons(
                    Button(
                        'Annuler',
                        _id='cancel_button',
                        type='link',
                        color='danger',
                        _class='is-outlined'
                    ),
                    Button(
                        'Enregistrer',
                        _id='submit_button',
                        type='submit',
                        color='success',
                        _class='is-outlined'
                    ),
                    _class='is-centered card-footer-item has-addons'
                ),
                _id='buttons_field',
                _class='field card-footer'
            )
        ]
        Tagger.__init__(self, 'FORM', *children)
        self._class += 'form card'
        self._style = "width:300px;"
        self.labelized = False
        self.request = None

    def __call__(self, page, request, **attributes):
        self.page = page
        self.attributes['_method'] = 'POST' if not '_method' in attributes.keys() else 'GET' if attributes['_method'] == 'GET' else 'POST'
        if 'title' in attributes.keys(): self.form_title.update(attributes['title'])
        if 'labelized' in attributes.keys(): self.labelized = attributes['labelized']
        self.request = request
        self.datas = self.request.form
        self.form = type("Flask_form", (Form,), self.flask_fields)(self.datas)
        if self.requette:
            self.form.validate()
        fields = []
        for num, field in enumerate(self.html_fields):
            name = field[0]
            field = field[1]
            if num > 0:
                fields.append(HR(_class='navbar-divider'))
            fields.append(field(self, name))
        self.form_fields.update(*fields)
        return self

    @property
    def requette(self):
        if self.request.method == self.attributes['_method']:
            return True
        return False
    
    @property
    def errors(self):
        return self.form.errors
    
    @property
    def validate(self):
        if self.requette and not self.errors:
            return True
        return False
    
    @property
    def values(self):
        return self.request.form

