import re

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS injection
css_addons = '''
  /* --- STATUS BADGES & CONTROLS --- */
  .status-select { 
    padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;
    border: 1px solid transparent; cursor: pointer; outline: none; appearance: none;
    transition: all 0.2s; 
  }
  .status-en-proceso { background-color: #fff3cd; color: #856404; border-color: #ffeeba; }
  .status-finalizado { background-color: #d1e7dd; color: #155724; border-color: #c3e6cb; }
  .status-no-finalizado { background-color: #f8d7da; color: #721c24; border-color: #f5c6cb; }
  
  .date-input {
    padding: 6px; border: 1px solid var(--border-color); border-radius: 6px;
    font-size: 13px; color: var(--text-main); font-family: inherit; width: 130px;
    background: #f8f9fa;
  }
  .date-input:focus { border-color: var(--primary); background: #fff; outline: none; }
  
  .highlight-row { border-left: 4px solid var(--primary) !important; background-color: rgba(13, 110, 253, 0.02) !important; }
  .important-icon { color: var(--primary); margin-right: 5px; }

  /* Notification Toast */
  .toast {
    position: fixed; bottom: 20px; right: 20px; background: #333; color: #fff;
    padding: 12px 24px; border-radius: 8px; font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    opacity: 0; transform: translateY(20px); transition: all 0.3s; pointer-events: none; z-index: 1000;
  }
  .toast.show { opacity: 1; transform: translateY(0); }
'''

content = content.replace('/* --- TABS --- */', css_addons + '\n  /* --- TABS --- */')

# We'll replace the static "Seguimiento de Entregables" table with a JS generated dynamic one
part1, part2 = content.split('<!-- PESTAÑA SEGUIMIENTO DE ENTREGABLES -->', 1)

tracking_section = '''<!-- PESTAÑA SEGUIMIENTO DE ENTREGABLES -->
    <div id="entregables" class="tab-content">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h2>Seguimiento de Entregables</h2>
        <button class="fc-button-primary" style="border:none; padding: 8px 16px; border-radius: 8px; cursor:pointer;" onclick="resetDeliverables()">Resetear Cambios</button>
      </div>
      
      <table id="deliverablesTable">
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
      </table>
    </div>
  </div>
'''

new_scripts = '''
  <div id="toast" class="toast">Cronograma actualizado!</div>

  <script>
    // ESTADO INICIAL
    const initialDeliverables = [
      { id: 'd1', name: "Prueba + capacitación telecomms", responsible: "Luis y Gerardo", date: "2026-05-17", status: "en-proceso", important: false },
      { id: 'd2', name: "Chasis funcional", responsible: "Milton y Said", date: "2026-05-31", status: "en-proceso", important: true },
      { id: 'd3', name: "Simulación funcional del brazo", responsible: "Angel y Raul", date: "2026-05-31", status: "en-proceso", important: false },
      { id: 'd4', name: "Chasis funcional + PCB + sensores", responsible: "Milton, Said, Luis", date: "2026-07-05", status: "en-proceso", important: true },
      { id: 'd5', name: "Brazo funcional + PCB", responsible: "Angel, Raul, Gerardo", date: "2026-07-19", status: "en-proceso", important: true }
    ];

    let deliverables = JSON.parse(localStorage.getItem('circ_deliverables')) || initialDeliverables;

    function renderTable() {
      const tbody = document.getElementById('deliverablesBody');
      tbody.innerHTML = '';
      
      deliverables.forEach((item, index) => {
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

    function updateStatus(id, newStatus) {
      const item = deliverables.find(d => d.id === id);
      if(item) {
        item.status = newStatus;
        saveAndReload();
      }
    }

    function updateDate(id, newDate) {
      if(!newDate) return;
      const item = deliverables.find(d => d.id === id);
      if(item) {
        item.date = newDate;
        item.status = 'en-proceso'; // Vuelve a estar en proceso si se reprograma
        showToast('Fecha reprogramada. El calendario se ha actualizado.');
        saveAndReload();
      }
    }

    function saveAndReload() {
      localStorage.setItem('circ_deliverables', JSON.stringify(deliverables));
      renderTable();
      updateCalendarEvents(); // Actualizar FullCalendar
    }

    function resetDeliverables() {
      if(confirm('¿Estás seguro de que deseas resetear los entregables a su estado original?')) {
        deliverables = JSON.parse(JSON.stringify(initialDeliverables));
        saveAndReload();
        showToast('Entregables reseteados al plan original.');
      }
    }

    function formatDate(dateStr) {
      const options = { day: 'numeric', month: 'short', year: 'numeric' };
      return new Date(dateStr + 'T00:00:00').toLocaleDateString('es-ES', options);
    }
    
    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3000);
    }

    // Funcionalidad de pestañas
    function openTab(tabId, btn) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      
      document.getElementById(tabId).classList.add('active');
      btn.classList.add('active');
      
      if (tabId === 'calendario') {
         setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderTable();
    });
  </script>
</body>
</html>
'''

