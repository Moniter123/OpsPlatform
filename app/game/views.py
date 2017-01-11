# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, flash
from flask_login import login_required
from app.scripts.saltapi import SaltApi
from . import game
import json


def output(params):
  client = SaltApi()
  json_data = json.loads(client.saltCmd(params))
  notice = json_data['return'][0].items()

  return notice

@game.route('/japan',methods=['GET','POST'])
@login_required
def japan():
    tag = {
         '': u'选择一个操作',
        'hotupdate': u'CBT 热更新',
        'codeupdate': u'CBT 代码更新',
        'confupdate': u'CBT 配置更新',
        'cleancache': u'CBT 缓存清理'
    }
    if request.method == 'POST':
        if request.form.get('comp_select') == 'hotupdate':
            params = {'client': 'local', 'fun': 'cmd.run', 'tgt': 'jp-contorl', 'arg': 'sh /root/cbt_update_jp_hot.sh' }
            notice = output(params)
            return render_template('japan.html', tag=tag, notice=notice, res=True)
        elif request.form.get('comp_select') == 'codeupdate':
            params = {'client': 'local', 'fun': 'cmd.run', 'tgt': 'jp-test', 'arg': 'date'}
            notice = output(params)
            return render_template('japan.html', tag=tag, notice=notice, res=True)
        elif request.form.get('comp_select') == 'confupdate':
            params = {'client': 'local', 'fun': 'cmd.run', 'tgt': 'jp-cbt', 'arg': 'date'}
            notice = output(params)
            return render_template('japan.html', tag=tag, notice=notice, res=True)
        elif request.form.get('comp_select') == 'cleancache':
            params = {'client': 'local', 'fun': 'cmd.run', 'tgt': 'jp-cbt', 'arg': 'sh /root/clear_game_temp_data.sh '}
            notice = output(params)
            return render_template('japan.html', tag=tag, notice=notice, res=True)
        else:
            flash(u'请选择一个操作项操作.')
    return render_template('japan.html', tag=tag)
