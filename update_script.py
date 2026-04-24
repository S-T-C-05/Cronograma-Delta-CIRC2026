import re

with open('Cronograma.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_tabs = '''
  /* --- TABS --- */
  .tab-container { margin-top: 2rem; }
  .tab-buttons { display: flex; border-bottom: 2px solid var(--border-color); margin-bottom: 1.5rem; gap: 0.5rem; flex-wrap: wrap; }
  .tab-btn { 
    background: none; border: none; padding: 12px 24px; font-size: 16px; 
    font-weight: 600; color: var(--text-muted); cursor: pointer;
    border-bottom: 3px solid transparent; margin-bottom: -2px; transition: all 0.3s;
  }
  .tab-btn:hover { color: var(--primary); }
  .tab-btn.active { color: var(--primary); border-bottom-color: var(--primary); }
  .tab-content { display: none; margin-top: 1rem; }
  .tab-content.active { display: block; padding-bottom: 3rem; }
  .responsible-badge { font-size: 15px; color: var(--text-muted); font-weight: normal; margin-left: 10px; }
'''
content = content.replace('</style>', css_tabs + '\n</style>')

part1, part2 = content.split('<div id="calendar"></div>', 1)

new_structure = '''
  <div class="tab-container">
    <div class="tab-buttons">
      <button class="tab-btn active" onclick="openTab('calendario', this)">Calendario</button>
      <button class="tab-btn" onclick="openTab('descripcion', this)">Descripción de los proyectos</button>
      <button class="tab-btn" onclick="openTab('entregables', this)">Seguimiento de entregables</button>
    </div>

    <!-- PESTAÑA CALENDARIO -->
    <div id="calendario" class="tab-content active">
      <div id="calendar"></div>
'''

part2_script, part2_tables = part2.split('</script>', 1)

new_structure += part2_script + '''
      <!-- Fix para el renderizado del calendario al cambiar de pestaña -->
      <script>
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => window.dispatchEvent(new Event('resize')), 100);
        });
      </script>
    </div>

    <!-- PESTAÑA DESCRIPCION DE PROYECTOS -->
    <div id="descripcion" class="tab-content">
'''

part2_tables = part2_tables.replace('<h2 class="chasis-title">1. Proyecto: Chasis</h2>', 
  '<h2 class="chasis-title">1. Proyecto: Chasis <span class="responsible-badge">(Responsables: Milton y Said)</span></h2>')
part2_tables = part2_tables.replace('<h2 class="brazo-title">2. Proyecto: Brazo Robótico</h2>',
  '<h2 class="brazo-title">2. Proyecto: Brazo Robótico <span class="responsible-badge">(Responsables: Angel y Raul)</span></h2>')
part2_tables = part2_tables.replace('<h2 class="microros-title">3. Proyecto: micro-ROS + STM32</h2>',
  '<h2 class="microros-title">3. Proyecto: micro-ROS + STM32 <span class="responsible-badge">(Responsables: Luis y Gerardo)</span></h2>')

# Quitamos cierre del body html para inyectar tabs
idx = part2_tables.rfind('</div>')
part2_tables = part2_tables[:idx]

new_structure += part2_tables + '''
    </div>

    <!-- PESTAÑA SEGUIMIENTO DE ENTREGABLES -->
    <div id="entregables" class="tab-content">
      <h2 style="margin-bottom: 2rem;">Seguimiento de Entregables</h2>
      <table>
        <thead>
          <tr>
            <th style="width: 20%;">Semana / Fechas</th>
            <th style="width: 45%;">Actividad / Hito</th>
            <th style="width: 35%;">Detalles</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Semana 3</strong><br><span style="color: var(--text-muted)">17 May – 23 May</span></td>
            <td>Prueba + capacitación de telecomms</td>
            <td><ul><li>Control de Xbox</li><li>Integración de IMU</li></ul></td>
          </tr>
          <tr>
            <td rowspan="2" style="vertical-align: middle;"><strong>Semana 5</strong><br><span style="color: var(--text-muted)">31 May – 6 Jun</span></td>
            <td>Chasis funcional</td>
            <td></td>
          </tr>
          <tr>
            <td>Simulación funcional del brazo</td>
            <td></td>
          </tr>
          <tr>
            <td><strong>Semana 10</strong><br><span style="color: var(--text-muted)">5 Jul – 11 Jul</span></td>
            <td>Chasis funcional + PCB + sensores</td>
            <td></td>
          </tr>
          <tr>
            <td><strong>Semana 12</strong><br><span style="color: var(--text-muted)">19 Jul – 25 Jul</span></td>
            <td>Brazo funcional + PCB</td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <script>
    function openTab(tabId, btn) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      
      document.getElementById(tabId).classList.add('active');
      btn.classList.add('active');
      
      if (tabId === 'calendario') {
         setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
      }
    }
  </script>

</div>
</body>
</html>
'''

final_content = part1 + new_structure

with open('Cronograma.html', 'w', encoding='utf-8') as f:
    f.write(final_content)
    
print("Cronograma.html has been updated successfully.")