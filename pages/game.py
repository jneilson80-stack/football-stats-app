from nicegui import ui, app
import shared

@ui.page('/game')
def game_page():
    shared.render_nav()
    ui.label('⚡ Fast Tap Game Mode').classes('text-2xl font-bold p-4')

    lineup = app.storage.user['lineup']
    if not lineup:
        ui.label('No players in lineup. Add players first.').classes('text-red-600 text-lg p-4')
        return

    # ----------------------------------------
    # Player selectors
    # ----------------------------------------
    with ui.row().classes('w-full justify-around p-4'):
        p1 = ui.select(lineup, label='Player 1').classes('w-1/3')
        p2 = ui.select(lineup, label='Player 2').classes('w-1/3')

    # Helper to build two-column button grids
    def two_col_buttons(buttons):
        with ui.row().classes('w-full no-wrap gap-4'):
            with ui.column().classes('w-1/2 gap-2'):
                for label, func in buttons[0]:
                    ui.button(label, on_click=func).classes('w-full')
            with ui.column().classes('w-1/2 gap-2'):
                for label, func in buttons[1]:
                    ui.button(label, on_click=func).classes('w-full')

    # ----------------------------------------
    # PLAYER 1 SECTION
    # ----------------------------------------
    with ui.column().classes('w-full bg-gray-100 p-4 rounded-lg mt-4'):
        ui.label('Player 1 Actions').classes('text-xl font-bold')

        def tap1(field, delta):
            shared.record_fast_tap(p1.value, field, delta, 'p1')

        # Defense (always visible)
        ui.label('🛡️ Defense').classes('font-semibold mt-2')
        two_col_buttons([
            [
                ('FP', lambda: tap1('Flag_Pulls', 1)),
                ('SK', lambda: tap1('Sacks', 1)),
                ('INT', lambda: tap1('INT', 1)),
            ],
            [
                ('PBU', lambda: tap1('PBU', 1)),
                ('SFTY', lambda: tap1('Safety', 1)),
                ('DTD', lambda: tap1('Def_TD', 1)),
                ('FF', lambda: tap1('Forced_Fumble', 1)),
            ]
        ])

        ui.separator()

        # Receiving (always visible)
        ui.label('🤲 Receiving').classes('font-semibold mt-2')
        two_col_buttons([
            [
                ('REC', lambda: tap1('Rec', 1)),
                ('RTD', lambda: tap1('Rec_TD', 1)),
            ],
            [
                ('RY +1', lambda: tap1('Rec_Yds', 1)),
                ('RY +5', lambda: tap1('Rec_Yds', 5)),
            ]
        ])

        ui.separator()

        # Rushing (collapsible)
        with ui.expansion('🏃 Rushing').classes('mt-2'):
            two_col_buttons([
                [
                    ('RA', lambda: tap1('Rush_Att', 1)),
                    ('RTD', lambda: tap1('Rush_TD', 1)),
                ],
                [
                    ('RY +1', lambda: tap1('Rush_Yds', 1)),
                    ('RY +5', lambda: tap1('Rush_Yds', 5)),
                ]
            ])

        ui.separator()

        # Passing (collapsible)
        with ui.expansion('🎯 Passing').classes('mt-2'):
            two_col_buttons([
                [
                    ('PA', lambda: tap1('Pass_Att', 1)),
                    ('PC', lambda: tap1('Pass_Comp', 1)),
                    ('PTD', lambda: tap1('Pass_TD', 1)),
                ],
                [
                    ('PY +1', lambda: tap1('Pass_Yds', 1)),
                    ('PY +5', lambda: tap1('Pass_Yds', 5)),
                    ('INT‑T', lambda: tap1('Pass_INT', 1)),
                ]
            ])

        ui.separator()

        def undo1():
            if shared.undo_last('p1'):
                ui.notify('Player 1: Last action undone')
            else:
                ui.notify('Player 1: Nothing to undo')

        ui.button('↩️ Undo', on_click=undo1, color='red').classes('mt-2')

    # ----------------------------------------
    # PLAYER 2 SECTION (stacked below)
    # ----------------------------------------
    with ui.column().classes('w-full bg-gray-100 p-4 rounded-lg mt-6'):
        ui.label('Player 2 Actions').classes('text-xl font-bold')

        def tap2(field, delta):
            shared.record_fast_tap(p2.value, field, delta, 'p2')

        # Defense
        ui.label('🛡️ Defense').classes('font-semibold mt-2')
        two_col_buttons([
            [
                ('FP', lambda: tap2('Flag_Pulls', 1)),
                ('SK', lambda: tap2('Sacks', 1)),
                ('INT', lambda: tap2('INT', 1)),
            ],
            [
                ('PBU', lambda: tap2('PBU', 1)),
                ('SFTY', lambda: tap2('Safety', 1)),
                ('DTD', lambda: tap2('Def_TD', 1)),
                ('FF', lambda: tap2('Forced_Fumble', 1)),
            ]
        ])

        ui.separator()

        # Receiving
        ui.label('🤲 Receiving').classes('font-semibold mt-2')
        two_col_buttons([
            [
                ('REC', lambda: tap2('Rec', 1)),
                ('RTD', lambda: tap2('Rec_TD', 1)),
            ],
            [
                ('RY +1', lambda: tap2('Rec_Yds', 1)),
                ('RY +5', lambda: tap2('Rec_Yds', 5)),
            ]
        ])

        ui.separator()

        # Rushing (collapsible)
        with ui.expansion('🏃 Rushing').classes('mt-2'):
            two_col_buttons([
                [
                    ('RA', lambda: tap2('Rush_Att', 1)),
                    ('RTD', lambda: tap2('Rush_TD', 1)),
                ],
                [
                    ('RY +1', lambda: tap2('Rush_Yds', 1)),
                    ('RY +5', lambda: tap2('Rush_Yds', 5)),
                ]
            ])

        ui.separator()

        # Passing (collapsible)
        with ui.expansion('🎯 Passing').classes('mt-2'):
            two_col_buttons([
                [
                    ('PA', lambda: tap2('Pass_Att', 1)),
                    ('PC', lambda: tap2('Pass_Comp', 1)),
                    ('PTD', lambda: tap2('Pass_TD', 1)),
                ],
                [
                    ('PY +1', lambda: tap2('Pass_Yds', 1)),
                    ('PY +5', lambda: tap2('Pass_Yds', 5)),
                    ('INT‑T', lambda: tap2('Pass_INT', 1)),
                ]
            ])

        ui.separator()

        def undo2():
            if shared.undo_last('p2'):
                ui.notify('Player 2: Last action undone')
            else:
                ui.notify('Player 2: Nothing to undo')

        ui.button('↩️ Undo', on_click=undo2, color='red').classes('mt-2')

    # ----------------------------------------
    # Live Summary Table
    # ----------------------------------------
    ui.separator()
    ui.label('📊 Live Game Summary').classes('text-xl font-bold p-4')

    summary_table = ui.table(
        columns=[
            {'name': 'Player', 'label': 'Player', 'field': 'Player'},
            {'name': 'FP', 'label': 'FP', 'field': 'Flag_Pulls'},
            {'name': 'SK', 'label': 'SK', 'field': 'Sacks'},
            {'name': 'INT', 'label': 'INT', 'field': 'INT'},
            {'name': 'PBU', 'label': 'PBU', 'field': 'PBU'},
            {'name': 'SFTY', 'label': 'SFTY', 'field': 'Safety'},
            {'name': 'DTD', 'label': 'DTD', 'field': 'Def_TD'},
            {'name': 'FF', 'label': 'FF', 'field': 'Forced_Fumble'},
            {'name': 'REC', 'label': 'REC', 'field': 'Rec'},
            {'name': 'RY', 'label': 'RY', 'field': 'Rec_Yds'},
            {'name': 'RTD', 'label': 'RTD', 'field': 'Rec_TD'},
            {'name': 'RA', 'label': 'RA', 'field': 'Rush_Att'},
            {'name': 'RY', 'label': 'RY', 'field': 'Rush_Yds'},
            {'name': 'RTD', 'label': 'RTD', 'field': 'Rush_TD'},
            {'name': 'PA', 'label': 'PA', 'field': 'Pass_Att'},
            {'name': 'PC', 'label': 'PC', 'field': 'Pass_Comp'},
            {'name': 'PY', 'label': 'PY', 'field': 'Pass_Yds'},
            {'name': 'PTD', 'label': 'PTD', 'field': 'Pass_TD'},
            {'name': 'INT‑T', 'label': 'INT‑T', 'field': 'Pass_INT'},
        ],
        rows=[],
    ).classes('p-4 w-full overflow-x-auto')

    def refresh_summary():
        rows = []
        for p in app.storage.user['stats']:
            shared.ensure_player_fields(p)
            rows.append(p)
        summary_table.rows = rows

    ui.timer(0.5, refresh_summary)