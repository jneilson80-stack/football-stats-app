from nicegui import ui, app
import shared

@ui.page('/add')
def add_merge_page():
    ui.label('➕ Add or Merge Player Stats').classes('text-2xl font-bold p-4')

    lineup_names = app.storage.user['lineup']
    existing_names = [p['Player'] for p in app.storage.user['stats']]
    combined_names = sorted(set(lineup_names + existing_names))

    name_options = ['Reset selection (use new name field)'] + combined_names

    state = {
        'selected_option': 'Reset selection (use new name field)',
        'new_name': '',
    }

    with ui.column().classes('p-4 gap-4'):

        name_input = ui.input(
            'New player name (if adding someone new):',
            on_change=lambda e: state.update(new_name=e.value),
        )

        select = ui.select(
            options=name_options,
            label='Choose an existing player or reset:',
            value=state['selected_option'],
            on_change=lambda e: state.update(selected_option=e.value),
        )

        ui.separator()

        with ui.column().classes('gap-2'):
            ui.label('Defense').classes('text-xl font-bold')
            fp = ui.number('Flag Pulls (FP)', min=0, step=1, value=0)
            sacks = ui.number('Sacks', min=0, step=1, value=0)
            dint = ui.number('Interceptions (INT)', min=0, step=1, value=0)
            pbu = ui.number('Pass Breakups (PBU)', min=0, step=1, value=0)
            sfty = ui.number('Safeties (SFTY)', min=0, step=1, value=0)
            dtd = ui.number('Defensive Touchdowns (DTD)', min=0, step=1, value=0)
            ff = ui.number('Forced Fumbles (FF)', min=0, step=1, value=0)

        with ui.column().classes('gap-2 mt-4'):
            ui.label('Receiving').classes('text-xl font-bold')
            rec = ui.number('Receptions (Rec)', min=0, step=1, value=0)
            recy = ui.number('Receiving Yards (RecYds)', min=0, step=1, value=0)
            rectd = ui.number('Receiving Touchdowns (RecTD)', min=0, step=1, value=0)

        with ui.column().classes('gap-2 mt-4'):
            ui.label('Rushing').classes('text-xl font-bold')
            rusha = ui.number('Rushing Attempts (RushAtt)', min=0, step=1, value=0)
            rushy = ui.number('Rushing Yards (RushYds)', min=0, step=1, value=0)
            rushtd = ui.number('Rushing Touchdowns (RushTD)', min=0, step=1, value=0)

        with ui.column().classes('gap-2 mt-4'):
            ui.label('Passing (QB)').classes('text-xl font-bold')
            pa = ui.number('Pass Attempts (PA)', min=0, step=1, value=0)
            pc = ui.number('Pass Completions (PC)', min=0, step=1, value=0)
            pyds = ui.number('Passing Yards (PYds)', min=0, step=1, value=0)
            ptd = ui.number('Passing Touchdowns (PTD)', min=0, step=1, value=0)
            pint = ui.number('Interceptions Thrown (INT-T)', min=0, step=1, value=0)

        def handle_add_merge():
            if state['selected_option'] == 'Reset selection (use new name field)':
                name = (state['new_name'] or '').strip()
            else:
                name = state['selected_option'].strip()

            if not name:
                ui.notify('Please select a player or enter a new player name.', type='negative')
                return

            is_new = shared.get_player_by_name(name) is None

            total_stats = (
                fp.value + sacks.value + dint.value + pbu.value + sfty.value + dtd.value + ff.value +
                rec.value + recy.value + rectd.value +
                rusha.value + rushy.value + rushtd.value +
                pa.value + pc.value + pyds.value + ptd.value + pint.value
            )

            if is_new and total_stats == 0:
                ui.notify('Please enter stats for a new player.', type='negative')
                return

            entry = {
                'Player': name,
                'Flag_Pulls': fp.value,
                'Sacks': sacks.value,
                'INT': dint.value,
                'PBU': pbu.value,
                'Safety': sfty.value,
                'Def_TD': dtd.value,
                'Forced_Fumble': ff.value,
                'Rec': rec.value,
                'Rec_Yds': recy.value,
                'Rec_TD': rectd.value,
                'Rush_Att': rusha.value,
                'Rush_Yds': rushy.value,
                'Rush_TD': rushtd.value,
                'Pass_Att': pa.value,
                'Pass_Comp': pc.value,
                'Pass_Yds': pyds.value,
                'Pass_TD': ptd.value,
                'Pass_INT': pint.value,
            }

            result = shared.merge_or_add_player(entry)

            if name not in app.storage.user['lineup']:
                app.storage.user['lineup'].append(name)
                app.storage.user['lineup'].sort()

            if result == 'added':
                ui.notify(f'Added stats for {name}.', type='positive')
            else:
                ui.notify(f'Merged (overwrote) stats for {name}.', type='positive')

        ui.button('➕ Add / Merge Player Stats', on_click=handle_add_merge).classes('mt-4')

    if app.storage.user['stats']:
        ui.separator()
        ui.label('📊 Current Player Stats').classes('text-xl font-bold p-4')
        table_rows = []
        for p in app.storage.user['stats']:
            shared.ensure_player_fields(p)
            table_rows.append({
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

        ui.table(
            columns=[
                {'name': 'Player', 'label': 'Player', 'field': 'Player'},
                {'name': 'FP', 'label': 'FP', 'field': 'FP'},
                {'name': 'Sacks', 'label': 'Sacks', 'field': 'Sacks'},
                {'name': 'INT', 'label': 'INT', 'field': 'INT'},
                {'name': 'PBU', 'label': 'PBU', 'field': 'PBU'},
                {'name': 'SFTY', 'label': 'SFTY', 'field': 'SFTY'},
                {'name': 'DTD', 'label': 'DTD', 'field': 'DTD'},
                {'name': 'FF', 'label': 'FF', 'field': 'FF'},
                {'name': 'Rec', 'label': 'Rec', 'field': 'Rec'},
                {'name': 'RecYds', 'label': 'RecYds', 'field': 'RecYds'},
                {'name': 'RecTD', 'label': 'RecTD', 'field': 'RecTD'},
                {'name': 'RushAtt', 'label': 'RushAtt', 'field': 'RushAtt'},
                {'name': 'RushYds', 'label': 'RushYds', 'field': 'RushYds'},
                {'name': 'RushTD', 'label': 'RushTD', 'field': 'RushTD'},
                {'name': 'PA', 'label': 'PA', 'field': 'PA'},
                {'name': 'PC', 'label': 'PC', 'field': 'PC'},
                {'name': 'PYds', 'label': 'PYds', 'field': 'PYds'},
                {'name': 'PTD', 'label': 'PTD', 'field': 'PTD'},
                {'name': 'INT-T', 'label': 'INT-T', 'field': 'INT-T'},
            ],
            rows=table_rows,
        ).classes('p-4')