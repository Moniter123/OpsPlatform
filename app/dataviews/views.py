# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, flash
from flask_login import current_user, login_required
from . import dataviews
import json

@dataviews.route('/query1')
@login_required
def query1():
    posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    return render_template('query1.html', posts=posts)

@dataviews.route('/query3')
@login_required
def query3():
    posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    return render_template('query3.html', posts=posts)


@dataviews.route('/query4')
@login_required
def query4():
    import random
    r1 = random.randint(0, 100)
    posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    return render_template('query4.html', posts=posts,test=r1)


@dataviews.route('/query5')
@login_required
def query5():
    posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    return render_template('query5.html', posts=posts)