# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, flash, send_from_directory
from flask_login import current_user, login_required
from app.scripts.saltapi import SaltApi
from . import main
from .. import db
from ..models import User,Hostinfo
import json,requests
import xlwt  # 将数据导入到excel中

@main.route('/')
def index():
     if not current_user.is_authenticated:
        return redirect('auth/login')
     else:
        host_count = db.session.query(Hostinfo).count()
        return render_template('new_dashboard.html',host_count=host_count)

@main.route('/monitor',methods=['GET'])
@login_required
def monitor():
    url = "http://admin:admin@114.55.0.47:3000/api/org/"
    s = requests.session().get(url=url)
    print s

    return  render_template('monitor.html')


@main.route('/basic')
@login_required
def basic():
    posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    return render_template('dashboard.html', posts=posts)


# 个人信息
@main.route('/profile/<username>')
@login_required
def profile(username):
    res = User.query.filter_by(username=username).first()
   # res = User.query.filter(username=username).first()
    print res
    return render_template('profile.html')


@main.route('/data',methods=['GET','POST'])
@login_required
def data():
    if request.method == 'POST':
        content = request.form['contenet']
        print request.form['contenet']
        if request.form['contenet'] == '':
            flash(u'请填写表名称.')
            return render_template('datadump.html')
        else:
            client=SaltApi()
            params = {'client': 'local', 'fun': 'cmd.run', 'tgt': 'jp-cbt', 'arg': '/bin/bash /root/import_from_jptest_to_jpcbt.sh %s' % content }
            json_data=json.loads(client.saltCmd(params))['return'][0].values()
            return render_template('datadump.html',data=json_data)
    return  render_template('datadump.html')

@main.route('/data1',methods=['GET','POST'])
@login_required
def data1():
    if request.method == 'POST':
        content = request.form['contenet']
        print request.form['contenet']
        if request.form['contenet'] == '':
            flash(u'请填写表名称.')
            return render_template('datadump.html')
        else:
            client=SaltApi()
            params = {'client': 'local', 'fun': 'cmd.run', 'tgt': 'jp-cbt', 'arg': '/bin/bash /root/import_from_jpcbt_to_jpserver.sh %s' % content }
            json_data=json.loads(client.saltCmd(params))['return'][0].values()
            return render_template('datadump.html',data=json_data)
    return  render_template('datadump.html')



# 导出数据
@main.route('/export_data',methods=['GET','POST'])
def export_data():
    if request.method == 'POST':
        row = 1
        wbk = xlwt.Workbook()
        sheet=wbk.add_sheet('hostlist')
        sheet.write(0, 0, u'主机名')
        sheet.write(0, 1, u'外网IP')
        sheet.write(0, 2, u'内网IP')
        sheet.write(0, 3, u'内存大小(M)')
        sheet.write(0, 4, u'CPU类型')
        sheet.write(0, 5, u'CPU数量')
        sheet.write(0, 6, u'OS版本')
        sheet.write(0, 7, u'内核版本')

        details=[]
        [details.append(i.to_list()) for i in Hostinfo.query.all()]

        for i in details:
            sheet.write(row, 0, i[1])
            sheet.write(row, 1, i[2])
            sheet.write(row, 2, i[3])
            sheet.write(row, 3, i[4])
            sheet.write(row, 4, i[5])
            sheet.write(row, 5, i[6])
            sheet.write(row, 6, i[7])
            sheet.write(row, 7, i[8])
            row+=1
        wbk.save('/tmp/hostlist.xls')
        #文件下载
        return send_from_directory('/tmp', 'hostlist.xls', as_attachment=True)
