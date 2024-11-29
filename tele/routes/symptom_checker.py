from flask import Blueprint, render_template

symptom_checker_bp = Blueprint('symptom_checker', __name__)

@symptom_checker_bp.route('/symptom-checker', methods=['GET'])
def symptom_checker():
    """
    Route to display the symptom checker integration page.
    """
    return render_template('symptom_checker.html')
