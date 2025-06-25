from flask_login import current_user

@games_bp.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        opponent = request.form['opponent']
        location = request.form['location']
        result = request.form['result']
        team_score = int(request.form['team_score'])
        opponent_score = int(request.form['opponent_score'])

        team_id = current_user.team_id

        new_game = Game(
            date=date,
            opponent=opponent,
            location=location,
            result=result,
            team_score=team_score,
            opponent_score=opponent_score,
            team_id=team_id
        )
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('games.games'))

    # ❌ No need to show all teams — it's only the current user's team
    return render_template("add_game.html")
