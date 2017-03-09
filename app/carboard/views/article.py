from flask import (
    render_template, request, flash, redirect, url_for
)
from flask_login import login_required

from . import carboard
from ..models.article import Article
from ..forms.article import ArticleForm
from ..constants import PER_PAGE
from ...extensions import db

# -------------------- /carboard/article/ : List of articles ---------------- #


@carboard.route('/article/')
@login_required
def indexArticle():
    articles = Article.query.paginate(
        page=request.args.get('page', 1, type=int),
        per_page=request.args.get('per_page', PER_PAGE, type=int),
    )
    return render_template('carboard/article/index.html', articles=articles)

# -------------------- /carboard/article/id : Show article ------------------ #


@carboard.route('/article/<int:id>', methods=['GET'])
@login_required
def showArticle(id):
    article = Article.query.get_or_404(id)
    return render_template('carboard/article/show.html', article=article)

# -------------------- /carboard/article/new : Add article ------------------ #


@carboard.route('/article/new/<int:dataset_id>', methods=['GET', 'POST'])
@carboard.route('/article/new', methods=['GET', 'POST'])
@login_required
def newArticle(dataset_id=None):
    """ Add new article """

    form = ArticleForm()

    if form.validate_on_submit():
        article = Article(
            dataset_id=dataset_id,
            name=form.name.data,
            authors=form.authors.data,
            abstract=form.abstract.data,
            keywords=form.keywords.data,
            publication_date=form.publication_date.data,
            reference=form.reference.data,
            link=form.link.data,
        )
        db.session.add(article)
        db.session.commit()
        flash('Article {}, added successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.indexArticle'))

    return render_template('carboard/article/new.html', form=form, dataset_id=dataset_id)

# -------------------- /carboard/article/id/edit : Edit article ------------- #


@carboard.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editArticle(id):
    """ Edit existing article """

    article = Article.query.get_or_404(id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        flash('Article {}, updated successfully.'.format(form.name.data), 'success')
        return redirect(url_for('carboard.showArticle', id=id))

    return render_template('carboard/article/edit.html', form=form, id=id)

# -------------------- /carboard/article/id/delete : Delete article --------- #


@carboard.route('/article/<int:id>/delete', methods=['GET'])
@login_required
def deleteArticle(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    flash('Article {}, deleted successfully.'.format(article.name), 'success')
    return redirect(url_for('carboard.indexArticle'))