# We also need to modify the FullCalendar scripts to merge `rawEvents` with `deliverables`
content = part1 + tracking_section + new_scripts

# Find the initialization of Fullcalendar and inject dynamic update logic
calendar_injection = '''
        events: function(info, successCallback, failureCallback) {
          const rawEvents = [
            // CHASIS
            { title: '[Chasis] Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--chasis-color)' },
            { title: '[Chasis] Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--chasis-color)' },
            { title: '[Chasis] Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--chasis-color)' },
            { title: '[Chasis] Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--chasis-color)' },
            { title: '[Chasis] Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--chasis-color)' },
            { title: '[Chasis] Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--chasis-color)' },
            
            // BRAZO
            { title: '[Brazo] Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--brazo-color)' },
            { title: '[Brazo] Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--brazo-color)' },
            { title: '[Brazo] Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--brazo-color)' },
            { title: '[Brazo] Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--brazo-color)' },
            { title: '[Brazo] Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--brazo-color)' },
            { title: '[Brazo] Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--brazo-color)' },

            // MICRO-ROS
            { title: '[mROS] Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--microros-color)' },
            { title: '[mROS] Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--microros-color)' },
            { title: '[mROS] Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--microros-color)' },
            { title: '[mROS] Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--microros-color)' },
            { title: '[mROS] Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--microros-color)' },
            { title: '[mROS] Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--microros-color)' },

            // EVENTO DE COMPETENCIA
            { title: '🏆 COMPETENCIA CIRC (Utah)', start: '2026-08-01', end: '2026-08-08', color: '#dc3545' }
          ];

          let expandedEvents = [];
          rawEvents.forEach(function(evt) {
              let currentStr = evt.start;
              let endStr = evt.end;
              let current = new Date(currentStr + 'T00:00:00');
              let end = new Date(endStr + 'T00:00:00');

              while(current < end) {
                  let yyyy = current.getFullYear();
                  let mm = String(current.getMonth() + 1).padStart(2, '0');
                  let dd = String(current.getDate()).padStart(2, '0');
                  expandedEvents.push({
                      title: evt.title,
                      start: yyyy + '-' + mm + '-' + dd,
                      color: evt.color,
                      allDay: true
                  });
                  current.setDate(current.getDate() + 1);
              }
          });
          
          // INYECTAR ENTREGABLES DINAMICOS DESDE LOCALSTORAGE
          const currentDeliverables = JSON.parse(localStorage.getItem('circ_deliverables')) || initialDeliverables;
          currentDeliverables.forEach(d => {
             let clr = '#ffc107'; // en-proceso
             if(d.status === 'finalizado') clr = '#198754';
             if(d.status === 'no-finalizado') clr = '#dc3545';
             expandedEvents.push({
                title: '📍 Entregable: ' + d.name,
                start: d.date,
                color: clr, // color depends on status
                allDay: true
             });
          });

          successCallback(expandedEvents);
        }
      });
      calendar.render();
      
      // Store in global window so we can refetch easily
      window.circCalendar = calendar;
    });

    function updateCalendarEvents() {
        if(window.circCalendar) {
            window.circCalendar.refetchEvents();
        }
    }
  </script>
'''

# Now, we do string replacement in content for the calendar script
import re
content = re.sub(r'events:\s*function.*?}\s*}\);\s*calendar\.render\(\);\s*\}\);', calendar_injection, content, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("HTML successfully rewriten.")
