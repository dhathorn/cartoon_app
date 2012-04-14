from cartoon_app import app
from flask import Flask, request, session, redirect, url_for, \
             render_template, flash, make_response, abort
from models import *
from forms import *
from login_manager import login_manager
from flask.ext.login import login_user, login_required, logout_user

#user views
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.email == form.email.data).first()
        login_user(user)
        flash('You were logged in')
        return redirect(url_for('admin'))
    return render_template('login.html', form=form)

@app.route('/admin')
@login_required
def admin():
    data = Experiment.query.all()
    rv = "id\tstarted\t\t\t\tcompleted\t\t\thitId\tasgnId\timg 0\timg 1\timg 2\timg 3\timg 4\timg 5\timg 6\timg 7\timg 8\timg 9\timg 10\timg 11\n"
    for e in data:
        rv += e.string_format()
    resp = make_response(rv)
    resp.mimetype = "text/plain"
    return resp

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login'))

#experiment logic
instructions = """
We are going to ask you to answer questions about images. We will ask you if you think the images you view are hand drawn, or photographs. All images are generic scenes, and there are no offensive or graphic images.
"""
preview = """
You will be asked to make 12 different selections of this type. To proceed, select Accept HIT
"""

@app.route('/done')
def done():
    #this will prevent double submissions of the form if the user logs out and back into mturk with a diffrent user account
    if 'guard' in session:
        abort(401)
    if session.get('complete'):
        session['guard'] = True
        experiment = Experiment.query.get_or_404(session.get('id'))
        experiment.complete()
        db.session.commit()
        return render_template('finish.html')
    else:
        return redirect(url_for('experiment'))

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        if 'assignmentId' not in request.args or request.args['assignmentId'] == 'ASSIGNMENT_ID_NOT_AVAILABLE':
            #this is the preview
            flash(instructions)
            flash(preview)
            return render_template('experiment.html', form=ExperimentForm(),
                                   percent=0.0, picture='1.jpg')
        else:
            session['assignmentId'] = request.args['assignmentId']
            session['hitId'] = request.args['hitId']
    form = StartForm(request.form)
    if request.method == 'POST':
        if form.validate():
            experiment = Experiment(session['hitId'], session['assignmentId'])
            experiment.start()
            db.session.add(experiment)
            db.session.commit()
            session['id'] = experiment.id
            session['picture'] = 0
            flash('The experiment has now begun, rate the following photos based on how much they look like cartoons')
            return redirect(url_for('experiment'))
    return render_template('start.html', form=form)

@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if 'id' not in session:
        return redirect(url_for('start'))
    form = ExperimentForm(request.form)
    if request.method == 'POST':
        if form.validate():
            experiment = Experiment.query.get(session['id'])
            setattr(experiment, "img_%d" % session['picture'], int(form.choice.data))
            db.session.commit()
            session['picture'] += 1
            if session['picture'] == 12:
                session['complete'] = True
                return redirect(url_for('done'))

    percent = float(session['picture'] / 0.12)
    form.choice.data = None
    return render_template('experiment.html', form=form,
                            percent=percent, picture=("%s.jpg" %session['picture']))
