import re

with open('Cronograma.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the stray HTML table with the container the new JS function expects
text = re.sub(r'<table id="deliverablesTable">.*?</table>', 
              '<div id="tablesContainer">\n          <!-- Renderizado dinamicamente por JS en multiples tablas -->\n        </div>', 
              text, flags=re.DOTALL)

with open('Cronograma.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("HTML DOM updated to match JS render requirements.")
