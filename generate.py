import jinja2
from jinja2 import Template
import mistune
import os
import subprocess

class Item:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.items = []
        self.children = False

    def __iter__(self):
        return iter(self.items)

    def add(self, item):
        self.items.append(item)
        self.children = True
        return item

    def __getitem__(self, item):
        return self.items[item]

class TreeRenderer(mistune.Renderer):
    def reset_tree(self):
        self.tree = Item('root', 0)
        self.node_stack = [self.tree]
        self.level = 0

    def add_node(self, text, level):
        new_node = Item(text, level)
        self.node_stack[-1].add(new_node)
        self.node_stack.append(new_node)
        self.level = level

    def header(self, text, level, raw=None):
        #print('Got header: {} level: {}'.format(text, str(level)))
        if level == self.level + 1:
            # one level deeper: add new node below current one
            self.add_node(text, level)
        elif level == self.level:
            self.node_stack.pop()
            self.add_node(text, level)
        elif level <= self.level:
            # move up to appropriate parent and add new node there
            while level <= self.level:
                self.node_stack.pop()
                self.level = self.node_stack[-1].level
            self.add_node(text, level)
        else:
            # throw error that new header skips a level
            print('error error error')

        return text

    def list_item(self, text):
        #print("Got list item: {}".format(text))
        return text

    def text(self, text):
        return text.replace("&", "\&")


def walk(item, level):
    print("\t" * level + item.name)
    for i in item:
        walk(i, level + 1)

def get_git_version():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('ascii')

with open('syllabus.md') as f:
    s = f.read()

tree = TreeRenderer()
md = mistune.Markdown(renderer=tree)
tree.reset_tree()
md.parse(s)
#walk(tree.tree, 0)


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
print(template.render(items = tree.tree[0], version = get_git_version()))
