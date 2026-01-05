from nicegui import ui, app

# ----------------------------------------
# Navigation Bar (moved here to avoid circular imports)
# ----------------------------------------

def render_nav():
    with ui.header().classes('items-center justify-center bg-blue-700 text-white p-3 shadow-md'):
        with ui.row().classes('w-full justify-around text-lg'):
            ui.link('🏠 Home', '/')
            ui.link('👥 Lineup', '/lineup')
            ui.link('⚡ Game', '/game')
            ui.link('➕ Add', '/add')
            ui.link('📤 Export', '/export')

# ----------------------------------------
# Player lookup
# ----------------------------------------

def get_player_by_name(name: str):
    for p in app.storage.user['stats']:
        if p['Player'] == name:
            return p
    return None

# ----------------------------------------
# Ensure all fields exist
# ----------------------------------------

def ensure_player_fields(player: dict):
    defaults = {
        'Pass_Att': 0, 'Pass_Comp': 0, 'Pass_Yds': 0, 'Pass_TD': 0, 'Pass_INT': 0,
        'Rec': 0, 'Rec_Yds': 0, 'Rec_TD': 0,
        'Rush_Att': 0, 'Rush_Yds': 0, 'Rush_TD': 0,
        'Flag_Pulls': 0, 'Sacks': 0, 'INT': 0, 'PBU': 0,
        'Safety': 0, 'Def_TD': 0, 'Forced_Fumble': 0,
    }
    for k, v in defaults.items():
        if k not in player:
            player[k] = v

# ----------------------------------------
# Add / Merge logic (overwrite mode)
# ----------------------------------------

def merge_or_add_player(entry):
    stats = app.storage.user['stats']
    existing = get_player_by_name(entry['Player'])

    if existing is None:
        ensure_player_fields(entry)
        stats.append(entry)
        return 'added'

    ensure_player_fields(existing)
    ensure_player_fields(entry)

    for key in entry:
        if key != 'Player':
            existing[key] = entry[key]

    return 'merged'

# ----------------------------------------
# Fast Tap logic (additive mode)
# ----------------------------------------

def record_fast_tap(player_name: str, field: str, delta: int, player_slot: str):
    if not player_name:
        return

    stats = app.storage.user['stats']
    player = get_player_by_name(player_name)

    if player is None:
        player = {'Player': player_name}
        ensure_player_fields(player)
        stats.append(player)

    ensure_player_fields(player)
    player[field] = max(0, player[field] + delta)

    app.storage.user[f'last_play_{player_slot}'] = {
        'player': player_name,
        'field': field,
        'delta': delta,
    }

# ----------------------------------------
# Undo last Fast Tap
# ----------------------------------------

def undo_last(player_slot: str):
    lp = app.storage.user.get(f'last_play_{player_slot}')
    if not lp:
        return False

    player = get_player_by_name(lp['player'])
    if not player:
        app.storage.user[f'last_play_{player_slot}'] = None
        return False

    ensure_player_fields(player)
    player[lp['field']] = max(0, player[lp['field']] - lp['delta'])

    app.storage.user[f'last_play_{player_slot}'] = None
    return True