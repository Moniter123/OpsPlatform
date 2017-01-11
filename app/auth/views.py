# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from flask_login import login_user, logout_user, current_user


# 用户登录
@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Check user info, email and password !
    '''
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first() # 数据库查询
            if user is not None and user.verify_password(form.password.data): # 用户是否存在以及密码是否争取额
                login_user(user,form.remember_me.data) # 记住我功能，bool值
                return redirect(url_for('main.index')) # 如果认证成功则重定向到已认证首页
            flash(u'邮箱或密码无效,请重新输入!','danger')    # 如果认证错误则flash一条消息过去
        except:
            flash(u'数据库连接错误错误，请检查数据库服务!', 'danger')
    return render_template('auth/login.html', form=form)


# 用户登出
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# 用户注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You Are Register Success!','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

