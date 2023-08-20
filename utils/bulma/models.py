import sass
from ..files import *

class Bulma:
    def __init__(self, sass_path_file):
        self.path = sass_path_file
        self.file_name = name(sass_path_file)
        self.dir = dirname(sass_path_file)
        self.start = sass_path_file.split(ext(sass_path_file))[0]
        self.sep = '_'
        self.num = self.get_num()
        self.compile
    
    def get_num(self):
        csss = self.csss
        if len(csss) == 1:
            css = csss[0]
            if self.sep in css and css.endswith('.css'):
                css = css.split('{}{}'.format(self.start, self.sep))
                if not css[1].startswith('.css'):
                    try:
                        return int(css[1].rsplit('.css')[0])
                    except:
                        pass
        self.del_csss
        return 1
        
    @property
    def css(self):
        if len(self.csss) > 1:
            self.del_csss
        if not self.csss:
            self.compile
        return basename(self.csss[0]) if len(self.csss) == 1 else None

    @property
    def csss(self):
        return listdir(self.dir, style='path', start=self.file_name, end='.css')

    @property
    def del_csss(self):
        for file in self.csss:
            delete(file)

    @property
    def compile(self):
        css_file = '{}{}{}.css'.format(self.start, self.sep, self.num)
        if not exist(css_file):
            write(css_file, sass.compile(filename=self.path))

    def update(self, num:int|None=None):
        self.del_csss
        self.num += 1
        if num:
            self.num = num
        if self.num >= 100: self.num = 1
        self.compile

class Sass_file:
    def __init__(self, path, bulma):
        self.path = path
        self.bulma = bulma
        if not isfile(path):
            raise TypeError("{} is not a file".format(path))
        self.content = self.get_file_content()

    def is_var(self, line):
        return True if line.startswith('$') and ':' in line else False
    
    def is_section(self, line):
        return True if line.startswith('//') else False

    def read(self):
        return read(self.path, type='list')
    
    def write(self):
        content = ''
        for line in self.content['start']:
            content += '{}\n'.format(line)
        for section, vars in self.content['sections'].items():
            content += '// {}\n'.format(labelize(section.replace('_', ' ')))
            for key, value in vars.items():
                content += '${}: {}\n'.format(key, value())
        write(self.path, content)
        self.bulma.update()

    def get_file_content(self):
        start=[]
        sections=dict()
        name = ''
        for line in self.read():
            if self.is_section(line):
                name = line.strip('//').strip('\n').strip().replace(' ', '_').lower()
                sections[name] = dict()
            elif self.is_var(line) and name:
                var = line.split(':', 1)
                key = var[0].strip().strip('$')
                value = var[1].strip('\n').strip()
                sections[name][key] = value
            elif not name:
                start.append(line)
        return dict(start=start, sections=sections)

    def __getitem__(self, name):
        return self.content['sections'][name]
    def __setitem__(self, name, vars):
        if isinstance(vars, dict):
            if name not in self.content['sections'].keys():
                self.content['sections'][name] = dict()
            for key, value in vars.items():
                self.set_var(key, value, name)
    def __delitem__(self, name):
        if name in self.content['sections'].keys():
            del self.content['sections'][name]
            self.write()
