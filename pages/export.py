from nicegui import ui, app
import json
import random
from datetime import datetime
import io
import shared

@ui.page('/export')
def export_page():
    ui.label('📤 Export Summary & Season Save/Load').classes('text-2xl font-bold p-4')

    stats = app.storage.user['stats']
    if not stats:
        ui.label('No stats available to export yet. Play a game or add stats first.').classes('text-red-600 p-4')
        return

    rows = []
    for p in stats:
        shared.ensure_player_fields(p)
        rows.append({
            'Player': p['Player'],
            'FP': p['Flag_Pulls'],
            'Sacks': p['Sacks'],
            'INT': p['INT'],
            'PBU': p['PBU'],
            'SFTY': p.get('Safety', 0),
            'DTD': p.get('Def_TD', 0),
            'FF': p.get('Forced_Fumble', 0),
            'Rec': p['Rec'],
            'RecYds': p['Rec_Yds'],
            'RecTD': p['Rec_TD'],
            'RushAtt': p['Rush_Att'],
            'RushYds': p['Rush_Yds'],
            'RushTD': p['Rush_TD'],
            'PA': p['Pass_Att'],
            'PC': p['Pass_Comp'],
            'PYds': p['Pass_Yds'],
            'PTD': p['Pass_TD'],
            'INT-T': p['Pass_INT'],
        })

    ui.label('Preview').classes('text-xl font-bold p-4')
    ui.table(
        columns=[{'name': k, 'label': k, 'field': k} for k in rows[0].keys()],
        rows=rows,
    ).classes('p-4')

    # CSV
    csv_lines = []
    headers = list(rows[0].keys())
    csv_lines.append(','.join(headers))
    for r in rows:
        csv_lines.append(','.join(str(r[h]) for h in headers))
    csv_data = '\n'.join(csv_lines)

    # TXT
    buffer = io.StringIO()
    buffer.write('Flag Football Stats Summary\n\n')
    for r in rows:
        buffer.write(
            f"{r['Player']}: "
            f"FP={r['FP']}, Sacks={r['Sacks']}, INT={r['INT']}, PBU={r['PBU']}, "
            f"SFTY={r['SFTY']}, DTD={r['DTD']}, FF={r['FF']}, "
            f"Rec={r['Rec']}, RecYds={r['RecYds']}, RecTD={r['RecTD']}, "
            f"RushAtt={r['RushAtt']}, RushYds={r['RushYds']}, RushTD={r['RushTD']}, "
            f"PA={r['PA']}, PC={r['PC']}, PYds={r['PYds']}, PTD={r['PTD']}, INT-T={r['INT-T']}\n"
        )
    txt_data = buffer.getvalue()

    season_data = {
        'stats': app.storage.user['stats'],
        'lineup': app.storage.user['lineup'],
    }
    season_json = json.dumps(season_data, indent=4)
    season_filename = (
        f"season_flagfootball_{random.randint(1, 1_000_000)}_"
        f"{datetime.now().strftime('%m-%d-%y')}.json"
    )

    with ui.row().classes('p-4 gap-4'):
        ui.download(text=csv_data, filename='flagfootball_stats_summary.csv', label='💾 Download CSV')
        ui.download(text=txt_data, filename='flagfootball_stats_summary.txt', label='📝 Download TXT Summary')
        ui.download(text=season_json, filename=season_filename, label='💾 Download Season JSON')

    ui.separator()

    ui.label('📁 Season Load').classes('text-xl font-bold p-4')

    async def handle_upload(e):
        file = e.content
        try:
            loaded = json.loads(file.read().decode('utf-8'))
            if 'stats' not in loaded:
                ui.notify("Invalid season file. Missing required 'stats' field.", type='negative')
                return
            app.storage.user['stats'] = loaded.get('stats', [])
            app.storage.user['lineup'] = loaded.get('lineup', [])
            ui.notify('Season loaded — lineup and stats successfully restored!', type='positive')
        except Exception as ex:
            ui.notify(f'Error loading season file: {ex}', type='negative')

    ui.upload(on_upload=handle_upload, label='📂 Load Season JSON', auto_upload=True, multiple=False).classes('p-4')