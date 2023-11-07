from markupsafe import Markup
from wtforms import Form, StringField

from settings import DEFAULT_SIZE
from utils.functions import labelize

from .elements import *
from .taggers import *
from .validators import *


class Control(Tagger, type):
    WIDGET_CLASSES = {
        'CheckboxInput' : 'input',
        'FileInput' : 'input',
        'HiddenInput' : 'input',
        'ListWidget' : 'select is-multiple',
        'PasswordInput' : 'input',
        'RadioInput' : 'input',
        'Select' : 'select',
        'SubmitInput' : 'input',
        'TableWidget' : '',
        'TextArea' : 'textarea',
        'TextInput' : 'input',
        'Option' : ''
    }
    def __init__(self, nom, bases, dict):
        Tagger.__init__(self, 'DIV', **self.attributes)
        self._class += 'control'
        self.field = None
        self.label = None

    def __call__(self, form, name, **attributes):
        attributes['_id'] = f'control_{name}'
        self.field = form.form._fields[name]
        self.label = str_2_tagger(str(self.field.label))
        self.widget = str_2_tagger(str(self.field))
        self.widget._class += self.WIDGET_CLASSES[self.field.widget.__class__.__name__]
        if form.requette:
            self.widget.color = 'danger' if self.field.errors else 'success'

class Control_string(metaclass=Control):
    self.icon = 'cog'
    self.attributes['_class'] = 'has-icons-left has-icons-right'
    # def __init__(self, form, name, icon='user', **attributes):
    #     Control.__init__(self, form, name)
    #     if not form.labelized:
    #         self.widget.attributes['_placeholder'] = labelize(self.label.children[0])
    #     self.children.append(self.icon)
    #     if form.requette:
    #         self.children.append(Icon('check', _class='is-right', _id='icon_right', color='success'))
    #         if self.field.errors:
    #             color = 'danger'
    #             self.icon_left.color = color
    #             self.icon_right.color = color
    #             self.icon_right.code = 'exclamation-triangle'

class Field(Tagger, type):
    def __init__(self, nom, bases, dict):
        Tagger.__init__(self, 'DIV')
        self._class += 'field'
        self.field = None
        self.label = None

    def __call__(self, form, name, **attributes):
        attributes['_id'] = f'field_{name}'
        self.control = self.control(form, name, **attributes)
        self.field = form.form._fields[name]
        self.children = [self.control]
        if form.labelized:
            self.label = str_2_tagger(str(self.field.label))
            self.label.children = [labelize(self.label.children[0])]
            self.label._class += 'label'
            children.insert(0, self.label)
        if self.field.errors:
            children.append(P(labelize(self.field.errors[0]), _class='help is-danger'))
        return self

class Field_string(Field):
    control = Control_string
    def __call__(self, form, name, **attributes):
    #     if not 'control' in attributes.keys(): 
    #         attributes['control'] = Control_string(form, name)
        Field.__call__(self, form, name, 'cog', **attributes)

class Field_name(Field_string):
    icon = 'user'
    # def __init__(self, form, name, **attributes):
    #     attributes['control'] = Control_string(form, name, 'user')
    #     Field_string.__init__(self, form, name, **attributes)

class Field_email(Field_string):
    icon = 'at'
    # def __init__(self, form, name, **attributes):
    #     attributes['control'] = Control_string(form, name, 'at')
    #     Field_string.__init__(self, form, name, **attributes)

class Html_form(Tagger, type):
    def __new__(cls, nom, bases, dict):
        return type.__new__(cls, nom, bases, dict)

    def __init__(self, nom, bases, dict):
        self.html_fields = []
        self.flask_fields = {}
        for name, field in self.fields.items():
            self.flask_fields[name] = field['flask'](field['title'], field['validators'])
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

    def __call__(self, request, **attributes):
        self.attributes['_method'] = 'POST' if not '_method' in attributes.keys() else 'GET' if attributes['_method'] == 'GET' else 'POST'
        if 'title' in attributes.keys(): self.form_title.update(attributes['title'])
        if 'labelized' in attributes.keys(): self.labelized = attributes['labelized']
        self.request = request
        self.datas = self.request.form
        self.form = type("Flask_form", (Form,), self.flask_fields)(self.datas)
        if self.requette:
            self.form.validate()
        fields = []
        for name, field in self.html_fields:
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

