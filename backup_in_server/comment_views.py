from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect

from zelda import db
from ..forms import CommentForm
from zelda.models import Post, Comment

from zelda.views.auth_views import Comment_login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:post_id>', methods=('POST',))
@Comment_login_required
def create(post_id):
  form = CommentForm()
  post = Post.query.get_or_404(post_id)
  if form.validate_on_submit():
    content = request.form['content']
    comment = Comment(content=content, create_date=datetime.now(), user=g.user)
    post.comment_set.append(comment)
    db.session.commit()
    return redirect(url_for('main.detail', post_id = post_id))
  return render_template('post_detail.html', post=post, form=form)
	#post = Post.query.get_or_404(post_id)
	#content = request.form['content']
	#comment = Comment(question=post, content=content, create_date=datetime.now())
	#db.session.add(comment)
	#db.session.commit()
	#return redirect(url_for('main.detail', post_id = post_id))
