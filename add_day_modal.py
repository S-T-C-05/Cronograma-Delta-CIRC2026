import re

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Day Modal HTML before the ending </body> tag
day_modal_html = """
<!-- DAY MODAL -->
<div id="dayModal" class="modal-overlay">
  <div class="modal-content" style="max-height: 80vh; display: flex; flex-direction: column;">
    <div class="modal-header">
      <h3 id="dayModalTitle">Eventos del Día</h3>
      <button class="close-btn" onclick="closeDayModal()">&times;</button>
    </div>
    <div class="modal-body" id="dayModalBody" style="overflow-y: auto; padding-top: 10px;">
      <!-- Content populated dynamically -->
    </div>
  </div>
</div>

<script>
function closeDayModal() {
  document.getElementById('dayModal').classList.remove('active');
}
function openDayModal(dateStr, htmlContent) {
  // Format date loosely (e.g. 2026-04-23 -> 23 Abr 2026)
  const d = new Date(dateStr + 'T00:00:00');
  const dStr = d.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  
  document.getElementById('dayModalTitle').innerText = dStr.charAt(0).toUpperCase() + dStr.slice(1);
  
  const body = document.getElementById('dayModalBody');
  if (!htmlContent) {
     body.innerHTML = '<div style="color: #6c757d; text-align: center; padding: 20px;">No hay eventos registrados en este día.</div>';
  } else {
     body.innerHTML = htmlContent;
  }
  
  document.getElementById('dayModal').classList.add('active');
}
document.getElementById('dayModal').addEventListener('click', function(e) {
  if (e.target === this) closeDayModal();
});
</script>
"""

if '<!-- DAY MODAL -->' not in text:
    text = text.replace('<!-- MODAL ENTREGABLES -->', day_modal_html + '\n<!-- MODAL ENTREGABLES -->')

