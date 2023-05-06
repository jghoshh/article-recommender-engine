from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from textblob import TextBlob
from datetime import datetime
from core.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('username', 'email', name='unique_username_email'),
    )

    favorite_articles = db.relationship('Article', secondary='favorite_article', backref='favorited_by')
    viewed_articles = db.relationship('Article', secondary='viewed_article', backref='viewed_by')
    shared_articles = db.relationship('Article', secondary='shared_article', backref='shared_by')
    user_recommendations = db.relationship('Article', secondary='recommendation', backref='recommended_to')
    comments = db.relationship('Comment', backref='author')

    def set_password(self, password):
        if len(password) < 8:
            raise ValueError('Password should be at least 8 characters long')
        if password.isnumeric() or password.isalpha() or password.islower() or password.isupper():
            raise ValueError('Password should contain both uppercase and lowercase letters, numbers and special characters')
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def does_user_exist(username):
        return db.query.filter_by(username=username).first() is not None
    
    @classmethod
    def does_email_exist(email):
        return db.query.filter_by(email=email).first() is not None

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False, index=True)
    url = db.Column(db.String(512), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False, index=True)
    polarity = db.Column(db.Float, nullable=False)
    subjectivity = db.Column(db.Float, nullable=False)
    click_through_rate = db.Column(db.Float, nullable=False, default=0.05)
    engagement_rate = db.Column(db.Float, nullable=False, default=0.05)
    shares = db.Column(db.Integer, nullable=False, default=10)
    likes = db.Column(db.Integer, nullable=False, default=10)
    dislikes = db.Column(db.Integer, nullable=False, default=2)
    views = db.Column(db.Integer, nullable=False, default=100)
    saves = db.Column(db.Integer, nullable=False, default=10)
    recommendation_count = db.Column(db.Integer, nullable=False, default=0)
    
    recommendations = db.relationship('User', secondary='recommendation', backref='recommended_articles')
    comments = db.relationship('Comment', backref='article')

    def calculate_sentiment(self):
        blob = TextBlob(self.content)
        self.polarity = blob.sentiment.polarity
        self.subjectivity = blob.sentiment.subjectivity
    
    @staticmethod
    def get_recommended_articles(user):
        # Replace with actual business logic later
        dummy_articles = [
            {
                'id': 1,
                'title': 'Recommended Article 1',
                'summary': 'This is a summary of the recommended article 1.',
            },
            {
                'id': 2,
                'title': 'Recommended Article 2',
                'summary': 'This is a summary of the recommended article 2.',
            },
            {
                'id': 3,
                'title': 'Recommended Article 3',
                'summary': 'This is a summary of the recommended article 3.',
            }
        ]
        return dummy_articles

    @staticmethod
    def get_popular_articles():
        # Replace with actual business logic later
        dummy_articles = [
            {
                'id': 1,
                'title': 'BlueSky: News or Horror?',
                'summary': 'This is a summary of the popular article 1.',
            },
            {
                'id': 2,
                'title': 'Popular Article 2',
                'summary': 'This is a summary of the popular article 2.',
            },
            {
                'id': 3,
                'title': 'Popular Article 3',
                'summary': 'This is a summary of the popular article 3.',
            }
        ]
        return dummy_articles

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False, index=True)
    read_time = db.Column(db.Integer, nullable=False)
    scroll_depth = db.Column(db.Float, nullable=False, default=0.0)
    rating = db.Column(db.Integer, nullable=True)
    last_interaction_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref='interactions')
    article = db.relationship('Article', backref='interactions')
    comments = db.relationship('Comment', backref='interaction')

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating is not None and (rating < 1 or rating > 5):
            raise ValueError('Rating must be between 1 and 5')
        return rating

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), nullable=False, index=True)
    interaction_id = db.Column(db.Integer, db.ForeignKey('interaction.id', ondelete='CASCADE'), nullable=False, index=True)
    polarity = db.Column(db.Float, nullable=False)
    subjectivity = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def calculate_sentiment(self):
        blob = TextBlob(self.content)
        self.polarity = blob.sentiment.polarity
        self.subjectivity = blob.sentiment.subjectivity

# Association tables for many to many relationship between users and articles.
favorite_article = db.Table('favorite_article',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), primary_key=True)
)

viewed_article = db.Table('viewed_article',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), primary_key=True)
)

shared_article = db.Table('shared_article',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), primary_key=True),
    db.Column('platform', db.String(64), nullable=False, primary_key=True)
)

recommendation = db.Table('recommendation',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), primary_key=True),
    db.Column('recommended_on', db.DateTime, nullable=False, default=datetime.utcnow)
)