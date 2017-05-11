import json
import csv
from os.path import basename
from importlib import import_module
from threading import Thread
import traceback
from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required, current_user

from . import carboard
from ..models.dataset import Dataset
from ..models.file import File
from ..forms.dataset import DatasetForm, FeedDatasetForm
from ..helpers import upload_dsfile
from ..constants import PER_PAGE
from ...extensions import db

# -------------------- /carboard/dataset/ : List of datasets ---------------- #


@carboard.route('/dataset/')
@login_required
def indexDataset():
    datasets = Dataset.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/dataset/index.html', datasets=datasets)

# -------------------- /carboard/dataset/id : Show dataset ------------------ #


@carboard.route('/dataset/<int:id>', methods=['GET'])
@login_required
def showDataset(id):
    dataset = Dataset.query.get_or_404(id)
    return render_template('carboard/dataset/show.html', dataset=dataset)

# -------------------- /carboard/dataset/new : Add dataset ------------------ #


@carboard.route('/dataset/new', methods=['GET', 'POST'])
@login_required
def newDataset():
    """ Add new dataset """

    form = DatasetForm()

    if form.validate_on_submit():
        dataset = Dataset(
            name=form.name.data,
            description=form.description.data,
            author=form.author.data,
            lab=form.lab.data,
            website=form.website.data,
        )
        db.session.add(dataset)
        db.session.commit()
        flash('Dataset {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexDataset'))

    return render_template('carboard/dataset/new.html', form=form)

# -------------------- /carboard/dataset/id/edit : Edit dataset ------------- #


@carboard.route('/dataset/feed/<int:id>', methods=['GET', 'POST'])
@login_required
def feedDataset(id):
    """ Fill dataset with data that may come from diff sources """

    dataset = Dataset.query.get_or_404(id)

    form = FeedDatasetForm()

    if form.validate_on_submit():
        files = request.form.getlist('files')
        try:
            # Dataset slug a.k.a module name
            slug = dataset.slug
            # Import the module
            mod = import_module(".elastic", 'app.importer.datasets.' + slug)
            # Indexing function
            index_function = 'index_bulk'  # 'index'
            # get a reference to the init function
            init = getattr(mod, index_function)
            # create a threaded job to index uploaded data according to it's dataset
            thread = Thread(target=init, args=[files, dataset, current_user.id])
            thread.daemon = True
            thread.start()
            # thread.join(1)
            # print(active_count())
            flash('Files added to Dataset "{}" are being indexed in background.'.format(dataset.name), 'success')
        except ImportError:
            flash('No dataset indexer is provided!', 'error')
        except Exception as err:
            flash('Something went wrong while trying to indexed dataset files!', 'error')
            traceback.print_exc()
            # raise
        # raise
        return redirect(url_for('carboard.indexDataset'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ), 'error')

    return render_template(
        'carboard/dataset/feed.html',
        form=form,
        dataset=dataset
    )

# -------------------- /carboard/dataset/id/edit : Edit dataset ------------- #


@carboard.route('/dataset/getfile/<int:id>', methods=['POST'])
@login_required
def getFileDataset(id):
    """ Handle multiple dataset file uploads """

    dataset = Dataset.query.get_or_404(id)
    if request.method == 'POST':
        trace = upload_dsfile('file', dataset.slug)
        file = File(
            user_id=current_user.id,
            filename=basename(trace['message']),
            path=trace['message']
        )
        db.session.add(file)
        db.session.commit()
        return json.dumps(trace)

# -------------------- /carboard/dataset/id/edit : Edit dataset ------------- #


@carboard.route('/dataset/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editDataset(id):
    """ Edit existing dataset """
    dataset = Dataset.query.get_or_404(id)
    form = DatasetForm(obj=dataset)
    if form.validate_on_submit():
        form.populate_obj(dataset)
        db.session.commit()
        flash('Dataset {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showDataset', id=id))

    return render_template('carboard/dataset/edit.html', form=form, id=id)

# -------------------- /carboard/dataset/id/delete : Delete dataset --------- #


@carboard.route('/dataset/<int:id>/toggle', methods=['GET'])
@login_required
def toggleDataset(id):
    dataset = Dataset.query.get_or_404(id)
    # getattr(dataset, 'status', 0)
    status = dataset.status if dataset.status is not None else 0
    dataset.status = 1 - status
    db.session.commit()
    msg = 'activated' if dataset.status is 1 else 'deactivated'
    flash('Dataset {}, {} successfully.'.format(dataset.name, msg), 'success')
    return redirect(url_for('carboard.indexDataset'))

# -------------------- /carboard/dataset/id/delete : Delete dataset --------- #


@carboard.route('/dataset/<int:id>/delete', methods=['GET'])
@login_required
def deleteDataset(id):
    dataset = Dataset.query.get_or_404(id)
    db.session.delete(dataset)
    db.session.commit()
    flash('Dataset {}, deleted successfully.'.format(dataset.name), 'success')
    return redirect(url_for('carboard.indexDataset'))
