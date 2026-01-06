from nicegui import ui, app
from datetime import datetime
import zoneinfo

# ============================================================
# STORAGE INITIALIZATION
# ============================================================

def ensure_storage():
    """Guarantee all required storage keys exist."""
    user = app.storage.user

    if 'stats' not in user:
        user['stats'] = []              # Season totals

    if 'game_stats' not in user:
        user['game_stats'] = []         # Current game only

    if 'lineup' not in user:
        user['lineup'] = []             # Persistent roster

    if 'last_update' not in user:
        user['last_update'] = None      # Timestamp of last merge


# ============================================================
# NAVIGATION BAR
# ============================================================

def render_nav():
    with ui.header().classes('items-center justify-center bg-blue-700 text-white p-3 shadow-md'):
        with ui.row().classes(
            'w-full justify-around text-lg flex-wrap gap-2'
        ):
            ui.link('🏠 Home', '/')
            ui.link('👥 Lineup', '/lineup')
            ui.link('⚡ Game', '/game')
            ui.link('📤 Export', '/export')


# ============================================================
# PLAYER LOOKUP HELPERS
# ============================================================

def get_player_by_name(name: str, source='stats'):
    """Lookup player in either season stats or game stats."""
    ensure_storage()
    data = app.storage.user[source]
    for p in data:
        if p['Player'] == name:
            return p
    return None


def ensure_player_fields(player: dict):
    """Guarantee all stat fields exist for a player."""
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


# ============================================================
# ADD / MERGE (EXPORT TAB)
# ============================================================

def merge_or_add_player(entry):
    """Used by Add/Merge tab — still writes into season stats."""
    ensure_storage()
    stats = app.storage.user['stats']
    existing = get_player_by_name(entry['Player'], source='stats')

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


# ============================================================
# FAST TAP LOGIC — WRITES INTO GAME_STATS
# ============================================================

def record_fast_tap(player_name: str, field: str, delta: int, player_slot: str):
    if not player_name:
        return

    ensure_storage()
    game_stats = app.storage.user['game_stats']

    # Lookup in game stats
    player = get_player_by_name(player_name, source='game_stats')

    # Create player entry on first tap
    if player is None:
        player = {'Player': player_name}
        ensure_player_fields(player)
        game_stats.append(player)

    # Ensure fields BEFORE updating
    ensure_player_fields(player)

    # Now safe to increment
    player[field] = max(0, player[field] + delta)

    # Track last play for undo
    app.storage.user[f'last_play_{player_slot}'] = {
        'player': player_name,
        'field': field,
        'delta': delta,
    }


# ============================================================
# UNDO LAST FAST TAP — UNDOES INSIDE GAME_STATS
# ============================================================

def undo_last(player_slot: str):
    ensure_storage()
    lp = app.storage.user.get(f'last_play_{player_slot}')
    if not lp:
        return False

    player = get_player_by_name(lp['player'], source='game_stats')
    if not player:
        app.storage.user[f'last_play_{player_slot}'] = None
        return False

    ensure_player_fields(player)
    player[lp['field']] = max(0, player[lp['field']] - lp['delta'])

    app.storage.user[f'last_play_{player_slot}'] = None
    return True


# ============================================================
# MERGE GAME → SEASON (WITH PACIFIC TIME FIX)
# ============================================================

def merge_game_into_season():
    """Merge current game stats into season totals."""
    ensure_storage()
    user = app.storage.user

    game_stats = user['game_stats']
    if not game_stats:
        ui.notify('No game stats to merge.', type='warning')
        return

    season_stats = user['stats']

    # Build lookup for season stats
    season_by_name = {p['Player']: p for p in season_stats}

    # Merge each game player into season totals
    for g in game_stats:
        name = g['Player']
        if name not in season_by_name:
            # New player for the season
            new_entry = g.copy()
            ensure_player_fields(new_entry)
            season_stats.append(new_entry)
            season_by_name[name] = new_entry
        else:
            s = season_by_name[name]
            ensure_player_fields(s)
            for key, value in g.items():
                if key == 'Player':
                    continue
                if isinstance(value, (int, float)):
                    s[key] = s.get(key, 0) + value

    # Clear game stats
    user['game_stats'] = []

    # Timestamp (Pacific Time)
    pacific = zoneinfo.ZoneInfo('America/Los_Angeles')
    now_local = datetime.now(pacific)
    user['last_update'] = now_local.strftime('%b %d, %Y @ %I:%M %p')

    ui.notify('Game stats merged into season totals.', type='positive')