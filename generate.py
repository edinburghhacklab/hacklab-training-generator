import jinja2
import os
from jinja2 import Template

class Item(object):

    def __init__(self, name):
        self.name = name
        self.items = {}
        self.children = True

    def __iter__(self):
        return iter(self.items.items())

    def add(self, key, item):
        self.items[key] = item
        return item

    def __getitem__(self, item):
        return self.items[item]

    def __getattr__(self, attr):
        try:
            return self.items[attr]
        except KeyError:
            raise AttributeError(attr)

    def __str__(self):
        return "<Item '%s'>" % self.name

items = Item('CNC Mill')
safety = items.add('Safety', Item('safety'))
safety.add('Awareness of risks', {})
safety.add('Safety features', {})
safety.add('Use of PPE', {})
basics = items.add('Basics', Item('basics'))
basics.add('Turning on', {})
basics.add('Homing', {})
basics.add('Overrides', {})
basics.add('etc.', {})


latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)
template = latex_jinja_env.get_template('training-card-template.tex')
print(template.render(items = items))