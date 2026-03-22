from flask import Flask, render_template, jsonify, request, session
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ontario Fertilizer Recommendations Database
ONTARIO_SEASONS = {
    'spring': {
        'months': [4, 5],
        'name': 'Spring (Late April - May)',
        'description': 'Critical for breaking dormancy and early growth'
    },
    'early_summer': {
        'months': [6],
        'name': 'Early Summer (June)',
        'description': 'Support active growth'
    },
    'late_summer': {
        'months': [7, 8],
        'name': 'Late Summer (July - August)',
        'description': 'Light feeding to maintain vigor'
    },
    'fall': {
        'months': [9, 10],
        'name': 'Fall (September - October)',
        'description': 'Critical for root development and winter hardiness'
    },
    'early_winter': {
        'months': [11],
        'name': 'Early Winter (November)',
        'description': 'Optional: potassium-rich for winter prep'
    }
}

GRASS_TYPES = {
    'cool_season_mix': {
        'name': 'Cool-Season Mix (Kentucky Bluegrass, Rye, Fescue)',
        'region': 'Most common Ontario',
        'annual_apps': 4,
        'peak_growth': [4, 5, 9, 10],
        'summer_dormant': True
    },
    'perennial_rye': {
        'name': 'Perennial Ryegrass',
        'region': 'Ontario lawns',
        'annual_apps': 4,
        'peak_growth': [4, 5, 9, 10],
        'summer_dormant': True
    },
    'tall_fescue': {
        'name': 'Tall Fescue',
        'region': 'Ontario lawns',
        'annual_apps': 3,
        'peak_growth': [4, 5, 9, 10],
        'summer_dormant': True
    }
}

HEALTH_LEVELS = {
    'excellent': {'factor': 0.7, 'apps': 3},
    'good': {'factor': 1.0, 'apps': 4},
    'fair': {'factor': 1.3, 'apps': 5},
    'poor': {'factor': 1.6, 'apps': 5}
}



