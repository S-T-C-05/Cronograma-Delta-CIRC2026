import re

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add CSS for Calendar Events & Modal
css_addons = """
  /* --- MODAL --- */
  .modal-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.5); display: none; align-items: center; justify-content: center;
    z-index: 2000; opacity: 0; transition: opacity 0.3s;
  }
  .modal-overlay.active { display: flex; opacity: 1; }
  .modal-content {
    background: #ffffff; width: 90%; max-width: 500px; border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden;
    transform: translateY(-20px); transition: transform 0.3s;
  }
  .modal-overlay.active .modal-content { transform: translateY(0); }
  .modal-header {
    padding: 16px 20px; border-bottom: 1px solid var(--border-color);
    display: flex; justify-content: space-between; align-items: center;
    background: #f8f9fa;
  }
  .modal-header h3 { margin: 0; font-size: 1.2rem; color: var(--text-main); font-weight: 700; }
  .close-btn { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--text-muted); line-height: 1; }
  .close-btn:hover { color: #dc3545; }
  .modal-body { padding: 20px; font-size: 14.5px; line-height: 1.8; color: #495057; }
  .status-badge { padding: 4px 12px; border-radius: 12px; font-weight: 700; font-size: 13px; display: inline-block; margin-top: 5px; }
  
  /* --- CUSTOM FC EVENTS VIEW --- */
  .fc-event-phase {
    background-color: var(--fc-bg-color); color: #fff; padding: 2px; font-size: 11px; border-radius: 4px;
    opacity: 0.8 !important; transition: opacity 0.2s; text-align: center; border: none; cursor: pointer;
  }
  .fc-event-phase:hover { opacity: 1 !important; transform: scale(1.01); }
  
  .fc-event-deliv {
    display: flex; align-items: center; gap: 6px; padding: 3px 8px; margin: 2px 0;
    background-color: #fff; border: 1px solid #ced4da; border-radius: 16px;
    color: #495057; font-size: 11.5px; font-weight: 600; cursor: pointer;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04); transition: all 0.2s;
    overflow: hidden; white-space: nowrap; text-overflow: ellipsis;
  }
  .fc-event-deliv:hover {
    transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-color: #adb5bd; z-index: 10;
  }
  .fc-deliv-dot { width: 9px; height: 9px; border-radius: 50%; border: 1px solid rgba(0,0,0,0.1); flex-shrink: 0; }
  
  /* Make sure background calendar events do not overflow cells unpleasantly */
  .fc-daygrid-event-harness { z-index: 1; }
"""

if '/* --- MODAL --- */' not in text:
    text = text.replace('/* --- TABS --- */', css_addons + '\n  /* --- TABS --- */')

# 2. Add Modal HTML before </body>
modal_html = """
<!-- MODAL ENTREGABLES -->
<div id="delivModal" class="modal-overlay">
  <div class="modal-content">
    <div class="modal-header">
      <h3 id="modalTitle">Detalle</h3>
      <button class="close-btn" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body">
      <div style="margin-bottom: 12px; font-size: 16px;"><strong>Proyecto:</strong> <span id="modalProject" style="color: var(--primary); font-weight: 700;"></span></div>
      <div style="margin-bottom: 12px; font-size: 15px;"><strong>Entregable / Hito:</strong> <span id="modalDesc"></span></div>
      <div style="margin-bottom: 12px;"><strong>Responsables:</strong> <span id="modalResp"></span></div>
      <div style="margin-top: 15px;"><strong>Estado:</strong> <br>
      <span id="modalStatusBadge" class="status-badge"></span></div>
    </div>
  </div>
</div>

<script>
function closeModal() {
  document.getElementById('delivModal').classList.remove('active');
}
function openModal(title, project, desc, resp, status) {
  document.getElementById('modalTitle').innerText = title;
  document.getElementById('modalProject').innerText = project;
  document.getElementById('modalDesc').innerText = desc;
  document.getElementById('modalResp').innerText = resp;
  
  const badge = document.getElementById('modalStatusBadge');
  badge.innerText = status === 'en-proceso' ? 'En Proceso' : (status === 'finalizado' ? 'Finalizado' : 'No Finalizado');
  
  // Custom Badge Look
  badge.style.backgroundColor = status === 'en-proceso' ? '#fff3cd' : (status === 'finalizado' ? '#d1e7dd' : '#f8d7da');
  badge.style.color = status === 'en-proceso' ? '#856404' : (status === 'finalizado' ? '#155724' : '#721c24');
  badge.style.border = '1px solid ' + (status === 'en-proceso' ? '#ffeeba' : (status === 'finalizado' ? '#c3e6cb' : '#f5c6cb'));
  
  document.getElementById('delivModal').classList.add('active');
}

// Cerrar modal al clickear afuera del contenido
document.getElementById('delivModal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});
</script>
"""

if '<!-- MODAL ENTREGABLES -->' not in text:
    text = text.replace('</body>', modal_html + '\n</body>')

