import re

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

# --- PART 1: UPDATE DAY MODAL TO NAVIGATE TO PHASE ---
# 1.1 First, add targetId to rawPhases
raw_phases_replacement = r"""const rawPhases = [
         { title: 'Chasis Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--chasis-color)', targetId: 'chasis-title' },
         { title: 'Chasis Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--chasis-color)', targetId: 'chasis-title' },
         { title: 'Chasis Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--chasis-color)', targetId: 'chasis-title' },
         { title: 'Chasis Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--chasis-color)', targetId: 'chasis-title' },
         { title: 'Chasis Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--chasis-color)', targetId: 'chasis-title' },
         { title: 'Chasis Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--chasis-color)', targetId: 'chasis-title' },
         
         { title: 'Brazo Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--brazo-color)', targetId: 'brazo-title' },
         { title: 'Brazo Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--brazo-color)', targetId: 'brazo-title' },
         { title: 'Brazo Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--brazo-color)', targetId: 'brazo-title' },
         { title: 'Brazo Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--brazo-color)', targetId: 'brazo-title' },
         { title: 'Brazo Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--brazo-color)', targetId: 'brazo-title' },
         { title: 'Brazo Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--brazo-color)', targetId: 'brazo-title' },

         { title: 'mROS Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--microros-color)', targetId: 'microros-title' },
         { title: 'mROS Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--microros-color)', targetId: 'microros-title' },
         { title: 'mROS Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--microros-color)', targetId: 'microros-title' },
         { title: 'mROS Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--microros-color)', targetId: 'microros-title' },
         { title: 'mROS Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--microros-color)', targetId: 'microros-title' },
         { title: 'mROS Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--microros-color)', targetId: 'microros-title' },

         { title: '🏆 Competencia CIRC', start: '2026-08-01', end: '2026-08-08', color: '#dc3545', targetId: 'chasis-title' }
      ];"""
      
text = re.sub(r'const rawPhases = \[.*?\];', raw_phases_replacement, text, flags=re.DOTALL)

# 1.2 Modify activePhases.forEach rendering
phase_rendering_old = r"""activePhases\.forEach\(p => \{.*?htmlContent \+= `<div style="background: \$\{p\.color\}; color: white; padding: 6px 12px; margin-bottom: 6px; border-radius: 6px; font-weight: 600; font-size: 14px;">\$\{p\.title\}</div>`;.*?\}\);"""
phase_rendering_new = r"""
              activePhases.forEach(p => {
                 htmlContent += `<div onclick="closeDayModal(); goToPhase('${p.targetId}')" style="background: ${p.color}; color: white; padding: 6px 12px; margin-bottom: 6px; border-radius: 6px; font-weight: 600; font-size: 14px; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'" title="Ir a la descripción de esta fase">${p.title}</div>`;
              });
"""

text = re.sub(phase_rendering_old, phase_rendering_new.strip(), text, flags=re.DOTALL)

# 1.3 Add goToPhase function if not exists
goto_phase_script = """
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
</script>"""

text = text.replace('</script>', goto_phase_script + '\n<script>', 1)


# --- PART 2: SPLIT DELIVERABLES INTO 3 TABLES ---
# 2.1 Update HTML structure for tables
old_table_html = """<table id="deliverablesTable">
          <thead>
            <tr>
              <th style="width: 25%;">Hito / Entregable</th>
              <th style="width: 15%;">Responsable</th>
              <th style="width: 20%;">Fecha Programada</th>
              <th style="width: 20%;">Estado</th>
              <th style="width: 20%;">Reprogramar (No Finalizado)</th>
            </tr>
          </thead>
          <tbody id="deliverablesBody">
            <!-- Renderizado dinamicamente -->
          </tbody>
        </table>"""

new_table_html = """<div id="tablesContainer">
          <!-- Renderizado dinamicamente en multiples tablas -->
        </div>"""

text = text.replace(old_table_html, new_table_html)

# 2.2 Update renderTable function
old_renderFunc = re.search(r'function renderTable\(\) \{.*?\n      \}', text, re.DOTALL).group(0)

new_renderFunc = """function renderTable() {
        const container = document.getElementById('tablesContainer');
        container.innerHTML = '';
        
        const groups = {
           "Chasis": [],
           "Brazo Robótico": [],
           "Integración Múltiple (mROS, Telecomms, PCB)": [],
           "Otros / Competencia": []
        };
        
        deliverables.forEach((item) => {
            if (/chasis/i.test(item.name)) {
                groups["Chasis"].push(item);
            } else if (/brazo/i.test(item.name)) {
                groups["Brazo Robótico"].push(item);
            } else if (/telecomms|pcb|mros/i.test(item.name)) {
                groups["Integración Múltiple (mROS, Telecomms, PCB)"].push(item);
            } else {
                groups["Otros / Competencia"].push(item);
            }
        });
        
        for(let g in groups) {
           if(groups[g].length === 0) continue;
           
           const sectionTitle = document.createElement('h3');
           sectionTitle.style.marginTop = "2.5rem";
           sectionTitle.style.marginBottom = "1rem";
           sectionTitle.style.color = "var(--primary)";
           sectionTitle.style.fontSize = "1.3rem";
           sectionTitle.style.borderBottom = "2px solid #e9ecef";
           sectionTitle.style.paddingBottom = "5px";
           sectionTitle.innerText = g;
           container.appendChild(sectionTitle);
           
           const table = document.createElement('table');
           table.id = "tabla-" + g.replace(/\s+/g, '');
           table.innerHTML = `
              <thead>
                <tr>
                  <th style="width: 25%;">Hito / Entregable</th>
                  <th style="width: 15%;">Responsable</th>
                  <th style="width: 20%;">Fecha Programada</th>
                  <th style="width: 20%;">Estado</th>
                  <th style="width: 20%;">Reprogramar</th>
                </tr>
              </thead>
              <tbody>
              </tbody>
           `;
           container.appendChild(table);
           
           const tbody = table.querySelector('tbody');
           groups[g].forEach((item) => {
              const row = document.createElement('tr');
              if (item.important) row.classList.add('highlight-row');
              
              const canReschedule = item.status === 'no-finalizado';
              
              row.innerHTML = `
                <td>${item.important ? '<span class="important-icon">★</span>' : ''}<strong>${item.name}</strong></td>
                <td>${item.responsible}</td>
                <td><strong>${formatDate(item.date)}</strong></td>
                <td>
                  <select class="status-select status-${item.status}" onchange="updateStatus('${item.id}', this.value)">
                    <option value="en-proceso" ${item.status === 'en-proceso' ? 'selected' : ''}>En Proceso</option>
                    <option value="finalizado" ${item.status === 'finalizado' ? 'selected' : ''}>Finalizado</option>
                    <option value="no-finalizado" ${item.status === 'no-finalizado' ? 'selected' : ''}>No Finalizado</option>
                  </select>
                </td>
                <td>
                  ${canReschedule ? `<input type="date" class="date-input" value="${item.date}" onchange="updateDate('${item.id}', this.value)">` : '<span style="color: #adb5bd; font-size: 13px;">N/A</span>'}
                </td>
              `;
              tbody.appendChild(row);
           });
        }
      }"""

text = text.replace(old_renderFunc, new_renderFunc)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied phase navigation and split tracking view!")