# 2. Update Calendar config to include dateClick
# I will supply the hardcoded phases array inside dateClick, and get deliverables from localStorage
calendar_config_new = r"""
      var calendarEl = document.getElementById('calendar');
      
      const rawPhases = [
         { title: 'Chasis Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--chasis-color)' },
         { title: 'Chasis Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--chasis-color)' },
         { title: 'Chasis Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--chasis-color)' },
         { title: 'Chasis Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--chasis-color)' },
         { title: 'Chasis Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--chasis-color)' },
         { title: 'Chasis Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--chasis-color)' },
         
         { title: 'Brazo Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--brazo-color)' },
         { title: 'Brazo Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--brazo-color)' },
         { title: 'Brazo Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--brazo-color)' },
         { title: 'Brazo Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--brazo-color)' },
         { title: 'Brazo Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--brazo-color)' },
         { title: 'Brazo Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--brazo-color)' },

         { title: 'mROS Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--microros-color)' },
         { title: 'mROS Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--microros-color)' },
         { title: 'mROS Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--microros-color)' },
         { title: 'mROS Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--microros-color)' },
         { title: 'mROS Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--microros-color)' },
         { title: 'mROS Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--microros-color)' },

         { title: '🏆 Competencia CIRC', start: '2026-08-01', end: '2026-08-08', color: '#dc3545' }
      ];

      var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        initialDate: '2026-04-23',
        locale: 'es',
        firstDay: 1,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,multiMonthYear'
        },
        buttonText: { today: 'Hoy', month: 'Mensual', year: 'Anual' },
        
        // Custom Render for Phases and Deliverables
        eventContent: function(arg) {
           const props = arg.event.extendedProps;
           // UI for Deliverables (dot + truncated short text)
           if (props.type === 'deliverable') {
              return { html: `<div class="fc-event-deliv" title="Ver entregable: ${arg.event.extendedProps.rawName}"><div class="fc-deliv-dot" style="background:${arg.event.backgroundColor}"></div>${arg.event.title}</div>` };
           }
        },
        
        // CLICK ON DAY CELLS
        dateClick: function(info) {
           const clickedDateStr = info.dateStr;
           const clickedTimestamp = new Date(clickedDateStr + 'T00:00:00').getTime();
           let htmlContent = '';
           
           // 1. Encontrar Fases activas en esta fecha
           let activePhases = rawPhases.filter(p => {
              const s = new Date(p.start + 'T00:00:00').getTime();
              const e = new Date(p.end + 'T00:00:00').getTime();
              // La fase incluye un rango (excluimos el fin exacto o no, tradicionalmente el end en FC es exclusivo)
              return clickedTimestamp >= s && clickedTimestamp < e;
           });
           
           if(activePhases.length > 0) {
              htmlContent += '<h4 style="margin-top:0; font-size:15px; color:#495057; border-bottom: 2px solid #e9ecef; padding-bottom:5px;">Fases en Curso</h4>';
              activePhases.forEach(p => {
                 htmlContent += `<div style="background: ${p.color}; color: white; padding: 6px 12px; margin-bottom: 6px; border-radius: 6px; font-weight: 600; font-size: 14px;">${p.title}</div>`;
              });
           }
           
           // 2. Encontrar Entregables en esta fecha
           const currentDeliverables = JSON.parse(localStorage.getItem('circ_deliverables')) || initialDeliverables;
           let activeDelivs = currentDeliverables.filter(d => d.date === clickedDateStr);
           
           if(activeDelivs.length > 0) {
              htmlContent += '<h4 style="margin-top:15px; font-size:15px; color:#495057; border-bottom: 2px solid #e9ecef; padding-bottom:5px;">Entregables Pendientes / Vencidos</h4>';
              activeDelivs.forEach(d => {
                 let badgeClr = d.status === 'en-proceso' ? '#ffc107' : (d.status === 'finalizado' ? '#198754' : '#dc3545');
                 htmlContent += `
                   <div style="border: 1px solid #dee2e6; padding: 10px; border-radius: 8px; margin-bottom: 8px; cursor: pointer; transition: background 0.2s;" 
                        onmouseover="this.style.backgroundColor='#f8f9fa'" 
                        onmouseout="this.style.backgroundColor='white'"
                        onclick="closeDayModal(); openModal('Detalles del Entregable', '', '${d.name.replace(/'/g, "\\'")}', '${d.responsible}', '${d.status}');" >
                     <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                        <div style="width: 12px; height: 12px; border-radius: 50%; background: ${badgeClr};"></div>
                        <strong style="color: #212529;">${d.name}</strong>
                     </div>
                     <div style="font-size: 13px; color: #6c757d; margin-left: 20px;">Responsable: ${d.responsible}</div>
                   </div>
                 `;
              });
           }
           
           openDayModal(clickedDateStr, htmlContent);
        },

        // EVENT CLICK ROUTING
        eventClick: function(info) {
           const props = info.event.extendedProps;
           // If user clicks a Deliverable event in the calendar directly
           if (props.type === 'deliverable') {
              openModal(
                 "Detalles del Entregable", 
                 props.project, 
                 props.rawName, 
                 props.responsible, 
                 props.status
              );
           }
        },

        events: function(info, successCallback, failureCallback) {
          let allEvents = [];
          
          // INYECTAR SOLO ENTREGABLES (PUNTOS)
          const currentDeliverables = JSON.parse(localStorage.getItem('circ_deliverables')) || initialDeliverables;
          currentDeliverables.forEach(d => {
             // Colored dot indicator
             let clr = '#ffc107'; // en-proceso
             if(d.status === 'finalizado') clr = '#198754';
             if(d.status === 'no-finalizado') clr = '#dc3545';
             
             let projectName = "Hito General";
             let rawName = d.name;
             
             // Extract bracket tags
             const match = d.name.match(/^\[(.*?)\]\\s*(.*)$/);
             if (match) {
                 projectName = match[1];
                 rawName = match[2];
             } else if (d.name.includes("Chasis")) projectName = "Chasis";
             else if (d.name.includes("Brazo")) projectName = "Brazo Robótico";
             else if (d.name.includes("Telecomms") || d.name.includes("PCB") || d.name.includes("telecomms")) projectName = "Integración Múltiple";

             // Very short title for clean view
             let shortTitle = rawName.length > 25 ? rawName.substring(0, 22) + '...' : rawName;
             
             allEvents.push({
                title: shortTitle,
                start: d.date,
                allDay: true,
                backgroundColor: clr,
                extendedProps: {
                    type: 'deliverable',
                    project: projectName,
                    rawName: rawName,
                    responsible: d.responsible,
                    status: d.status
                }
             });
          });

          successCallback(allEvents);
        }
      });
      calendar.render();
      window.circCalendar = calendar;
"""

pattern = re.compile(r'var calendarEl = document\.getElementById\(\'calendar\'\);.*?window\.circCalendar = calendar;', re.DOTALL)
text = pattern.sub(calendar_config_new, text)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Added Day Click to reveal phases + deliverables dynamically!")
