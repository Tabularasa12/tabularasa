from .taggers import *
from settings import DEFAULT_SIZE

__all__ = [
    'Buttons',
    'Button',
    'Text',
    'Icon',
    'Image',
    'Icon_image',
    'Title',
    'Subtitle',
    'Content',
    'Block',
    'Box',
    'Container',
    'Section',
    'Level'
]

class Buttons(Tagger):
    def __init__(self, *children, **attributes):
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += self.__class__.__name__.lower()

class Button(Tagger):
    def __init__(self, *children, _type='A', **attributes):
        Tagger.__init__(self, _type, *children, **attributes)
        self._class += self.__class__.__name__.lower()
        self.url = attributes['url'] if 'url' in attributes.keys() else ''
        self.title = attributes['title'] if 'title' in attributes.keys() else None
        if not 'size' in self.attributes.keys(): self.size = DEFAULT_SIZE

    def __get_url__(self):
        return self.attributes['_href']
    def __set_url__(self, name):
        self.attributes['_href'] = name
    def __del_url__(self):
        self.attributes['_href'] = '#'
    url = property(__get_url__, __set_url__, __del_url__)

    def __get_text__(self):
        return self.attributes['_title']
    def __set_text__(self, value): 
        self.attributes['_title'] = value
    def __del_text__(self):
        self.attributes['_title'] = ''
    text = property(__get_text__, __set_text__, __del_text__)

class Text(Tagger):
    autorized_formats = ['capitalized', 'lowercase', 'uppercase', 'italic', 'bold']
    def __init__(self, *text, **attributes):
        Tagger.__init__(self, *text, **attributes, _base='SPAN')
        self.formats = self.attributes['formats'] if 'formats' in attributes.keys() else None

    def get_formats(self):
        return self.attributes['formats']
    def set_formats(self, *name):
        name = [*name]
        for n in name:
            if n in self.autorized_formats:
                sizes = ['capitalized', 'lowercase', 'uppercase']
                if n in sizes:
                    sizes.remove(n)
                    for size in sizes:
                        self._class -= 'is-{}'.format(size)
                        if self.formats:
                            if size in self.formats:
                                self.attributes['formats'].remove(size)
                if n == 'bold':
                    self._class += 'has-text-weight-{}'.format(n)
                else:
                    self._class += 'is-{}'.format(n)
                self.attributes['formats'].append(n)
    def del_formats(self):
        for type in self.autorized_formats:
            if type == 'bold':
                self._class -= 'has-text-weight-{}'.format(type)
            else:
                self._class -= 'is-{}'.format(type)
            if type in self.formats:
                self.attributes['formats'].remove(type)
    formats = property(get_formats, set_formats, del_formats)

    color = Tagger.text_color

class Icon(Tagger):
    def __init__(self, code, prefix='fa-', **attributes):
        Tagger.__init__(self, 'SPAN', I(_id='icon', _class=f'fa {prefix}{code}'), **attributes)
        self._class += self.__class__.__name__.lower()
        self.prefix = prefix
        self.code = code
        self.size = self.attributes['size'] if 'size' in self.attributes.keys() else DEFAULT_SIZE

    color = Tagger.text_color

    def get_code(self):
        for item in self.icon._class.list:
            if item.startswith(self.prefix):
                return item.split(self.prefix)[1]
    def set_code(self, name):
        if isinstance(name, str):
            self.icon._class.replace(f'{self.prefix}{self.code}', f'{self.prefix}{name}')
    def del_code(self):
        self.icon._class.replace(f'{self.prefix}{self.code}', 'fa')
    code = property(get_code, set_code)

    def get_size(self):
        return self.icon.size
    def set_size(self, value):
        self.icon.size = value
    def del_size(self):
        del self.icon.size
    size = property(get_size, set_size, del_size)

