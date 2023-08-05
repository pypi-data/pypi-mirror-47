# htmldocx
Convert html to docx

Dependencies: `python-docx` & `bs4` (if you want to fix html before converting or extract tables)

### To install

`pip install htmldocx`

### Usage

Add strings of html to an existing docx.Document object

```from parser import HtmlToDocx
from docx import Document
from htmldocx import HtmlToDocx

document = Document()
new_parser = HtmlToDocx()
# do stuff to document

html = '<h1>Hello world</h1>'
new_parser.add_html_to_document(html, document)

# do more stuff to document
document.save('your_file_name')
```

Convert files directly

`new_parser.parse_html_file(input-html-file, output-docx-file)`

Specify options: options default to `True`. Set to `False` before running to disable extraction

`new_parser.options['tables'] = False`

Currently available options: `tables`, `images`
