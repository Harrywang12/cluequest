from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
import os
from groq import Groq

bp = Blueprint('game', __name__)
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@bp.route('/')
@login_required
def index():
    return render_template('game/index.html')

@bp.route('/generate_story', methods=['POST'])
@login_required
def generate_story():
    level = current_user.progress + 1
    difficulty = "Medium"  # You can adjust this based on level
    
    prompt = f"""Create a detective story for level {level} with:
- A setting (e.g., mansion, park, office)
- A description of what crime happened
- A victim and their backstory
- 4 suspects, each with motives and alibis
- {max(3 - level // 5, 1)} key clues
- {2 + level // 5} red herrings
- One culprit
- An explanation of why the culprit committed the crime
- Make it a {difficulty} difficulty level"""

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=1024,
    )

    story = completion.choices[0].message.content
    return jsonify({"story": story})

@bp.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
    current_user.progress += 1
    db.session.commit()
    return jsonify({"progress": current_user.progress}) 