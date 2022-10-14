from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "user_accnt"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(345), unique=True)
    first_name = db.Column(db.String(20), unique=False)
    last_name = db.Column(db.String(20), unique=False)
    password = db.Column(db.Text, nullable=False)
    user_role=db.Column(db.String(10),nullable=False)
    backtest_scenes = db.relationship('BackTestScene', backref='User')


class BackTestScene(db.Model):
    __tablename__ = "backtestscene"
    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(20), unique=False)
    start_date = db.Column(db.String(20), unique=False)
    end_date = db.Column(db.String(20), unique=False)
    ema_value = db.Column(db.String(20), unique=False)
    sma_value = db.Column(db.String(20), unique=False)
    fma_value = db.Column(db.String(20), unique=False)
    initial_cash = db.Column(db.String(20), unique=False)
    fee = db.Column(db.String(20), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_accnt.id'))


class BackTestResult(db.Model):
    __tablename__ = "backtestresult"
    id = db.Column(db.Integer, primary_key=True)
    returns = db.Column(db.String(20), unique=False)
    number_of_trades = db.Column(db.String(20), unique=False)
    winning_trades = db.Column(db.String(20), unique=False)
    losing_trades = db.Column(db.String(20), unique=False)
    max_drawdown = db.Column(db.String(20), unique=False)
    sharpe_ratio = db.Column(db.String(20), unique=False)
    backtest_scene_id = db.Column(db.Integer, db.ForeignKey('backtestscene.id'))
    backtest_scene = db.relationship("BackTestScene", backref=db.backref("backtestscene", uselist=False))
