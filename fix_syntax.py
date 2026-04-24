import re

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix the FullCalendar script tag and <style>
bad_fc = r"""<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'>
function goToPhase\(targetId\) \{.*?\}
</script>
<script>
<style>"""

good_fc = r"""<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>
<style>"""

text = re.sub(bad_fc, good_fc, text, flags=re.DOTALL)

# 2. Put goToPhase somewhere valid (e.g. inside the day modal script)
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
if 'goToPhase' not in text:
    text = text.replace('function closeDayModal()', gotophase_fn + '\nfunction closeDayModal()')


# 3. Fix the syntax error in renderTable
bad_render_end = r"""                tbody\.appendChild\(row\);
             \}\);
          \}
        \}\);
      \}
  
    function updateStatus\(id, newStatus\) \{"""

good_render_end = r"""                tbody.appendChild(row);
             });
          }
      }
  
    function updateStatus(id, newStatus) {"""

text = re.sub(bad_render_end, good_render_end, text, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed syntax errors!")