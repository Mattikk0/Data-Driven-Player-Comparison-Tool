# ⚽ Data-Driven Player Comparison Tool

A powerful web application that discovers similar footballers based on comprehensive statistical analysis. Search for any player and instantly find their statistical twins and contrasts across Europe's top leagues.

![Python](https://img.shields.io/badge/Python-44%25-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-34.7%25-yellow)
![CSS](https://img.shields.io/badge/CSS-12.5%25-pink)
![HTML](https://img.shields.io/badge/HTML-8.8%25-orange)

---

## 🎯 Overview

This tool leverages advanced statistical analysis to identify footballers with similar performance patterns. Whether you're a scout, analyst, or football enthusiast, quickly find players with comparable stats across the **Big 5 European Leagues** (Premier League, La Liga, Serie A, Bundesliga, Ligue 1).

### Key Features

✨ **Smart Player Search** - Find any active footballer across top European leagues
📊 **Statistical Comparison** - Cosine similarity matching based on 30+ performance metrics
🔍 **Detailed Results** - Get top 10 most and least similar players
👥 **Player Profiles** - View age, position, current team, and market value
🚀 **Lightning Fast** - Real-time results powered by optimized algorithms

---

## 📋 How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Application                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (HTML/CSS/JS)                                      │
│  ├── Search Interface                                        │
│  ├── Results Display (Top & Least Similar)                   │
│  └── Player Card Showcase                                    │
│                                                               │
│  Backend (Python)                                            │
│  ├── app.py (Routes & Logic)                                 │
│  ├── queries/                                                │
│  │   ├── transfermarkt_query.py (Player Data)                │
│  │   └── fbref_query.py (Statistical Data)                   │
│  └── modules/                                                │
│      ├── stats_comparator.py (Similarity Logic)              │
│      ├── data_processing.py (Z-Score & Cosine Similarity)    │
│      └── config.py (Position Mappings)                       │
│                                                               │
│  External APIs                                               │
│  ├── FBref (via SoccerData - Player Statistics)              │
│  └── Transfermarkt (via felipeall - Player Info & Value)     │
└─────────────────────────────────────────────────────────────┘
```

### Statistical Methodology

The comparison algorithm uses **cosine similarity** with normalized statistics:

1. **Data Extraction** - Retrieves player stats from FBref (30+ metrics)
2. **Z-Score Normalization** - Standardizes stats across all players in the league
3. **Feature Vectorization** - Converts normalized stats into numerical vectors
4. **Cosine Similarity Calculation** - Measures similarity between player vectors
5. **Ranking** - Orders results from most to least similar

This ensures fair comparison regardless of playing style or position-specific metrics.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Running Transfermarkt API server (localhost:8000)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mattikk0/Data-Driven-Player-Comparison-Tool.git
   cd Data-Driven-Player-Comparison-Tool
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors soccerdata pandas scikit-learn requests unidecode
   ```

4. **Start the Transfermarkt API** (separate setup required)
   - Ensure the Transfermarkt API is running on `localhost:8000`
   - This provides player search and profile data

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

---

## 📖 API Documentation

### Endpoints

#### 1. Get Similar Players
```http
POST /search
Content-Type: application/json

{
  "player_name": "Messi"
}
```

**Response:**
```json
{
  "most": [
    {
      "name": "Player Name",
      "position": "RW",
      "team": "Team Name",
      "value": "€50M",
      "age": 28,
      "similarity": 0.92
    }
  ],
  "least": [
    {
      "name": "Player Name",
      "position": "CB",
      "team": "Team Name",
      "value": "€30M",
      "age": 31,
      "similarity": 0.15
    }
  ]
}
```

#### 2. Get Player Information
```http
POST /player_info
Content-Type: application/json

{
  "player_name": "Messi"
}
```

**Response:**
```json
{
  "name": "Lionel Messi",
  "position": "RW",
  "team": "Inter Miami CF",
  "value": "€35M",
  "age": 36,
  "image_url": "https://..."
}
```

---

## 📁 Project Structure

```
Data-Driven-Player-Comparison-Tool/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── queries/
│   ├── transfermarkt_query.py      # Transfermarkt API interactions
│   └── fbref_query.py              # FBref data processing
│
├── modules/
│   ├── stats_comparator.py         # Core comparison logic
│   ├── data_processing.py          # Statistical calculations
│   └── config.py                   # Position mappings (FBref ↔ Transfermarkt)
│
└── static/
    ├── html/
    │   └── index.html              # Web interface
    └── assets/
        ├── styles.css              # Styling
        ├── data.js                 # API communication
        ├── animations.js           # UI animations
        └── styling.js              # Dynamic styling
```

---

## 🔑 Key Components

### `app.py` - Application Server
- Handles HTTP requests and responses
- Orchestrates player search workflow
- Manages CORS for cross-origin requests

### `queries/transfermarkt_query.py` - Player Data
- Searches for players by name
- Retrieves player profiles (age, position, team, value, image)
- Filters out retired players

### `queries/fbref_query.py` - Statistical Data
- Fetches comprehensive player statistics
- Handles position-specific metrics (different stats for GK vs outfield players)
- Aggregates data across multiple stat categories

### `modules/stats_comparator.py` - Similarity Engine
- Compares searched player against all similar position players
- Returns similarity scores for ranking

### `modules/data_processing.py` - Advanced Analytics
- **Z-Score Normalization** - Standardizes stats for fair comparison
- **Cosine Similarity** - Measures angular distance between stat vectors
- Handles missing data and edge cases

### `modules/config.py` - Position Configuration
- Maps Transfermarkt positions to FBref positions
- Ensures only positionally similar players are compared
- Supports 13 different positions/roles

---

## 💡 Usage Examples

### Finding Similar Strikers
```javascript
// Search for Erling Haaland
{
  "player_name": "Erling Haaland"
}
// Returns top 10 strikers with similar goal-scoring patterns, physicality, and positioning
```

### Finding Similar Midfielders
```javascript
// Search for Bruno Fernandes
{
  "player_name": "Bruno Fernandes"
}
// Returns midfielders with comparable passing, dribbling, and playmaking stats
```

### Finding Similar Defenders
```javascript
// Search for Virgil van Dijk
{
  "player_name": "Virgil van Dijk"
}
// Returns defenders with similar defensive abilities, positioning, and passing skills
```

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python, Flask |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Data Processing** | Pandas, Scikit-learn, NumPy |
| **APIs** | FBref (SoccerData), Transfermarkt (felipeall) |
| **Statistical Methods** | Z-Score Normalization, Cosine Similarity |

---

## 📊 Supported Leagues

The tool analyzes players from the Big 5 European Leagues:

🇬🇧 **Premier League** (England)  
🇪🇸 **La Liga** (Spain)  
🇮🇹 **Serie A** (Italy)  
🇩🇪 **Bundesliga** (Germany)  
🇫🇷 **Ligue 1** (France)  

Data from the **2025-2026 season**

---

## 🎓 How Z-Score Normalization Works

For fair comparison across different player profiles:

```
Z-Score = (Player Value - League Average) / Standard Deviation

Example:
- Messi's Goals: 45 (Z-Score: +2.5)
- Average Goals: 10
- Std Dev: 14

This means Messi scored 2.5 standard deviations above the mean!
```

---

## 🐛 Error Handling

The application gracefully handles:
- ❌ Player not found in Transfermarkt database
- ❌ Retired or inactive players (automatically skipped)
- ❌ Players with insufficient statistical data
- ❌ API connectivity issues (with retry logic)
- ❌ Invalid JSON requests

---

## 🚦 Performance Considerations

- **Async Operations** - Uses Python async/await for non-blocking API calls
- **Efficient Caching** - Minimizes redundant API requests
- **Optimized Queries** - Filters data server-side before processing
- **Vectorized Calculations** - NumPy/Scikit-learn for fast numerical operations

Typical response time: **2-5 seconds** depending on API availability

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open source. Feel free to use and modify for your needs.

---

## 🙏 Acknowledgments

This project stands on the shoulders of giants:

- **[SoccerData](https://github.com/ChangeAI/soccerdata)** - For providing the FBref API wrapper to access comprehensive football statistics
- **[felipeall's Transfermarkt API](https://github.com/felipeall/transfermarkt-api)** - For the Transfermarkt API enabling player search and market value data

Without these amazing open-source projects, this tool wouldn't be possible.

---

## 📧 Contact & Support

For questions, issues, or suggestions, please open an issue on the GitHub repository.

---

**Made with ⚽ by Mattikk0**  
*Discover your player's statistical twin today!*