# 3. Rewrite Calendar Initialization
calendar_config_new = r"""
      var calendarEl = document.getElementById('calendar');
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
           // UI for long running Phase
           if (props.type === 'phase') {
              return { html: `<div class="fc-event-phase" style="--fc-bg-color: ${arg.event.backgroundColor}" title="Ir a descripción de ${arg.event.title}">${arg.event.title}</div>` };
           } 
           // UI for Deliverables (dot + truncated short text)
           else if (props.type === 'deliverable') {
              return { html: `<div class="fc-event-deliv" title="Ver entregable: ${arg.event.extendedProps.rawName}"><div class="fc-deliv-dot" style="background:${arg.event.backgroundColor}"></div>${arg.event.title}</div>` };
           }
        },
        
        // EVENT CLICK ROUTING
        eventClick: function(info) {
           const props = info.event.extendedProps;
           // If user clicks a Phase, Navigate to it precisely.
           if (props.type === 'phase') {
              // open TAB Description
              const tabBtn = document.querySelector('button[onclick*="descripcion"]');
              if (tabBtn) openTab('descripcion', tabBtn);
              
              // Scroll to the specific project phase title
              setTimeout(() => {
                 const target = document.querySelector('.' + props.targetId);
                 if(target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    // Highlight flash effect
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
           // If user clicks a Deliverable, Open Modal
           else if (props.type === 'deliverable') {
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
          // BACKGROUND CONTINOUS PHASES
          const rawPhases = [
            { title: 'Chasis Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--chasis-color)', extendedProps: {type: 'phase', targetId: 'chasis-title'} },
            { title: 'Chasis Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--chasis-color)', extendedProps: {type: 'phase', targetId: 'chasis-title'} },
            { title: 'Chasis Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--chasis-color)', extendedProps: {type: 'phase', targetId: 'chasis-title'} },
            { title: 'Chasis Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--chasis-color)', extendedProps: {type: 'phase', targetId: 'chasis-title'} },
            { title: 'Chasis Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--chasis-color)', extendedProps: {type: 'phase', targetId: 'chasis-title'} },
            { title: 'Chasis Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--chasis-color)', extendedProps: {type: 'phase', targetId: 'chasis-title'} },
            
            { title: 'Brazo Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--brazo-color)', extendedProps: {type: 'phase', targetId: 'brazo-title'} },
            { title: 'Brazo Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--brazo-color)', extendedProps: {type: 'phase', targetId: 'brazo-title'} },
            { title: 'Brazo Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--brazo-color)', extendedProps: {type: 'phase', targetId: 'brazo-title'} },
            { title: 'Brazo Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--brazo-color)', extendedProps: {type: 'phase', targetId: 'brazo-title'} },
            { title: 'Brazo Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--brazo-color)', extendedProps: {type: 'phase', targetId: 'brazo-title'} },
            { title: 'Brazo Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--brazo-color)', extendedProps: {type: 'phase', targetId: 'brazo-title'} },

            { title: 'mROS Fase 1', start: '2026-04-23', end: '2026-05-07', color: 'var(--microros-color)', extendedProps: {type: 'phase', targetId: 'microros-title'} },
            { title: 'mROS Fase 2', start: '2026-05-07', end: '2026-05-21', color: 'var(--microros-color)', extendedProps: {type: 'phase', targetId: 'microros-title'} },
            { title: 'mROS Fase 3', start: '2026-05-21', end: '2026-06-11', color: 'var(--microros-color)', extendedProps: {type: 'phase', targetId: 'microros-title'} },
            { title: 'mROS Fase 4', start: '2026-06-11', end: '2026-07-01', color: 'var(--microros-color)', extendedProps: {type: 'phase', targetId: 'microros-title'} },
            { title: 'mROS Fase 5', start: '2026-07-01', end: '2026-07-16', color: 'var(--microros-color)', extendedProps: {type: 'phase', targetId: 'microros-title'} },
            { title: 'mROS Fase 6', start: '2026-07-16', end: '2026-08-01', color: 'var(--microros-color)', extendedProps: {type: 'phase', targetId: 'microros-title'} },

            { title: '🏆 Competencia CIRC', start: '2026-08-01', end: '2026-08-08', color: '#dc3545', extendedProps: {type: 'phase', targetId: 'chasis-title'} }
          ];

          let allEvents = [...rawPhases];
          
          // INYECTAR ENTREGABLES DINAMICOS COMO OBJETOS PIN-PUNTUALES
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

import re
# We parse from "var calendarEl =" to "window.circCalendar = calendar;" 
# which was created during the last prompt logic
pattern = re.compile(r'var calendarEl = document\.getElementById\(\'calendar\'\);.*?window\.circCalendar = calendar;', re.DOTALL)
text = pattern.sub(calendar_config_new, text)

# Limpiar restos por si acaso había configs repetidas (la anterior tenía rawEvents.forEach)
text = re.sub(r'const rawEvents = \[.*?\];.*?successCallback\(expandedEvents\);', '', text, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied UI Calendar features and interactions.")
