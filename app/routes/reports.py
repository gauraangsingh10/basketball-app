from flask import Blueprint, render_template, make_response, redirect, url_for, flash
from xhtml2pdf import pisa
from io import BytesIO
from ..models import Player, Stat, Game
from flask_login import login_required, current_user

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/team_stats_pdf')
@login_required
def team_stats_pdf():
    team = current_user.team
    if not team:
        flash("No team found to generate report.", "warning")
        return redirect(url_for('teams.team_stats'))

    players = team.players
    games = team.games

    # Render HTML from template
    rendered = render_template('pdf/team_stats_pdf.html', team=team, players=players, games=games)
    
    # Generate PDF
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf)
    if pisa_status.err:
        return "PDF generation failed", 500

    # Return as downloadable file
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=team_stats.pdf'
    return response
