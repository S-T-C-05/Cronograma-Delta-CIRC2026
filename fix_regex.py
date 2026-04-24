import re

with open('Cronograma.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the rogue `});`
old_text = text
text = re.sub(r'                tbody\.appendChild\(row\);\s*\}\);\s*\}\s*\}\);\s*\}\s*function updateStatus',
              r'''                tbody.appendChild(row);
             });
          }
      }
      
    function updateStatus''', text)

# Now fix the </script> tag
text = re.sub(r'<script src=\'https://cdn\.jsdelivr\.net/npm/fullcalendar@6\.1\.11/index\.global\.min\.js\'>\s*function goToPhase.*?\}\s*</script>\s*<script>\s*<style>',
             r"<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>\n<style>", text, flags=re.DOTALL)

with open('Cronograma.html', 'w', encoding='utf-8') as f:
    f.write(text)

if old_text != text:
    print("Corrections applied successfully with regex substitution.")
else:
    print("Nothing changed. Regex did not match.")
