from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from core.models import Article, User
from core.forms import SearchForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    search_form = SearchForm()
    if current_user.is_authenticated:
        # Display personalized recommendations for logged-in users
        recommended_articles = Article.get_recommended_articles(current_user)
    else:
        # Display popular articles for anonymous users
        recommended_articles = Article.get_popular_articles()

    return render_template('index/index.html', articles=recommended_articles, search_form=search_form)

@main_bp.route('/article/<int:article_id>')
def article_detail(article_id):
    # article = Article.query.get(article_id)
    # if article is None:
    #    flash('Article not found', 'danger')
    #    return redirect(url_for('main.index'))

    content = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu bibendum dolor. Maecenas sit amet neque non tortor condimentum tincidunt vitae sodales sem. Nunc venenatis, metus ac ultrices vulputate, eros ante tristique quam, pulvinar euismod dui mi vitae nibh. Nunc iaculis suscipit velit, et convallis elit scelerisque egestas. Nullam vehicula magna eget tellus porta, vitae luctus urna tempor. Maecenas posuere leo nec odio maximus elementum. Ut arcu nisl, luctus ac lorem in, porttitor consequat libero. Donec orci nunc, maximus a bibendum non, aliquam ut velit. Vestibulum quis mollis mi.

Proin ullamcorper a enim id ultricies. Nunc augue sapien, iaculis a nisl at, fringilla tempor felis. Praesent vitae arcu at nulla bibendum facilisis. In aliquam rhoncus ex, et aliquet velit elementum vitae. Nulla facilisi. Sed consectetur at felis eget viverra. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec elementum, sem sodales bibendum efficitur, neque urna dapibus lorem, non commodo leo dui quis erat. Quisque vestibulum, felis sit amet porta fermentum, nisl ex eleifend lacus, a maximus felis metus sit amet eros. Vestibulum semper eros non ligula interdum, sed sodales odio scelerisque. Vivamus tempus, velit in rhoncus molestie, justo nisi fringilla neque, in ultricies ex diam eget justo. Aenean faucibus malesuada euismod. Proin pretium ligula quis congue euismod. Praesent pulvinar rutrum diam vel elementum. Sed justo libero, molestie vel arcu eget, volutpat condimentum purus.

Donec posuere aliquam sapien, ut imperdiet nibh. Aenean gravida leo elementum, vulputate nulla eu, luctus risus. Duis vitae purus lectus. Fusce dapibus sed lectus et tempor. Nulla facilisi. Donec quis pellentesque est, et tempus justo. Integer ut semper ex. Integer ultricies, elit vitae tempor interdum, arcu mauris consequat velit, sed convallis metus eros eget nibh. Maecenas condimentum tristique auctor. Quisque egestas lorem dolor.

Ut ornare, massa eu consequat accumsan, ipsum diam ultricies elit, et condimentum eros velit vel leo. Pellentesque a risus lorem. Suspendisse aliquet bibendum consectetur. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nam tristique ipsum felis, non aliquam velit viverra sed. Vestibulum iaculis sed massa ac lacinia. Nullam nisi nulla, viverra at sapien sit amet, convallis egestas felis. Proin gravida lacus dolor, eget pellentesque mauris convallis at. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.

Nulla ante magna, auctor a felis ac, feugiat tincidunt urna. Nulla facilisi. Nullam condimentum scelerisque volutpat. Duis posuere viverra aliquam. Nam ullamcorper nibh vitae elit maximus fringilla. Donec imperdiet lacus ac lectus condimentum posuere. Mauris lobortis, arcu sed ullamcorper rutrum, eros turpis pulvinar metus, sit amet rutrum elit nulla sit amet mauris. Nunc sed arcu neque. Curabitur arcu nisl, facilisis nec risus id, maximus fringilla ligula. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    '''

    return render_template('index/article_detail.html',
                           title='Sample Article Title',
                           content=content)

@main_bp.route('/profile')
@login_required
def user_profile():
    favorited_articles = current_user.get_favorited_articles()
    viewed_articles = current_user.get_viewed_articles()
    shared_articles = current_user.get_shared_articles()

    return render_template('user_profile.html', favorited_articles=favorited_articles, viewed_articles=viewed_articles, shared_articles=shared_articles)

@main_bp.route('/search', methods=['POST'])
def search():
    search_form = SearchForm(request.form)
    if search_form.validate():
        search_results = Article.search_articles(search_form.keywords.data)
        return render_template('search_results.html', search_results=search_results, search_form=search_form)

    flash('Invalid search query', 'danger')
    return redirect(url_for('main.index'))