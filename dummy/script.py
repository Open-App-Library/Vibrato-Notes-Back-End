import json
from random import randint
from django.contrib.auth.models import User
from notes.models import Note, Notebook, Tag

# How to Run This Script:
# Open up the Django Shell and type...
# >>> from dummy import script
# >>> script.all()
# Voila!
# You could also import things individually
# >>> script.import_notebooks()
# >>> script.import_tags()
# >>> script.import_notes()

USER = User.objects.all()[0] # First user

def load_json(fname):
	with open("dummy/"+fname) as f:
		return json.load(f)
	return None

# Import Notebooks
def import_notebooks():
	notebooks = load_json("notebooks.json")
	def import_notebook(notebook, parent=None):
		new_notebook = Notebook()
		new_notebook.title = notebook['title']
		new_notebook.user = USER
		if parent:
			new_notebook.parent = parent
		new_notebook.save()
		if notebook.get("children", None):
			for child in notebook['children']:
				import_notebook(child, new_notebook)
	for notebook in notebooks:
		import_notebook(notebook)
	print("Imported Notebooks.")

# Import Tags
def import_tags():
	tags = load_json("tags.json")
	for tag in tags:
		new_tag = Tag()
		new_tag.title = tag
		new_tag.user  = USER
		new_tag.save()
	print("Imported Tags.")

# Import Notes
def import_notes():
	notes = load_json("notes.json")
	notebooks = Notebook.objects.all()
	notebooksl = len(notebooks) - 1
	tags = Tag.objects.all()
	tagsl = len(tags) - 1
	for note in notes:
		new_note = Note()
		new_note.title = note['title']
		new_note.text  = note['text']
		new_note.user  = USER
		new_note.notebook = notebooks[randint(0, notebooksl)]
		amt_of_tags = randint(0, tagsl)
		new_note.save()
		for i in range(0, amt_of_tags):
			new_note.tags.add(tags[randint(0, tagsl)])
		new_note.save()
	print("Imported Notes.")

def all():
	import_notebooks()
	import_tags()
	import_notes()
	print("Imported everything!")
