from flask import Blueprint, render_template

app_view = Blueprint('app_view', __name__,
                        template_folder='templates')


@app_view.route('/dashboard')
def index():
    return render_template("dashboard.html")
