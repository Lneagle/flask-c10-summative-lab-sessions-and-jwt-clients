#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from config import db, app
from models import User, Post

fake = Faker()

with app.app_context():
    print('Deleting all records...')
    Post.query.delete()
    User.query.delete()

    print('Creating users...')

    users = []
    usernames = []

    for i in range(20):
        username = fake.first_name()
        while username in usernames: # Guarantee uniqueness
            username = fake.first_name()
        usernames.append(username)

        user = User(username=username)
        user.password_hash = user.username + 'password'

        users.append(user)

    db.session.add_all(users)

    print('Creating posts...')

    posts = []

    for i in range(100):
        content = fake.text()
        title = fake.sentence()

        post = Post(content=content, title=title)
        post.user = rc(users)

        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()

    print('Complete')