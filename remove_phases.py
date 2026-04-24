import re

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

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
           // UI for Deliverables (dot + truncated short text)
           if (props.type === 'deliverable') {
              return { html: `<div class="fc-event-deliv" title="Ver entregable: ${arg.event.extendedProps.rawName}"><div class="fc-deliv-dot" style="background:${arg.event.backgroundColor}"></div>${arg.event.title}</div>` };
           }
        },
        
        // EVENT CLICK ROUTING
        eventClick: function(info) {
           const props = info.event.extendedProps;
           // If user clicks a Deliverable, Open Modal
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

pattern = re.compile(r'var calendarEl = document\.getElementById\(\'calendar\'\);.*?window\.circCalendar = calendar;', re.DOTALL)
text = pattern.sub(calendar_config_new, text)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed continuous lines. Only deliverables are shown.")
