# 🏈 Football Stats App

A clean, fast, and mobile‑friendly football statistics tracker built with **Python** and **NiceGUI**.  
Designed for real‑time sideline use, this app makes it easy to record plays, track player performance, and generate game summaries with zero friction.

---

## 🚀 Features

- **Live game tracking** with intuitive buttons and workflows  
- **Player management** with quick add/merge tools  
- **Automatic stat summaries** for offense, defense, and special teams  
- **Clean UI** optimized for phones and tablets  
- **Instant export** of game data  
- **FAQ page** for quick reference during live use  
- **Persistent layout** and predictable navigation for stress‑free scoring  

---

## 📁 Project Structure

```
football-stats-app/
│
├── main.py               # App entry point
├── shared.py             # Shared utilities and state
├── pages/
│   ├── game.py           # Live game tracking
│   ├── lineup.py         # Player management
│   ├── add_merge.py      # Add/merge player workflow
│   ├── export.py         # Export tools
│   └── Archive/          # Older versions and notes
│
└── .gitignore            # Python + environment exclusions
```

---

## 🛠️ Tech Stack

- **Python 3.x**
- **NiceGUI** for UI
- **GitHub Desktop** for version control
- **Lightsail** (optional) for deployment

---

## ▶️ Running the App Locally

1. Install dependencies:
   ```
   pip install nicegui
   ```
2. Run the app:
   ```
   python main.py
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

---

## 📦 Exporting Game Data

The app includes built‑in export tools for saving game summaries or sharing stats with coaches, parents, or players.

---

## 🧭 Roadmap

- Add season‑long stat tracking  
- Add team management  
- Add per‑player dashboards  
- Add CSV export  
- Add dark mode  

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
