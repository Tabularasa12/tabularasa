from .taggers import *
from .elements import *
from utils.functions import labelize
from settings import DEFAULT_SIZE
from wtforms import Form, SelectField, RadioField, StringField, validators
from markupsafe import Markup

class Control(Tagger):
    CLASSES = dict(
        CheckboxInput = 'input',
        FileInput = 'input',
        HiddenInput = 'input',
        ListWidget = 'select is-multiple',
        PasswordInput = 'input',
        RadioInput = 'input',
        Select = 'select',
        SubmitInput = 'input',
        TableWidget = '',
        TextArea = 'textarea',
        TextInput = 'input',
        Option = ''
    )
    def __init__(self, name=None, field=None, **attributes):
        widget = str_2_tagger(str(field))
        widget._class += self.CLASSES[field.widget.__class__.__name__]
        attributes['_id'] = f'{name}_control'
        Tagger.__init__(self, 'DIV', widget, **attributes)
        self._class += 'control'

class Field(Tagger):
    def __init__(self, name, field, **attributes):
        attributes['_id'] = f'{name}_field'
        Tagger.__init__(self, 'DIV', Control(name, field), **attributes)
        self._class += 'field'


class Html_form(Tagger):
    def __init__(self, form, **attributes):
        self.form = form
        self._fields = []
        for name, field in self.form._fields.items():
            self._fields.append(Field(name, field))
        children = [
            *self._fields,
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
        attributes['_method'] = 'POST'
        Tagger.__init__(self, 'FORM', *children, **attributes)
        self._class += 'form box'

class Form_config(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])

# class Widget(Tagger):
#     def __html__(self, field):
#         if field.label:
#             label = LABEL(field.name, _class='label')
        # field = 
#     input = INPUT(_class='input', _type='text', _placeholder='Text')
#     control = DIV(input, _class='control')
#     ret = DIV(label, control, _class='field')
#     if field.errors:
#         for error in field.errors:
#             ret.append(P(error, _class='danger'))
#     return ret


# class Error(Tagger):
#     def __init__(self, name, *children, color='danger', **attributes):
#         Tagger.__init__(self, 'P', *children, id=name, **attributes)
#         self._class += 'helper'
#         self.message = self.children

# class Text_lenth:
#     def __init__(self, min=1, max=1):
#         self.min = min
#         self.max = max

#     def validate(self, value):
#         errors = dict()
#         if isinstance(value, str):
#             if len(value) < self.min:
#                 errors['']
#         return errors



# class Widget(Tagger):
#     def __init__(self, field, *children, **attributes):
#         self.value = field.value
#         children = [*children]
#         self.type = field.widget
#         if self.type == 'text':
#             placeholder = field.default
#             children.append(INPUT(_class='input', _value=self.value, _type=self.type, _placeholder=placeholder))
#         Tagger.__init__(self, 'div', *children, _id=f'control_{field._id}', **attributes)
#         self._class += 'control'

# class Field(Tagger):
#     def __init__(
#         self,
#         id=None,
#         value=None,
#         default='text',
#         validators=[],
#         widget='text',
#         label=None,
#         labelize=False,
#         **attributes
#         ):
#         self.type = self.__class__.__name__.split('_')
#         if len(self.type) == 2:
#             self.type = self.type[1]
#         else:
#             self.type = 'text'
#         self._id = id if id else self.type.lower()
#         children = []
#         if label: labelize = True
#         self.label = ''
#         if labelize:
#             children.append(LABEL(label if label else labelize(self.id), _class='label'))
#         self.value = value
#         self.default = default
#         self.widget = widget
#         self.validators = validators
#         children.append(Widget(self))
#         Tagger.__init__(self, 'div', *children, **attributes)
#         self._class += 'field'
    
#     def validate(self, value):
#         validation = True
#         if self.validators:
#             for validator in self.validators:
#                 if not validator.validate(value):
#                     self.children.append(validator.error)
#                     validation = False
#         return validation

# class Field_text(Field):
#     def __init__(self):
#         Field.__init__(self)

# class Form(Tagger):
#     AUTORIZED_METHODS=['GET', 'POST', 'PUT']
#     def __init__(self, id=None, datas=dict(), fields=[], **attributes):
#         children = [
#             *fields,
#             DIV(
#                 DIV(
#                     Button(_id='submit_button', type='submit'),
#                     Button(_id='cancel_button', type='submit'),
#                     _id='buttons_control',
#                     _class='control'
#                 ),
#                 _id='buttons_field',
#                 _class='field is-grouped'
#             )
#         ]

#         Tagger.__init__(self, 'form', *children, **attributes)
#         self._id = id if id else self.__class__.__name__.split('_')[1] if '_' in self.__class__.__name__ else self.__class__.__name__
#         self._class += 'form'
#         if not '_method' in self.attributes.keys(): self.method = 'POST'
#         # self._db = db
#         # self._function = function(datas) if function else self.children
#         # if isinstance(datas, dict):
#         #     self.validate(datas)
        
#     # def __get__fileds__(self):
#     #     return self.children
#     # def __set_fields__(self, **values):
#     #     for field in self.__get__fileds__():
#     #         if field.name in values.keys():
#     #             field.value = values[field.name]
#     # def __del__fields__(self):
#     #     self.children = []
#     # fileds = property(__get__fileds__, __set_fields__, __del__fields__)

#     def __get__method__(self):
#         if '_method' in self.attributes.keys():
#             return self.attributes['_method']
#         return None
#     def __set_method__(self, name):
#         if name in self.AUTORIZED_METHODS:
#             self.attributes['_method'] = name
#     method = property(__get__method__, __set_method__)

#     def validate(self, **datas):
#         validation = True
#         for field in self.fileds:
#             if field.name in datas.keys():
#                 if not field.validate(datas[field.name]):
#                     validation = False
#                     for error in field.errors:
#                         filed.helper.append(error)
#         return validation

# class Form_config(Form):
#     fields=[
#         Field_text()
#     ]
#     def __init__(self, id=None, datas=dict(), **attributes):
#         Form.__init__(self, id=None, datas=dict(), fields=self.fields, **attributes)
#         print(self)