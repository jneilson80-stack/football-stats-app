from nicegui import ui

@ui.page('/faq')
def faq_page():
    ui.label('❓ FAQ / Formulas').classes('text-2xl font-bold p-4')

    ui.markdown(
        """
## 📘 What does each stat mean?

### Defense
- **FP (Flag Pulls):** Successful flag pulls (tackles in flag football)  
- **Sacks:** Quarterback sacks  
- **INT:** Defensive interceptions  
- **PBU:** Passes defended or knocked down  
- **SFTY (Safeties):** Defensive safeties scored  
- **DTD (Defensive TD):** Defensive touchdowns (e.g., pick-six, fumble return)  
- **FF (Forced Fumbles):** Times a defender caused a fumble  

### Receiving
- **Rec:** Receptions  
- **RecYds:** Receiving Yards  
- **RecTD:** Receiving Touchdowns  

### Rushing
- **RushAtt:** Rushing Attempts  
- **RushYds:** Rushing Yards  
- **RushTD:** Rushing Touchdowns  

### Passing (QB)
- **PA:** Pass Attempts  
- **PC:** Pass Completions  
- **PYds:** Passing Yards  
- **PTD:** Passing Touchdowns  
- **INT-T:** Interceptions Thrown  

---

## Add / Merge Players (Overwrite Mode)
- Manual stat entry  
- Saving overwrites that player’s totals  
- New players added to lineup automatically  

---

## Fast Tap Game Mode (Additive, Two Players)
- Two players visible side-by-side  
- Defense, Receiving, Rushing, Passing sections  
- +1 and +5 yard buttons for fast input  
- Undo per-player reverses the last tap  

---

## Export & Season Save/Load
- CSV + TXT export for stats  
- Season JSON saves all stats plus lineup  
- Load Season restores everything for future games  
"""
    ).classes('p-4')