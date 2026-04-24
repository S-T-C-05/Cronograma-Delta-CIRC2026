html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cronograma de Desarrollo - CIRC 2026</title>
<style>
  :root {
    --bg-page: #f8f9fa;
    --bg-card: #ffffff;
    --text-main: #333333;
    --text-muted: #6c757d;
    --border-color: #dee2e6;
    --primary: #0d6efd;
    --secondary: #6c757d;
    --chasis-color: #0dcaf0;
    --brazo-color: #6f42c1;
    --microros-color: #fd7e14;
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: var(--font-family);
    background-color: var(--bg-page);
    color: var(--text-main);
    line-height: 1.6;
    padding: 2rem;
  }
  .container {
    max-width: 1100px;
    margin: 0 auto;
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  }
  h1, h2, h3 { margin-bottom: 1rem; color: #212529; }
  h1 { border-bottom: 2px solid var(--primary); padding-bottom: 0.5rem; }
  .header-info { margin-bottom: 2rem; color: var(--text-muted); font-size: 15px; }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 3rem;
    font-size: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  th, td {
    padding: 12px 15px;
    border: 1px solid var(--border-color);
    text-align: left;
    vertical-align: top;
  }
  th { background-color: #f8f9fa; font-weight: 600; color: #495057; }
  .phase-title { font-weight: 600; color: #212529; }
  .days-badge {
    display: inline-block; padding: 2px 6px; border-radius: 4px;
    background: #e9ecef; color: #495057; font-size: 11px; font-weight: 600; margin-top: 4px;
  }
  .chasis-title { color: #088baf; border-bottom: 2px solid var(--chasis-color); display: inline-block; padding-bottom: 4px; }
  .brazo-title { color: #512e8e; border-bottom: 2px solid var(--brazo-color); display: inline-block; padding-bottom: 4px; }
  .microros-title { color: #c95e02; border-bottom: 2px solid var(--microros-color); display: inline-block; padding-bottom: 4px; }
  ul { padding-left: 18px; margin-top: 4px; }
  li { margin-bottom: 4px; }
</style>
</head>
<body>

<div class="container">
  <h1>Cronograma de Desarrollo de Software (CIRC 2026)</h1>
  <div class="header-info">
    <strong>Fecha de Partida:</strong> Hoy (23 de Abril de 2026) <br>
    <strong>Competencia:</strong> 7 de Agosto de 2026 <br>
    <strong>Duración Total:</strong> ~107 Días
  </div>

  <!-- CHASIS -->
  <h2 class="chasis-title">1. Proyecto: Chasis</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Fase / Duración</th>
        <th style="width: 15%;">Fechas</th>
        <th style="width: 40%;">Actividades Planificadas</th>
        <th style="width: 25%;">Entregables</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="phase-title">Fase 1: Fundamentos</span><br><span class="days-badge">14 Días</span></td>
        <td>23 Abr – 6 May</td>
        <td>Configuración inicial del workspace Nav2. Definición del modelo cinemático diferencial y nodos de teleoperación básicos.</td>
        <td><ul><li>Workspace ROS 2 listo.</li><li>Teleop por comandos activo.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 2: Seguridad y Control</span><br><span class="days-badge">14 Días</span></td>
        <td>7 May – 20 May</td>
        <td>Desarrollo de nodos de hardware, E-stop (parada de emergencia por software) y configuración de sensores.</td>
        <td><ul><li>Parada de emergencia operativa.</li><li>Estructura TF base del chasis.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 3: Percepción</span><br><span class="days-badge">21 Días</span></td>
        <td>21 May – 10 Jun</td>
        <td>Integración de IMU y Encoders. Fusión de odometría vía EKF.</td>
        <td><ul><li>Odometría publicando a 50Hz reales y filtrada.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 4: Inteligencia</span><br><span class="days-badge">20 Días</span></td>
        <td>11 Jun – 30 Jun</td>
        <td>Ajuste de navegación autónoma. Implementación de GPS Waypoints y tracking para la prueba de "Exploration".</td>
        <td><ul><li>Follow Waypoints integrado (Nav2).</li><li>Scripts de track autónomo.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 5: UI & Feedback</span><br><span class="days-badge">15 Días</span></td>
        <td>1 Jul – 15 Jul</td>
        <td>Dashboard de control y monitor de vibración activo (p/ Refreshment Delivery).</td>
        <td><ul><li>Foxglove web UI funcional para teleop de chasis.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 6: Pruebas (Integración)</span><br><span class="days-badge">16 Días</span></td>
        <td>16 Jul – 31 Jul</td>
        <td>Integración en entorno completo "Full Stack". Depuración y Dry-runs en terreno irregular.</td>
        <td><ul><li>chasis_launch.py libre de errores.</li><li>Bolsas de ROS comprobadas.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 7: Competencia</span><br><span class="days-badge">7 Días</span></td>
        <td>1 Ago – 7 Ago</td>
        <td>Optimización, preparación de repuestos y ajustes en Utah (CIRC).</td>
        <td><ul><li>Firmware y binarios de campo listos.</li></ul></td>
      </tr>
    </tbody>
  </table>

  <!-- BRAZO ROBÓTICO -->
  <h2 class="brazo-title">2. Proyecto: Brazo Robótico</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Fase / Duración</th>
        <th style="width: 15%;">Fechas</th>
        <th style="width: 40%;">Actividades Planificadas</th>
        <th style="width: 25%;">Entregables</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="phase-title">Fase 1: Fundamentos</span><br><span class="days-badge">14 Días</span></td>
        <td>23 Abr – 6 May</td>
        <td>Creación y validación del árbol de Joints. Configuración exhaustiva de URDF/SRDF.</td>
        <td><ul><li>Modelo visualizado y conectado en RViz sin errores.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 2: Estructura MoveIt2</span><br><span class="days-badge">14 Días</span></td>
        <td>7 May – 20 May</td>
        <td>Inicialización de MoveIt2. Conexión de ros2_control base en simulación.</td>
        <td><ul><li>Comandos simulados exitosos.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 3: Control Bajo Nivel</span><br><span class="days-badge">21 Días</span></td>
        <td>21 May – 10 Jun</td>
        <td>Implementación de TRAC-IK y validación del controlador por trayectorias cartesianas (Servo). Tuning del Gripper.</td>
        <td><ul><li>Brazo controlable por Joystick con latencia mínima.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 4: Misiones Especificas</span><br><span class="days-badge">20 Días</span></td>
        <td>11 Jun – 30 Jun</td>
        <td>Programación de Poses repetitivas (RoverCooked) y Morse Sender en el End-Effector (Heist).</td>
        <td><ul><li>Action Server de rutinas. Librería YAML configurada.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 5: UI & Feedback</span><br><span class="days-badge">15 Días</span></td>
        <td>1 Jul – 15 Jul</td>
        <td>Feedback de Torque del Gripper al Dashboard. Switch en vivo entre modo "Servo" a "Waypoints".</td>
        <td><ul><li>Módulo brazo en UI Foxglove y alertas de colisión/torque.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 6: Pruebas (Integración)</span><br><span class="days-badge">16 Días</span></td>
        <td>16 Jul – 31 Jul</td>
        <td>Manipulación de objetos del mundo real (botellas, rocas calibradas, teclados).</td>
        <td><ul><li>Tareas "Heist" y "RoverCooked" demostradas.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 7: Competencia</span><br><span class="days-badge">7 Días</span></td>
        <td>1 Ago – 7 Ago</td>
        <td>Calibración fina in-situ de límites IK y Torque.</td>
        <td><ul><li>Operación final en evento.</li></ul></td>
      </tr>
    </tbody>
  </table>

  <!-- MICRO-ROS + STM32 -->
  <h2 class="microros-title">3. Proyecto: micro-ROS + STM32</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Fase / Duración</th>
        <th style="width: 15%;">Fechas</th>
        <th style="width: 40%;">Actividades Planificadas</th>
        <th style="width: 25%;">Entregables</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="phase-title">Fase 1: Fundamentos</span><br><span class="days-badge">14 Días</span></td>
        <td>23 Abr – 6 May</td>
        <td>Setup e inicialización de STM32CubeMX, FreeRTOS y librerías estáticas de micro-ROS. Config. UART/USB.</td>
        <td><ul><li>Hardware con SO en tiempo real funcionando. Ping PC.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 2: Hardware & Seguridad</span><br><span class="days-badge">14 Días</span></td>
        <td>7 May – 20 May</td>
        <td>Estructuración y prioridades de FreeRTOS. Integrar interrupciones por E-stop.</td>
        <td><ul><li>Firmware responsivo < 10ms a freno de emergencia.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 3: Control PID</span><br><span class="days-badge">21 Días</span></td>
        <td>21 May – 10 Jun</td>
        <td>Desarrollo de cálculo PID por interrupción de timer. Asignación total de Publishers / Subscribers.</td>
        <td><ul><li>Lazo cerrado de velocidad estabilizado desde PC con PWM real.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 4: Telemetría</span><br><span class="days-badge">20 Días</span></td>
        <td>11 Jun – 30 Jun</td>
        <td>Gestión de envío de IMU / Encoders al Agent, evitando cuellos de botella en FreeRTOS.</td>
        <td><ul><li>Estabilidad en la red micro-ROS (sin caídas continuas).</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 5: UI & Feedback</span><br><span class="days-badge">15 Días</span></td>
        <td>1 Jul – 15 Jul</td>
        <td>Servicio automatizado Systemd del Agent en PC. Volcados de fallos de STM32 hacia la UI (batería).</td>
        <td><ul><li>Auto-reconexión USB probada con el hardware "Hot Plug".</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 6: Pruebas (Integración)</span><br><span class="days-badge">16 Días</span></td>
        <td>16 Jul – 31 Jul</td>
        <td>Pruebas de latencia bajo alta carga de operaciones simultáneas motor/brazo/camaras.</td>
        <td><ul><li>Latencia comprobada del control embebido en logs.</li></ul></td>
      </tr>
      <tr>
        <td><span class="phase-title">Fase 7: Competencia</span><br><span class="days-badge">7 Días</span></td>
        <td>1 Ago – 7 Ago</td>
        <td>Protección de hardware en Utah (Temperatura/Polvo) y blindaje de código firmware.</td>
        <td><ul><li>Archivos .bin generados y probados.</li></ul></td>
      </tr>
    </tbody>
  </table>

</div>
</body>
</html>
"""

with open("C:/Users/saidt/Documents/Unaq/Delta/2026/CIRC2026/Cronograma.html", "w", encoding="utf-8") as f:
    f.write(html_content)
