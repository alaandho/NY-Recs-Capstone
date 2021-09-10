from flask import Blueprint, render_template, request
from flask_login import login_required
from capstone_inventory.models import Recs

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
# @site.route('/<cat>', defaults = {'cat': None} )
def home():
    cat = request.args.get('cat')
    print(cat)
    if not cat:
        recommendations = Recs.query.all()
    else:
        recommendations = Recs.query.filter_by(category = cat).all()
        print(recommendations)
    return render_template('index.html', recommendations = recommendations)


@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



