from flask.helpers import flash
from flask.templating import render_template
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from .models import User, Deck, Card
from . import db
from flask import current_app as app
import werkzeug
from flask import abort, redirect, url_for
from werkzeug.security import generate_password_hash

import random


user_post_args = reqparse.RequestParser()
user_post_args.add_argument('username')
user_post_args.add_argument('password')

card_put_args = reqparse.RequestParser()
card_put_args.add_argument('score')

deck_post_args = reqparse.RequestParser()
deck_post_args.add_argument('deck_name')

card_post_args = reqparse.RequestParser()
card_post_args.add_argument('front')
card_post_args.add_argument('back')


class UserAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()
        u = User.query.filter_by(username=args['username']).first()
        if u:
            return "User already exists",409

        errors={}
        if len(args['username']) < 6:
            errors["USER001"]="Username is too short"
        if len(args['password']) < 6:
            errors["USER002"]="Password is too short"
        if errors !={}:
            return errors,400
        
        new_user = User(username=args['username'], password = generate_password_hash(args['password'], method='sha256'))
        try:
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            user=User.query.filter_by(username=args['username']).first()
            return {"id":user.id,"username":user.username},201
        except:
            return "Internal Server Error",500

    def get(self, username):
        try:
            u = User.query.filter_by(username=username).first()
            if u == None:
                return "User not found",404
            d = Deck.query.filter_by(user=username)
            dn = d.count()
            score=[deck.score for deck in d]
            return{
                "username": u.username,
                "deck_count": dn,
                "score": score
            },200
        except:
            return "Internal Server Error",500







class DeckAPI(Resource):
    def post(self, username):
        try:
            args = deck_post_args.parse_args()
            qd = Deck.query.filter_by(user=username,deck_name=args['deck_name']).first()
            if qd!=None:
                return {"id":qd.id,"deck_name":qd.deck_name,"user":qd.user},409
            
            d = Deck(deck_name=args['deck_name'], user=username)
            db.session.add(d)
            db.session.commit()
            deck=Deck.query.filter_by(deck_name=args['deck_name'],user=username).first()
            return {"id":deck.id,"deck_name":deck.deck_name,"user":deck.user},201
        except:
            return "Internal Server Error",500

    def get(self, username):
        try:
            u=User.query.filter_by(username=username).first()
            if u==None:
                return "User not found",404
            decks = Deck.query.filter_by(user=username)
            r=[]
            for deck in decks:
                r.append({'deck_name':deck.deck_name, 'score':deck.score, 'last_rev':str(deck.last_rev)})
            return r,200
        except:
            return "Internal Server Error",500
    




class   CardAPI(Resource):
    def post(self, deck,username):
        try:
            args = card_post_args.parse_args()
            DECK=Deck.query.filter_by(deck_name=deck).first()
            if DECK==None:
                return "Deck not found",404
            old_card=Card.query.filter_by(front=args['front'], back = args['back'], deck=DECK.deck_name).first()
            if old_card!=None:
                return "Card already exists",409
            new_card=Card(front=args['front'], back = args['back'], deck=DECK.deck_name)
            db.session.add(new_card)
            db.session.commit()
            card=Card.query.filter_by(front=args['front'], back = args['back'], deck=DECK.deck_name).first()
            return {"id":card.card_id,"front":card.front,"back":card.back,"deck":card.deck},201
        except:
            return "Internal Server Error",500

    def get(self, deck, username):
        try:
            decks = Deck.query.filter_by(user=username).first()
            if decks==None:
                return "Deck not found",404
            cards = Card.query.filter_by(deck=deck).all()
            cl=[]
            if cards:
                for c in cards:
                    cl.append(c)
                random.shuffle(cl)
                rc = cl.pop()
                return {
                    "card_id": rc.card_id,
                    "deck": rc.deck,
                    "front": rc.front,
                    "back": rc.back
                }
                return cl,200
            return "No cards found",404
        except:
            return "Internal Server Error",500

    def put(self, card_id):
        try:
            c=Card.query.filter_by(card_id=card_id).first()
            if c==None:
                return "Card not found",404
            args=card_put_args.parse_args()
            c.score = args['score']
            db.session.commit()
            card=Card.query.filter_by(card_id=card_id).first()
            return {"front":card.front,"back":card.back,"deck":card.deck,"score":card.score},200
        except:
            return "Internal Server Error",500    
        
