from nicegui import ui, app
import shared
from functools import partial


@ui.page('/game')
def game_page():
    shared.ensure_storage()
    shared.render_nav()
    # ------------------------------------------------------------
    # JS LONG-PRESS HANDLER (works on all NiceGUI versions)
    # ------------------------------------------------------------
    ui.add_head_html('''
        <script>
            function addLongPress(el, message) {
                let timer;
                el.addEventListener('touchstart', () => {
                    timer = setTimeout(() => {
                        window.dispatchEvent(new CustomEvent('longpress', {detail: message}));
                    }, 500);
                });
                el.addEventListener('touchend', () => clearTimeout(timer));
                el.addEventListener('touchmove', () => clearTimeout(timer));
            }
            window.addEventListener('longpress', (e) => {
                nicegui.notify(e.detail);
            });
        </script>
    ''')
    
    ui.label('⚡ Fast Tap Game Mode').classes('text-2xl font-bold p-4')

    lineup = app.storage.user.get('lineup', [])
    if not lineup:
        ui.label('No players in lineup. Add players first.').classes(
            'text-red-600 text-lg p-4'
        )
        return

    # ------------------------------------------------------------
    # PRE‑CREATE GAME PLAYERS (FIXES DOUBLE‑TAP BUG)
    # ------------------------------------------------------------
    game_stats = app.storage.user.setdefault('game_stats', [])
    existing_names = {p['Player'] for p in game_stats}

    for name in lineup:
        if name not in existing_names:
            new_entry = {'Player': name}
            shared.ensure_player_fields(new_entry)
            game_stats.append(new_entry)

    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------
    def get_or_create_game_player(player_name: str) -> dict:
        game_stats = app.storage.user.setdefault('game_stats', [])
        for p in game_stats:
            if p.get('Player') == player_name:
                shared.ensure_player_fields(p)
                return p
        new_player = {'Player': player_name}
        shared.ensure_player_fields(new_player)
        game_stats.append(new_player)
        return new_player

    def update_game_stat(player_name: str, field: str, value) -> None:
        try:
            numeric = int(value) if value not in (None, '') else 0
        except ValueError:
            ui.notify('Please enter a whole number', type='warning')
            return
        player = get_or_create_game_player(player_name)
        player[field] = numeric

    # ------------------------------------------------------------
    # SEASON TOTALS TABLE
    # ------------------------------------------------------------
    full_columns = [
        {'name': 'Player', 'label': 'Player', 'field': 'Player'},
        {'name': 'FP', 'label': 'FP', 'field': 'Flag_Pulls'},
        {'name': 'SK', 'label': 'SK', 'field': 'Sacks'},
        {'name': 'INT', 'label': 'INT', 'field': 'INT'},
        {'name': 'PBU', 'label': 'PBU', 'field': 'PBU'},
        {'name': 'SFTY', 'label': 'SFTY', 'field': 'Safety'},
        {'name': 'DTD', 'label': 'DTD', 'field': 'Def_TD'},
        {'name': 'FF', 'label': 'FF', 'field': 'Forced_Fumble'},
        {'name': 'REC', 'label': 'REC', 'field': 'Rec'},
        {'name': 'RY_REC', 'label': 'RY (Rec)', 'field': 'Rec_Yds'},
        {'name': 'RTD', 'label': 'RTD', 'field': 'Rec_TD'},
        {'name': 'RA', 'label': 'RA', 'field': 'Rush_Att'},
        {'name': 'RY_RUSH', 'label': 'RY (Rush)', 'field': 'Rush_Yds'},
        {'name': 'RTD_RUSH', 'label': 'RTD (Rush)', 'field': 'Rush_TD'},
        {'name': 'PA', 'label': 'PA', 'field': 'Pass_Att'},
        {'name': 'PC', 'label': 'PC', 'field': 'Pass_Comp'},
        {'name': 'PY', 'label': 'PY', 'field': 'Pass_Yds'},
        {'name': 'PTD', 'label': 'PTD', 'field': 'Pass_TD'},
        {'name': 'INT-T', 'label': 'INT-T', 'field': 'Pass_INT'},
    ]

    ui.separator()
    ui.label('📊 Season Totals').classes('text-xl font-bold p-4')
    season_table = ui.table(columns=full_columns, rows=[]).classes(
        'p-4 w-full overflow-x-auto'
    )

    timestamp_label = ui.label('Last updated: (not yet merged)').classes(
        'text-sm text-gray-600 px-4'
    )

    # ------------------------------------------------------------
    # GAME SUMMARY TABLE
    # ------------------------------------------------------------
    key_columns = [
        {'name': 'Player', 'label': 'Player', 'field': 'Player'},
        {'name': 'FP', 'label': 'FP', 'field': 'Flag_Pulls'},
        {'name': 'REC', 'label': 'REC', 'field': 'Rec'},
        {'name': 'RY', 'label': 'RY', 'field': 'Rec_Yds'},
        {'name': 'RA', 'label': 'RA', 'field': 'Rush_Att'},
        {'name': 'PY', 'label': 'PY', 'field': 'Pass_Yds'},
        {'name': 'TD', 'label': 'TD', 'field': 'Total_TD'},
    ]

    ui.separator()
    ui.label('📋 Current Game Summary').classes('text-xl font-bold p-4')

    game_summary_table = ui.table(
        columns=key_columns,
        rows=[],
        row_key='Player',
    ).classes('p-4 w-full overflow-x-auto')

    # ------------------------------------------------------------
    # REFRESH TABLES (MUST COME FIRST)
    # ------------------------------------------------------------
    def refresh_tables():
        # Season totals
        season_rows = []
        for p in app.storage.user.get('season_stats', []):
            shared.ensure_player_fields(p)
            season_rows.append(p)
        season_table.rows = season_rows

        # Game summary (hide zero-stat players)
        game_rows = []
        for p in app.storage.user.get('game_stats', []):
            shared.ensure_player_fields(p)

            has_stats = any(
                p.get(field, 0) > 0
                for field in [
                    'Flag_Pulls', 'Sacks', 'INT', 'PBU', 'Safety', 'Def_TD', 'Forced_Fumble',
                    'Rec', 'Rec_Yds', 'Rec_TD',
                    'Rush_Att', 'Rush_Yds', 'Rush_TD',
                    'Pass_Att', 'Pass_Comp', 'Pass_Yds', 'Pass_TD', 'Pass_INT'
                ]
            )
            if not has_stats:
                continue

            total_td = (
                p.get('Rec_TD', 0)
                + p.get('Rush_TD', 0)
                + p.get('Pass_TD', 0)
                + p.get('Def_TD', 0)
            )

            game_rows.append(
                {
                    'Player': p['Player'],
                    'Flag_Pulls': p['Flag_Pulls'],
                    'Rec': p['Rec'],
                    'Rec_Yds': p['Rec_Yds'],
                    'Rush_Att': p['Rush_Att'],
                    'Pass_Yds': p['Pass_Yds'],
                    'Total_TD': total_td,
                }
            )

        game_summary_table.rows = game_rows

        ts = app.storage.user.get('last_update')
        timestamp_label.text = (
            f'Last updated: {ts}' if ts else 'Last updated: (not yet merged)'
        )

    # ------------------------------------------------------------
    # TAP FUNCTION (MUST COME BEFORE BUTTONS)
    # ------------------------------------------------------------
    def tap(player_name: str, field: str, delta: int, tag: str):
        shared.record_fast_tap(player_name, field, delta, tag)
        refresh_tables()

    # ------------------------------------------------------------
    # TWO-COLUMN BUTTON LAYOUT (JS long-press + tooltip)
    # ------------------------------------------------------------
    def two_col_buttons(buttons):
        with ui.row().classes('w-full no-wrap gap-4'):
            with ui.column().classes('w-1/2 gap-2'):
                for label, func, tip in buttons[0]:
                    b = ui.button(label, on_click=func).tooltip(tip).classes('w-full')
                    b.on('mounted', f"addLongPress(document.getElementById('{b.id}'), '{tip}')")

            with ui.column().classes('w-1/2 gap-2'):
                for label, func, tip in buttons[1]:
                    b = ui.button(label, on_click=func).tooltip(tip).classes('w-full')
                    b.on('mounted', f"addLongPress(document.getElementById('{b.id}'), '{tip}')")

    # ------------------------------------------------------------
    # FAST TAP PLAYER BLOCK (NOW WITH TOOLTIPS)
    # ------------------------------------------------------------
    def render_player_block(player_name: str, tag: str):
        with ui.column().classes('w-full bg-gray-100 p-4 rounded-lg mt-4'):
            ui.label(f'{player_name} Actions').classes('text-xl font-bold')

            # DEFENSE
            ui.label('🛡️ Defense').classes('font-semibold mt-2')
            two_col_buttons(
                [
                    [
                        ('FP', partial(tap, player_name, 'Flag_Pulls', 1, tag), 'Flag Pulls'),
                        ('SK', partial(tap, player_name, 'Sacks', 1, tag), 'Sacks'),
                        ('INT', partial(tap, player_name, 'INT', 1, tag), 'Interceptions'),
                    ],
                    [
                        ('PBU', partial(tap, player_name, 'PBU', 1, tag), 'Pass Breakups'),
                        ('SFTY', partial(tap, player_name, 'Safety', 1, tag), 'Safety'),
                        ('DTD', partial(tap, player_name, 'Def_TD', 1, tag), 'Defensive Touchdown'),
                        ('FF', partial(tap, player_name, 'Forced_Fumble', 1, tag), 'Forced Fumble'),
                    ],
                ]
            )

            # RECEIVING
            ui.separator()
            ui.label('🤲 Receiving').classes('font-semibold mt-2')
            two_col_buttons(
                [
                    [
                        ('REC', partial(tap, player_name, 'Rec', 1, tag), 'Receptions'),
                        ('RTD', partial(tap, player_name, 'Rec_TD', 1, tag), 'Receiving Touchdown'),
                    ],
                    [
                        ('RY +1', partial(tap, player_name, 'Rec_Yds', 1, tag), 'Receiving Yards (+1)'),
                        ('RY +5', partial(tap, player_name, 'Rec_Yds', 5, tag), 'Receiving Yards (+5)'),
                    ],
                ]
            )

            # RUSHING
            ui.separator()
            with ui.expansion('🏃 Rushing').classes('mt-2'):
                two_col_buttons(
                    [
                        [
                            ('RA', partial(tap, player_name, 'Rush_Att', 1, tag), 'Rush Attempts'),
                            ('RTD', partial(tap, player_name, 'Rush_TD', 1, tag), 'Rushing Touchdown'),
                        ],
                        [
                            ('RY +1', partial(tap, player_name, 'Rush_Yds', 1, tag), 'Rushing Yards (+1)'),
                            ('RY +5', partial(tap, player_name, 'Rush_Yds', 5, tag), 'Rushing Yards (+5)'),
                        ],
                    ]
                )

            # PASSING
            ui.separator()
            with ui.expansion('🎯 Passing').classes('mt-2'):
                two_col_buttons(
                    [
                        [
                            ('PA', partial(tap, player_name, 'Pass_Att', 1, tag), 'Pass Attempts'),
                            ('PC', partial(tap, player_name, 'Pass_Comp', 1, tag), 'Pass Completions'),
                            ('PTD', partial(tap, player_name, 'Pass_TD', 1, tag), 'Passing Touchdown'),
                        ],
                        [
                            ('PY +1', partial(tap, player_name, 'Pass_Yds', 1, tag), 'Passing Yards (+1)'),
                            ('PY +5', partial(tap, player_name, 'Pass_Yds', 5, tag), 'Passing Yards (+5)'),
                            ('INT-T', partial(tap, player_name, 'Pass_INT', 1, tag), 'Interception Thrown'),
                        ],
                    ]
                )

            # UNDO
            def undo():
                if shared.undo_last(tag):
                    ui.notify(f'{player_name}: Last action undone')
                else:
                    ui.notify(f'{player_name}: Nothing to undo')
                refresh_tables()

            ui.button('↩️ Undo', on_click=undo, color='red').classes('mt-3')

    # ------------------------------------------------------------
    # MERGE BUTTON
    # ------------------------------------------------------------
    ui.button(
        'Merge Current Game Into Season Totals',
        on_click=lambda: (shared.merge_game_into_season(), refresh_tables()),
    ).classes('m-4')

    # ------------------------------------------------------------
    # LAYOUT
    # ------------------------------------------------------------
    p1_name = lineup[0] if len(lineup) >= 1 else None
    p2_name = lineup[1] if len(lineup) >= 2 else None

    if p1_name and p2_name:
        with ui.row().classes('w-full items-start gap-4 px-4'):
            with ui.column().classes('w-1/2'):
                render_player_block(p1_name, 'p1')
            with ui.column().classes('w-1/2'):
                render_player_block(p2_name, 'p2')
    elif p1_name:
        with ui.column().classes('w-full px-4'):
            render_player_block(p1_name, 'p1')

    # ------------------------------------------------------------
    # TIMER
    # ------------------------------------------------------------
    ui.timer(0.5, refresh_tables)