# Fertilizer recommendations for different scenarios
def get_fertilizer_recommendation(grass_type, health, soil_test, lawn_size):
    """
    Generate Ontario-specific fertilizer recommendations
    """
    recommendations = []
    
    grass_info = GRASS_TYPES.get(grass_type, GRASS_TYPES['cool_season_mix'])
    health_factor = HEALTH_LEVELS.get(health, HEALTH_LEVELS['good'])
    
    # Parse soil test (NPK levels: 0-30 scale, where 15 is optimal)
    try:
        n_level, p_level, k_level = soil_test.split(',')
        n_level = int(n_level.strip())
        p_level = int(p_level.strip())
        k_level = int(k_level.strip())
    except:
        n_level, p_level, k_level = 15, 15, 15  # Default = balanced
    
    lawn_size_num = float(lawn_size)
    
    # Spring Application (Late April - May)
    spring_app = {
        'season': 'Spring (Late April - May)',
        'month': 5,
        'timing': 'When soil reaches 60°F (around late April)',
        'why': 'Breaks dormancy and supports new growth',
        'npk': '30-0-10',
        'name': 'Spring Lawn Starter',
        'description': 'High nitrogen for leaf growth',
        'rate_per_1000': 0.5,
        'total_lbs': round(lawn_size_num * 0.5 / 1000, 1),
        'products': [
            'Scotts Turf Builder Early Spring',
            'Tomlinson Fertilizer Spring Mix',
            'Local Ontario supplier blends'
        ]
    }
    recommendations.append(spring_app)
    
    # Early Summer (June) - Light application
    if health in ['fair', 'poor']:
        early_summer_app = {
            'season': 'Early Summer (June)',
            'month': 6,
            'timing': 'Early June',
            'why': 'Light feeding to support growth without stress',
            'npk': '15-0-15',
            'name': 'Summer Maintenance',
            'description': 'Balanced nitrogen and potassium',
            'rate_per_1000': 0.3,
            'total_lbs': round(lawn_size_num * 0.3 / 1000, 1),
            'products': [
                'Scotts Turf Builder Maintenance',
                'Local blended mix'
            ]
        }
        recommendations.append(early_summer_app)
    
    # Late Summer Application (July - August) - LIGHT
    if health != 'poor':
        late_summer_app = {
            'season': 'Late Summer (July - August)',
            'month': 8,
            'timing': 'Mid-August preferred (less stress)',
            'why': 'Minimal feeding; focus on watering instead',
            'npk': '10-0-20',
            'name': 'Late Summer Light Application',
            'description': 'Potassium-focused for stress tolerance',
            'rate_per_1000': 0.2,
            'total_lbs': round(lawn_size_num * 0.2 / 1000, 1),
            'products': [
                'Potassium supplement',
                'Local blended mix'
            ]
        }
        recommendations.append(late_summer_app)
    
    # Fall Application - MOST IMPORTANT (Sept-Oct)
    fall_app = {
        'season': 'Fall (September - October)',
        'month': 10,
        'timing': 'Late September or early October',
        'why': 'CRITICAL: Promotes root development and winter hardiness',
        'npk': '25-0-25',
        'name': 'Fall Lawn Winterizer',
        'description': 'High potassium for root strength and winter survival',
        'rate_per_1000': 0.5,
        'total_lbs': round(lawn_size_num * 0.5 / 1000, 1),
        'products': [
            'Scotts Turf Builder WinterGuard',
            'Tomlinson Winterizer',
            'Local Ontario winter prep blends'
        ]
    }
    recommendations.append(fall_app)
    
    # Early Winter Optional (November)
    if health in ['good', 'excellent']:
        winter_app = {
            'season': 'Early Winter (November)',
            'month': 11,
            'timing': 'Early November before freeze',
            'why': 'Optional: Extra potassium for winter survival',
            'npk': '0-0-60',
            'name': 'Winter Preparation - Potassium boost',
            'description': 'Pure potassium application',
            'rate_per_1000': 0.15,
            'total_lbs': round(lawn_size_num * 0.15 / 1000, 1),
            'products': [
                'Potassium chloride',
                'Local suppliers'
            ]
        }
        recommendations.append(winter_app)
    
    # Soil-based adjustments
    adjustments = []
    if n_level < 12:
        adjustments.append("Your soil is LOW in nitrogen. Ensure full-strength spring and fall applications.")
    if p_level > 20:
        adjustments.append("Your soil has HIGH phosphorus. Avoid P in future applications (use 0-0-K formulas).")
    if k_level < 12:
        adjustments.append("Your soil is LOW in potassium. Emphasize potassium in fall (use products with higher K numbers).")
    
    return {
        'recommendations': recommendations,
        'grass_info': grass_info,
        'health_info': f"Lawn Health: {health.title()}",
        'soil_adjustments': adjustments,
        'annual_apps_count': len(recommendations)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-recommendations', methods=['POST'])
def get_recommendations():
    """Get fertilizer recommendations"""
    data = request.json
    grass_type = data.get('grassType', 'cool_season_mix')
    health = data.get('lawnHealth', 'good')
    soil_test = data.get('soilTest', '15,15,15')
    lawn_size = data.get('lawnSize', '5000')
    
    recommendations = get_fertilizer_recommendation(grass_type, health, soil_test, lawn_size)
    return jsonify(recommendations)

@app.route('/api/save-application', methods=['POST'])
def save_application():
    """Save an application to history"""
    data = request.json
    
    if 'applications' not in session:
        session['applications'] = []
    
    app_record = {
        'date': datetime.now().isoformat(),
        'season': data.get('season'),
        'fertilizer': data.get('fertilizer'),
        'amount': data.get('amount'),
        'notes': data.get('notes', '')
    }
    
    session['applications'].append(app_record)
    session.modified = True
    
    return jsonify({'success': True, 'applications': session.get('applications', [])})

@app.route('/api/get-applications', methods=['GET'])
def get_applications():
    """Get saved applications"""
    apps = session.get('applications', [])
    return jsonify({'applications': apps})

@app.route('/api/get-calendar', methods=['GET'])
def get_calendar():
    """Get the full-year fertilizer calendar for Ontario"""
    current_year = datetime.now().year
    calendar = []
    
    for season_key, season_info in ONTARIO_SEASONS.items():
        for month in season_info['months']:
            calendar.append({
                'month': month,
                'season': season_key,
                'name': season_info['name'],
                'description': season_info['description'],
                'date': f"{current_year}-{month:02d}-15"
            })
    
    return jsonify({'calendar': calendar})

if __name__ == '__main__':
    app.run(debug=True)
