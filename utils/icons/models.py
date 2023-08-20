from ..files import *

class Icons:
    prefix='fa-'
    first_line = 496
    end_line = 6350
    icons_dir = 'icons'

    def __init__(self, css_path_file):
        self.path = css_path_file
        self.css = self.path.split(self.icons_dir, 1)[1].strip('/')
        lines = read(css_path_file, type='list')[self.first_line:self.end_line]
        content_list = []
        code = content = None
        for line in lines:
            if not code and line.startswith('.{}'.format(self.prefix)):
                code = line.split('.{}'.format(self.prefix))[1].split(':', 1)[0].strip()
            elif code and 'content:' in line:
                content = line.split('content:')[1].split('"')[1].strip('\\')
                content_list.append((code, content))
                code = content = None
        used_content = []
        icons = []
        for code, content in content_list:
            if not content in used_content:
                icons.append(code)
                used_content.append(content)
        
        self.list = dict()
        for code in icons:
            self.list[code] = '{}{}'.format(self.prefix, code)
    
    def __getitem__(self, name):
        return self.list[name]
    