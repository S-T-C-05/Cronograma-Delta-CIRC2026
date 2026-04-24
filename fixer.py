import re
with open('Cronograma.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the rogue `});` block
text = re.sub(r'tbody\.appendChild\(row\);\s*\}\);\s*\}\s*\}\);\s*\}',
              r'tbody.appendChild(row);\n             });\n          }\n      }', text)

text = re.sub(r"<script src='https://cdn\.jsdelivr\.net/npm/fullcalendar@6\.1\.11/index\.global\.min\.js'>\s*function goToPhase\(targetId\) \{.*?\n\}\s*</script>\s*<script>\s*<style>",
             r"<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>\n<style>", text, flags=re.DOTALL)

with open('Cronograma.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done with pure replacement")
