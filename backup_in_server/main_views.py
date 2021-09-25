from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g
from zelda.models import Post
from ..forms import PostForm, CommentForm
from werkzeug.utils import redirect
from zelda import db  
from zelda.views.auth_views import Post_login_required

bp = Blueprint('main',__name__, url_prefix='/')


@bp.route('/')
def main():
	
    return render_template('main.html')

@bp.route('/board')
def board():
	post_list = Post.query.order_by(Post.create_date.desc())
	return render_template('post_list.html', post_list=post_list)

@bp.route('/detail/<int:post_id>/')
def detail(post_id): #매개변수에는 <int:post_id>가 들어감 
  form = CommentForm()
  post = Post.query.get_or_404(post_id)
  return render_template('post_detail.html', post=post, form=form)
 
@bp.route('/create', methods=('GET', 'POST'))
@Post_login_required
def create(): #수정 
  form = PostForm()
  if request.method == 'POST' and form.validate_on_submit():
    post = Post(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('main.board'))
  return render_template('post_form.html', form=form)
	

