import re

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Fullcalendar weirdness explicitly (it may not have matched before because my bad_fc regex was too specific)
text = re.sub(r"<script src='https://cdn\.jsdelivr\.net/npm/fullcalendar@6\.1\.11/index\.global\.min\.js'>\nfunction goToPhase\(targetId\) \{.*?\n\}\n</script>\n<script>\n<style>", 
      r"<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>\n<style>", text, flags=re.DOTALL)

# Ensure goToPhase exists normally using a safer insertion
gotophase_fn = """
function goToPhase(targetId) {
    const tabBtn = document.querySelector('button[onclick*="descripcion"]');
    if (tabBtn) openTab('descripcion', tabBtn);
    setTimeout(() => {
       const target = document.querySelector('.' + targetId);
       if(target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          const originalBg = target.style.backgroundColor;
          target.style.transition = "background 0.5s ease";
          target.style.backgroundColor = "#fff3cd";
          target.style.borderRadius = "8px";
          setTimeout(() => {
             target.style.backgroundColor = originalBg; 
          }, 1200);
       }
    }, 100);
}
"""
if 'function goToPhase' not in text:
    text = text.replace('function closeDayModal()', gotophase_fn + '\nfunction closeDayModal()')

# Fix the renderTable suffix
text = re.sub(r"""                tbody\.appendChild\(row\);\s*\}\);\s*\}\s*\}\);\s*\}\s*function updateStatus\(id, newStatus\) \{""",
r"""                tbody.appendChild(row);
             });
          }
      }

    function updateStatus(id, newStatus) {""", text, flags=re.DOTALL)


with open(html_file, 'w', encoding='utf-8') as f:
    f.write(text)
    
print("All fixes applied forcibly!")
