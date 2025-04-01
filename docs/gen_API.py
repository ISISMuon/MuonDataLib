from MuonDataLib.help.help_docs import _text
import os


file_name = os.path.join(os.path.dirname(__file__), 'API.MD')
with open(file_name, 'w') as file:
    file.write('''# Welcome to MuonDataLib API documentation''')

for text in _text:
    text.write_MD(file_name)
