import re
import json

html_file = 'Cronograma.html'

with open(html_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Buscamos todas las tablas
matches = re.finditer(r'<h2 class="([^"]+)-title">.*?Proyecto: ([^<]+)\s*<span class="responsible-badge">\((.*?)\)</span>.*?<tbody>(.*?)</tbody>', text, re.DOTALL)

events = []
id_counter = 1

for match in matches:
    cat_class = match.group(1) # chasis, brazo, microros
    project_name = match.group(2).strip()
    resp_raw = match.group(3).replace('Responsables:', '').strip()
    
    tbody = match.group(4)
    rows = re.finditer(r'<tr>(.*?)</tr>', tbody, re.DOTALL)
    
    for row_match in rows:
        row = row_match.group(1)
        cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(cols) >= 4:
            # col[0] = Fase
            fase_match = re.search(r'<span class="phase-title">([^<]+)</span>', cols[0])
            fase_name = fase_match.group(1) if fase_match else ""
            
            # col[1] = Fechas (ej: 23 Abr – 6 May)
            # col[3] = Entregables en <ul><li>
            entregables_li = re.findall(r'<li>(.*?)</li>', cols[3], re.DOTALL)
            
            # Obtener fecha final (la entregable es al final de la fase)
            # Ej: 23 Abr – 6 May -> 2026-05-06
            date_str = cols[1]
            dates = re.findall(r'\d+\s+[A-Za-z]+', date_str)
            
            end_date = "2026-08-01"
            if len(dates) >= 2:
                # convert "6 May" to "2026-05-06"
                d_end = dates[1].split()
                months = {'Abr':'04','May':'05','Jun':'06','Jul':'07','Ago':'08'}
                mm = months.get(d_end[1][:3], '01')
                dd = d_end[0].zfill(2)
                end_date = f"2026-{mm}-{dd}"
            
            for ent in entregables_li:
                events.append({
                    "id": f"p_{id_counter}",
                    "name": f"[{project_name}] {ent.strip()}",
                    "responsible": resp_raw,
                    "date": end_date,
                    "status": "en-proceso",
                    "important": False
                })
                id_counter += 1

# Agregar los milestones especiales de la tabla de la ultima edicion
extra = [
  {"id": 'd1', "name": "Control de Xbox + Integración IMU (Telecomms)", "responsible": "Luis y Gerardo", "date": "2026-05-23", "status": "en-proceso", "important": False},
  {"id": 'd2', "name": "Chasis funcional (Semana 5)", "responsible": "Milton y Said", "date": "2026-06-06", "status": "en-proceso", "important": True},
  {"id": 'd3', "name": "Simulación funcional del brazo (Semana 5)", "responsible": "Angel y Raul", "date": "2026-06-06", "status": "en-proceso", "important": False},
  {"id": 'd4', "name": "Chasis funcional + PCB + sensores (Semana 10)", "responsible": "Milton, Said, Luis, Gerardo", "date": "2026-07-11", "status": "en-proceso", "important": True},
  {"id": 'd5', "name": "Brazo funcional + PCB (Semana 12)", "responsible": "Angel, Raul, Luis, Gerardo", "date": "2026-07-25", "status": "en-proceso", "important": True}
]

events.extend(extra)
new_json = json.dumps(events, ensure_ascii=False, indent=6)
new_json_str = f"const initialDeliverables = {new_json};"

# Replace inside html
text = re.sub(r'const initialDeliverables = \[.*?\];', new_json_str, text, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(text)
    
print("Successfully extracted and merged all deliverables!")
