
with open('Cronograma.html', 'r', encoding='utf-8') as f:
    text = f.read()
    
bad = "             });\n          }\n        });\n      }\n  \n    function updateStatus"
good = "             });\n          }\n      }\n  \n    function updateStatus"
text = text.replace(bad, good)

bad2 = "             });\r\n          }\r\n        });\r\n      }\r\n  \r\n    function updateStatus"
good2 = "             });\r\n          }\r\n      }\r\n  \r\n    function updateStatus"
text = text.replace(bad2, good2)

bad_fc = "<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'>\nfunction goToPhase(targetId) {\n    const tabBtn = document.querySelector('button[onclick*=\"descripcion\"]');\n    if (tabBtn) openTab('descripcion', tabBtn);\n    setTimeout(() => {\n       const target = document.querySelector('.' + targetId);\n       if(target) {\n          target.scrollIntoView({ behavior: 'smooth', block: 'start' });\n          const originalBg = target.style.backgroundColor;\n          target.style.transition = \"background 0.5s ease\";\n          target.style.backgroundColor = \"#fff3cd\";\n          target.style.borderRadius = \"8px\";\n          setTimeout(() => {\n             target.style.backgroundColor = originalBg; \n          }, 1200);\n       }\n    }, 100);\n}\n</script>\n<script>\n<style>"
good_fc = "<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>\n<style>"
text = text.replace(bad_fc, good_fc)

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

with open('Cronograma.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("done")
