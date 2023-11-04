from markupsafe import Markup
from wtforms import Form, StringField

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
        'RadioInput' : 'input',
        'Select' : 'select',
        'SubmitInput' : 'input',
        'TableWidget' : '',
        'TextArea' : 'textarea',
        'TextInput' : 'input',
        'Option' : ''
    }
    def __init__(self, form, name, **attributes):
        self.form = form
        self.field_name = name
        self.widget = str_2_tagger(str(self.field))
        self.widget = Tagger(self.widget['name'], *self.widget['children'], **self.widget['attributes'])
        self.widget._class += self.WIDGET_CLASSES[self.field.widget.__class__.__name__]
        if form.requette:
            self.widget.color = 'danger' if self.field.errors else 'success'
        attributes['_id'] = 'control'
        Tagger.__init__(self, 'DIV', self.widget, **attributes)
        self._class += 'control'

    @property
    def field(self):
        return self.form.form._fields[self.field_name]

class Control_string(Control):
    def __init__(self, form, name, icon='user', **attributes):
        self.icon = Icon(icon, _class='is-left', _id='icon_left', color='info')
        Control.__init__(self, form, name)
        if not form.labelized:
            self.label = str_2_tagger(str(self.field.label))
            self.label = Tagger(self.label['name'], *self.label['children'], **self.label['attributes'])
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

class Field(Tagger):
    def __init__(self, form, name, **attributes):
        self.form = form
        self.field_name = name
        children = [attributes['control'] if 'control' in attributes.keys() else Control(form, name)]
        self.label = ''
        if self.form.labelized:
            self.label = str_2_tagger(str(self.field.label))
            self.label = Tagger(self.label['name'], *self.label['children'], **self.label['attributes'])
            self.label.children = [labelize(self.label.children[0])]
            self.label._class += 'label'
            children.insert(0, self.label)
        if self.field.errors:
            for error in self.field.errors:
                children.append(P(labelize(error), _class='help is-danger'))
        attributes['_id'] = name
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += 'field'

    @property
    def field(self):
        return self.form.form._fields[self.field_name]

    def __get_control__(self):
        return self.get_children_by_id('control')
    def __set_control__(self, value):
        if isinstance(value, Tagger):
            for num, children in enumerate(self.children):
                if children['_id'] == 'control':
                    self.children[num] = value
    control = property(__get_control__, __set_control__)

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
        attributes['control'] = Control_string(form, name, 'envelope')
        Field_string.__init__(self, form, name, **attributes)

class Html_form(Tagger):
    FILEDS = {
        'name' : Field_name,
        'mail' : Field_email,
    }
    def __init__(self, form, request, labelized=False, **attributes):
        if not '_method' in attributes.keys(): attributes['_method'] = 'POST'
        self.labelized = labelized
        self.fields = []
        self.children = []
        self.request = request
        self.form = form(request.form)
        Tagger.__init__(self, 'FORM', **attributes)
        self._class += 'form box'
        self.populate

    @property
    def populate(self):
        if self.requette:
            self.form.validate()
        self.fields = []
        for name, field in self.form._fields.items():
            self.fields.append(self.FILEDS[name](self, name))
        self.children = [
            *self.fields,
            DIV(
                DIV(
                    Button(_id='submit_button', type='submit', color='success'),
                    Button('Annuler', _id='cancel_button', type='link', color='danger'),
                    _id='buttons_control',
                    _class='control'
                ),
                _id='buttons_field',
                _class='field is-grouped'
            )
        ]
    
    @property
    def requette(self):
        if self.request.method == self.attributes['_method']:
            return True
        return False