class Image(Tagger):
    AUTORIZED_IMAGE_SIZES = [16, 24, 32, 48, 64, 96, 128, 196, 256, 384, 512, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700]
    def __init__(self, **attributes):
        image = IMG(
            _src = attributes['url'] if 'url' in attributes.keys() else '#',
            _title = attributes['text'] if 'text' in attributes.keys() else '',
            _alt = attributes['replace'] if 'replace' in attributes.keys() else '',
            _id='image',
        )
        Tagger.__init__(self, 'SPAN', image, **attributes)
        self._class += self.__class__.__name__.lower()

    def __get_url__(self): 
        return self.image['_src']
    def __set_url__(self, value): 
        self.image['_src'] = value
    def __del_url__(self):
        self.image['_src'] = '#'
    url = property(__get_url__, __set_url__, __del_url__)

    def __get_text__(self):
        return self.image['_title']
    def __set_text__(self, value): 
        self.image['_title'] = value
    def __del_text__(self):
        self.image['_title'] = ''
    text = property(__get_text__, __set_text__, __del_text__)

    def __get_replace__(self): 
        return self.image['_alt']
    def __set_replace__(self, value): 
        self.image['_alt'] = value
    def __del_replace__(self):
        self.image['_alt'] = ''
    replace = property(__get_replace__, __set_replace__, __del_replace__)

    def __get_size__(self):
        for size in self.AUTORIZED_IMAGE_SIZES:
            if f'is-{size}x{size}' in self._class.list:
                return size
        for size in self.AUTORIZED_SIZES:
            if f'is-size-{size}' in self._class.list:
                return size
        return None
    def __set_size__(self, value):
        hold_size = self.__get_size__()
        hold_size_class = None
        if hold_size:
            if hold_size in self.AUTORIZED_IMAGE_SIZES:
                hold_size_class = f'is-{hold_size}x{hold_size}'
            else:
                hold_size_class = f'is-size-{hold_size}'
        new_size_class = None
        if value in self.AUTORIZED_IMAGE_SIZES:
            new_size_class = f'is-{value}x{value}'
        elif value in self.AUTORIZED_SIZES:
            new_size_class = f'is-size-{value}'
        if new_size_class:
            self._class.replace(hold_size_class, new_size_class)
    def __del_size__(self):
        hold_size = self.__get_size__()
        if hold_size in self.AUTORIZED_IMAGE_SIZES:
            self._class -= f'is-{hold_size}x{hold_size}'
        elif hold_size in self.AUTORIZED_SIZES:
            self._class -= f'is-size-{hold_size}'
    size = property(__get_size__, __set_size__, __del_size__)

    def __get_color__(self):
        return self.image.back_color
    def __set_color__(self, name):
        if name in AUTORIZED_COLORS:
            self.image.back_color = name
    def __del_color__(self):
        del self.image.back_color
    color = property(__get_color__, __set_color__, __del_color__)

class Icon_image(Tagger):
    def __init__(self, **attributes):
        Tagger.__init__(self, 'SPAN', IMG(_src=attributes['url'], _id='image'), **attributes)
        self._class += 'icon'

    def get_size(self):
        return self.image.size
    def set_size(self, value):
        self.image.size = value
    def del_size(self):
        del self.image.size
    size = property(get_size, set_size, del_size)

    replace = Image.replace
    text = Image.text
    url = Image.url
    color = Image.color

class Title(Tagger):
    default_size = 2
    def __init__(self, *children, **attributes):
        if 'size' in attributes.keys():
            self._size = attributes['size']
            del attributes['size']
        else:
            self._size = self.default_size
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += self.__class__.__name__.lower()
    
    # def __get_size__(self):
    #     return self._size
    # def __set_size__(self, value):
    #     if isinstance(value, int):
    #         self._base[1:] = value
    #         self._size = value
    # def __del_size__(self):
    #         self._base[1:] = self.default_size
    #         self._size = self.default_size
    # size = property(get_size, get_size, del_size)

    color = Tagger.text_color

class Subtitle(Title):
    def __init__(self, *children, **attributes):
        Title.__init__(self, 'DIV', *children, **attributes)
        self._class.replace('title', 'subtitle')

class Content(Tagger):
    def __init__(self, *children, **attributes):
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += 'icon-text'

class Block(Tagger):
    def __init__(self, *children, **attributes):
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += self.__class__.__name__.lower()

class Box(Tagger):
    def __init__(self, *children, **attributes):
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += self.__class__.__name__.lower()

class Container(Tagger):
    def __init__(self, *children, **attributes):
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += self.__class__.__name__.lower()

class Section(Tagger):
    def __init__(self, *children, **attributes):
        Tagger.__init__(self, 'DIV', *children, **attributes, _base='section')
        self._class += self.__class__.__name__.lower()

class Level(Tagger):
    def __init__(self, *children, **attributes):
        Tagger.__init__(self, 'DIV', *children, **attributes)
        self._class += self.__class__.__name__.lower()

