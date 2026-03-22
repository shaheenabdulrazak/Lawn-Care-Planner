# Ontario Lawn Fertilizer Planner

A personalized lawn care application designed specifically for Ontario homeowners. Get customized fertilizer schedules based on your grass type, lawn health, soil conditions, and lawn size.

## Features

✅ **Personalized Recommendations**
- Customized to Ontario's climate and grass types
- Based on lawn health assessment and soil test results
- Accounts for seasonal growth patterns

✅ **Four Main Grass Types**
- Cool-Season Mix (Kentucky Bluegrass, Rye, Fescue) - Most Common
- Perennial Ryegrass
- Tall Fescue
- Custom recommendations for each

✅ **Comprehensive Tools**
- **Planner**: Get detailed fertilizer recommendations
- **Calendar**: See your full-year fertilizer schedule
- **Track Applications**: Record and save your fertilizer applications
- **Reminders**: Get alerts for optimal application times

✅ **Beautiful, Responsive UI**
- Clean, easy-to-use interface
- Mobile-friendly design
- Green theme matching lawn care theme
- Real-time recommendations

## Installation

1. **Install Python 3.8+**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the App

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser:**
   - Go to `http://localhost:5000`
   - Enter your lawn details and get started

## How to Play

1. **Place Your Bet:**
   - Enter bet amount (minimum $10)
   - Use quick bet buttons ($50, $100, $500)
   - Click "Deal" button

2. **Play Your Hand:**
   - **Hit**: Draw another card
   - **Stand**: Keep your current hand and let dealer play
   - **Double Down**: Double your bet and take exactly one more card

3. **Game Results:**
   - Win: Beat dealer's hand
   - Lose: Go over 21 or dealer has higher hand
   - Push: Tie with dealer (get your bet back)

## Game Rules

- **Blackjack**: 21 with first two cards = 1.5x payout
- **Push**: Tie with dealer = Get your bet back
- **Bust**: Over 21 = You lose
- **Dealer Rules**: Must hit on 16, must stand on 17+

## Game Balance

- Starting balance: $1,000
- Game runs in browser using Flask sessions
- History saved to browser's localStorage

## File Structure

```
BlackJack/
├── app.py                 # Flask backend with game logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main game page
└── static/
    ├── style.css         # Game styling
    └── game.js           # Frontend game logic
```

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Game Logic**: Object-oriented Python classes
- **Session Management**: Flask sessions
- **Data Storage**: LocalStorage (browser history)

## Enjoy! 🎰
