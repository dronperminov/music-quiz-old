from jinja2 import Environment, FileSystemLoader

templates = Environment(loader=FileSystemLoader("web/templates"), cache_size=0)