class Notification(Tagger):
    def __init__(self, id, message, url, **attributes):
        self.id = id
        url = Url(url)
        url.vars['del_flash'] = self.id
        button = Button(url=url(), _class='delete', _name='button')
        Tagger.__init__(self, button, str(message), **attributes)
        self._class += self.__class__.__name__.lower()
        if 'active' in self.attributes.keys():
            if self.attributes['active']:
                self.activate
            else:
                self.desactivate
            del self.attributes['active']

    @property
    def dict(self):
        return dict(message=self.message, **self.attributes)
    
    @property
    def activate(self):
        self._class -= 'is-hidden'

    @property
    def desactivate(self):
        self._class += 'is-hidden'
    
    @property
    def is_active(self):
        return False if 'is-hidden' in self._class.list else True
    
    def __get_url__(self):
        return self.button.url
    def __set_url__(self, url):
        url.vars['del_flash'] = self.id
        self.button.url = url
    def __del_url__(self):
        self.button.url = '#'
    url = property(__get_url__, __set_url__, __del_url__)

    def get_message(self):
        return self.children[1]
    def set_message(self, message):
        self.children[1] = str(message)
    def del_message(self):
        self.children[1] = ''
    message = property(get_message, set_message, del_message)

    def get_color(self):
        return Tagger.get_color(self)
    def set_color(self, name):
        Tagger.set_color(self, name)
        self.button.color = name
    def del_color(self):
        Tagger.del_color(self)
        self.button.color = None
    color = property(get_color, set_color, del_color)


# class Flash(Container):
#     def __init__(self, page, **attributes):
#         self.session = page.session
#         self.url = Url(page.url)
#         Container.__init__(self, *self.session_to_children, **attributes)
#         self._class -= 'flash'
    
#     @property
#     def dict(self):
#         ret = dict()
#         for child in self.children:
#             attr = copy.deepcopy(child.attributes)
#             _class=str(attr['_class'])
#             _style=str(attr['_style'])
#             del attr['_class']
#             del attr['_style']
#             ret[child.id] = dict(
#                 message=child.children[1],
#                 url=self.url(),
#                 _class=_class,
#                 _style=_style,
#                 **attr
#             )
#         return ret
    
#     def dict_to_notif(self, id, dict):
#         message = ''
#         if 'message' in dict.keys():
#             message = dict['message']
#             del dict['message']
#         url = self.url
#         if 'url' in dict.keys():
#             url = self.url()
#             del dict['url']
#         return Notification(id, message, url, **dict)
    
#     def dict_to_list(self, dict):
#         ret = []
#         for k, v in dict.items():
#             ret.append(self.dict_to_notif(k, v))
#         return ret
    
#     @property
#     def session_to_children(self):
#         return self.dict_to_list(self.session['flash'])
    
#     @property
#     def children_to_session(self):
#         self.session['flash'] = self.dict

#     def append(self, id, dict):
#         self.children.append(self.dict_to_notif(id, dict))
#         self.children_to_session
    
#     def update(self, id, dict):
#         for num, child in enumerate(self.children):
#             if id == child.id:
#                 self.children[num] = self.dict_to_notif(id, dict)
#         self.children_to_session

#     def delete(self, name):
#         if self[name]:
#             new_children = []
#             for num, children in enumerate(self.children):
#                 if children.id != name:
#                     new_children.append(self.children[num])
#             self.children = new_children
#         self.children_to_session

#     def activate(self, name):
#         if self[name]:
#             for num, children in enumerate(self.children):
#                 if children.id == name:
#                     self.children[num].activate
#         self.children_to_session

#     def desactivate(self, name):
#         if self[name]:
#             for num, children in enumerate(self.children):
#                 if children.id == name:
#                     self.children[num].desactivate
#         self.children_to_session
    
#     def __getitem__(self, name):
#         for num, notification in enumerate(self.children):
#             if name == notification.id:
#                 return self.children[num]
#         return None
#     def __setitem__(self, name, attributes):
#         if isinstance(attributes, dict):
#             if not self[name]:
#                 self.append(name, attributes)
#             else:
#                 self.update(name, attributes)

#     def __delitem__(self, name):
#         self.delete(name)
    
#     def xml(self):
#         self.session['flash'] = self.dict
#         return Container.xml(self)
