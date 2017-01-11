# -*- coding:utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from app.scripts.saltapi import SaltApi
from app.scripts.zabbixapi import ZabbixAction
from flask_login import  login_required
import json, datetime, sys, commands
from . import salt
from .. import db
from ..models import Hostinfo,Tasks
import datetime, os
reload(sys)
sys.setdefaultencoding('utf-8')
#####################################################################################
# 使用salt 拉取所有minion端的所需grains,并且入库
@salt.route('/',methods=['POST'])
@login_required
def import_hostinfo():
    if  request.method == 'POST':
        client = SaltApi()
        all_host = []
        for host in json.loads(client.saltCmd(params={'client': 'runner', 'fun': 'manage.up', 'tgt': '*'}))['return'][
            0]:
            all_host_info = dict(client.get_minions(host).items())
            hosts = {
                'hostname': all_host_info['hostname'],
                'private_ip': all_host_info['private_ip'],
                'public_ip': all_host_info['public_ip'],
                'mem_total': all_host_info['mem_total'],
                'cpu_type': all_host_info['cpu_type'],
                'num_cpus': all_host_info['num_cpus'],
                'os_release': all_host_info['os_release'],
                'kernelrelease': all_host_info['kernelrelease']
            }
            all_host.append(hosts)

            # 入库
            hostinfo = Hostinfo(
                hostname=hosts['hostname'],
                private_ip=hosts['private_ip'],
                public_ip=hosts['public_ip'],
                mem_total=hosts['mem_total'],
                cpu_type=hosts['cpu_type'],
                num_cpus=hosts['num_cpus'],
                os_release=hosts['os_release'],
                kernelrelease=hosts['kernelrelease']
            )
            try:
                db.session.add(hostinfo)
                db.session.commit()
                print hosts['hostname'], ' import success!'
            except:
                db.session.rollback()
                print hosts['hostname'], ' already exists!'
        return render_template('all_host_info.html', all_host=all_host)

#####################################################################################
@salt.route('/hostlist',methods=['GET','POST'])
@login_required
def hostlist():
    # 选择操作类型
    res = request.values.get('choose')
    if res == "详细":
        hostname = request.args.get('hostname')
        #print hostname
        # 查询单个主机的详细信息
        res = db.session.query(Hostinfo).filter_by(hostname=hostname)
        details = []
        [ details.append(x.to_list()) for x in res ]

        # get topinfo
        filepath = ('/tmp/topcache.txt')
        client=SaltApi()

        top_info = json.loads(client.saltCmd(params={'client': 'local', 'fun': 'cmd.run', 'tgt': hostname, 'arg':'top -b1 -n1 |head -n 5'}))['return'][0]

        for i in list(top_info.values()):
            with open(filepath, 'w') as f:
                f.write(i)
                f.close()

        #获取主机图形
        zclient=ZabbixAction()
        zclient.login()
        print hostname

        for res in zclient.get_graph(zclient.get_each_host(hostname), {"name": "Network traffic on eth0"}):
            network_id = res['graphid']
            print res['graphid'],res['name']
        for res in zclient.get_graph(zclient.get_each_host(hostname), {"name": "CPU load"}):
            cpuloads_id = res['graphid']
            print cpuloads_id
        for res in zclient.get_graph(zclient.get_each_host(hostname), {"name": "Memory usage"}):
            memory_id = res['graphid']
            print memory_id
        for res in zclient.get_graph(zclient.get_each_host(hostname), {"name": "CPU utilization"}):
            cpu_utilization_id = res['graphid']
            print cpu_utilization_id

        # 获取主机对应的主机组名称
        groupname=zclient.get_host_groupname(hostname)

        # test ping
        testping = json.loads(client.saltCmd(params={'client': 'local', 'fun': 'test.ping', 'tgt': hostname}))['return'][0].values()

        try:
            with open(filepath,'r') as f:
                top_info = f.readlines()
                f.close()

                return render_template('new_host_detail.html',
                                       testping=testping,
                                       groupname=groupname,
                                       hostname=hostname,
                                       details=details,
                                       top_info_list=top_info,
                                       network_id=network_id,
                                       cpuloads_id=cpuloads_id,
                                       memory_id=memory_id,
                                       cpu_utilization_id=cpu_utilization_id
                                       )
        except:
            return render_template('new_host_detail.html',
                                   testping=testping,
                                   hostname=hostname,
                                   details=details,
                                   top_info_list=top_info,
                                   network_id = network_id,
                                   cpuloads_id = cpuloads_id,
                                   memory_id = memory_id,
                                   cpu_utilization_id = cpu_utilization_id
                                   )

    elif res == "删除":
        hostname = request.args.get('hostname')
        print hostname
        delhost = Hostinfo.query.filter_by(hostname=hostname).first()
        try:
            db.session.delete(delhost)
            db.session.commit()
            print "Delete Host success!"
            flash(u"Delete Host success!",'success')
            # return render_template('hostlist.html')
        except:
            db.session.rollback()
        #print delhost

        return redirect(url_for('salt.query_allhost'))

    return render_template('hostlist.html')

#####################################################################################
# 查询数据库 前端展示所有server list
@salt.route('/hostlist_all',methods=['GET','POST'])
@login_required
def query_allhost():
    titles = [ '序列号','主机名', '外网IP', '内网IP', '内存大小', '内核版本', '操作']
    host_count = db.session.query(Hostinfo).count()
    page = request.args.get('page', 1, type=int)

    # 搜索某台主机
    if request.method == 'POST':
        hostname = request.form['hostname']
        # 本可以做模糊查询的，方法暂时没有找到  firter_by --> 精确查找， filter -->过滤条件
        pagination = Hostinfo.query.order_by(Hostinfo.hostname.asc()).filter(Hostinfo.hostname.like(hostname)).paginate(page, per_page=10, error_out=False)
    else:
        pagination = Hostinfo.query.order_by(Hostinfo.hostname.asc()).paginate(page, per_page=10, error_out=False)  # 默认返回数据库中所有主机

    posts = pagination.items

    details = []
    #print details
    [ details.append(i.to_list()) for i in posts ]

    return render_template('new_hostlist.html',
                           details=details,
                           titles=titles,
                           pagination=pagination,
                           posts=posts,
                           page=page,
                           host_count=host_count
                           )

#####################################################################################

# 执行salt 命令
@salt.route('/saltcmd',methods=['GET','POST'])
@login_required
def saltcmd():
    if request.method == 'POST':
        tgt_host = str(request.form['host'])
        cmd = str(request.form['cmd'])

        # 对单台主机进行命令执行
        cmd_params = {'client':'local','fun':'cmd.run','tgt':tgt_host,'arg': cmd }
        print tgt_host
        print cmd
        # 对某个分组执行批量(需要将主机加入到salt-mater主配置文件中，并开启分组功能)
        #cmd_params = {'client':'local','fun':'cmd.run', 'tgt':tgt_host ,'arg':cmd, 'expr_form':'nodegroup'}

        # 命令黑名单
        block_cmd = ['rm', '>', 'shutdown', 'poweroff', 'htop', 'date', 'echo']
        for i in block_cmd:
            if i in cmd:
                flash(u'禁止运行此命令: ','danger')
                return render_template('new_saltcmd.html',cmd=i)

        #判断填入的信息是否为空
        if tgt_host == '' or cmd == '':
            flash(u'目标主机 或 命令不能为空.','danger')
            return render_template('new_saltcmd.html')
        starttime = datetime.datetime.now()
        client = SaltApi()

        result = client.saltCmd(cmd_params)
        endtime = datetime.datetime.now()
        json_data = json.loads(result)
        tc = (endtime - starttime).seconds
        return render_template('new_saltcmd.html', result=json_data['return'][0].items(),cmd=cmd,tc=tc)
    return render_template('new_saltcmd.html')

#####################################################################################
# 执行salt 命令
@salt.route('/deploy',methods=['GET','POST'])
@login_required
def deploy():
    """
    软件部署 sls文件
    1. Init system
    2. Nginx
    3. ZabbixAgent
    4. PHP-FPM

    """
    Soft_dict={
         1:'a',
         2:'php-fpm',
         3:'appliaction/zabbix-agent/zabbix_agent',
         4:'init-system',
         5:'redis'
         }
    filepath = ('/tmp/deploy_cache')
    title = ['序列号', '目标主机', '应用名称', '执行JID', '部署时间', '详情']
    if request.method == 'POST':
        deploy_time=datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        server_list = []
        content = request.form['contenet'].split(',')

        [ server_list.append(i.strip()) for i in content ]

        soft_list=request.form.getlist('vehicle')

        if  server_list == [u'']  or not soft_list:
            flash(u'目标主机 and 软件选择 不能为空！','danger')
            return render_template('new_deploy.html',softs=Soft_dict.values())
        soft=[]
        client = SaltApi()

        fo = open('/tmp/deploy_cache','w') # 执行结果输出到缓存文件
        for soft_num in soft_list:
            if int(soft_num)  in Soft_dict.keys():
                for tgt_host in server_list:
                    soft.append(Soft_dict[int(soft_num)])

                    #执行应用部署，即执行sls文件后获取jid
                    deploy_parmas = {'client':'local_async', 'fun':'state.sls', 'tgt':tgt_host, 'arg':Soft_dict[int(soft_num)]}

                    #deploy_parmas = {'client':'local_async', 'fun':'state.sls', 'tgt':tgt_host, 'arg':'a'}


                    jid = dict(json.loads(client.saltCmd(params=deploy_parmas))['return'][0]).values()[0]
                    print tgt_host
                    t1 = ("%s,%s,%s,%s\n") % (tgt_host,Soft_dict[int(soft_num)],jid,deploy_time)
                    fo.write(t1)
                    print "主机 %s 将会部署 %s id 为 %s" % (tgt_host, Soft_dict[int(soft_num)], jid)
        fo.close()

        res = list((commands.getoutput('cat /tmp/deploy_cache')).decode('utf-8').split('\n'))

        return render_template('new_deploy.html',res=res,title=title,softs=Soft_dict.values(),result=True)

    #title = ['序列号', '目标主机', '应用名称', '执行JID', '部署时间', '详情']
    if os.path.exists(filepath) is False:
        return render_template('new_deploy.html', softs=Soft_dict.values(), title=title, result=False)
    else:
        res = list((commands.getoutput('cat /tmp/deploy_cache')).decode('utf-8').split('\n'))
        return render_template('new_deploy.html', softs=Soft_dict.values(),res=res,title=title, result=True)


#####################################################################################
# 通过jid获取result
@salt.route('/deployresult',methods=['GET','POST'])
@login_required
def deployresult():
    if request.method == 'POST':
        JID=request.args.get('JID')
        client = SaltApi()

        client.get_jobs(JID)
        #result = dict(json.loads(client.get_jobs(JID))['return'][0])  # salt_2016.11.1 新版本使用该语句

        result = json.loads(client.get_jobs(JID))['return'][0]['data'] # salt_2015.5.10 老版本使用该语句

        return render_template('new_deployresult.html', result=result)
    return render_template('new_deployresult.html')

#####################################################################################
# 获取jid详细结果
@salt.route('/get_jidres',methods=['GET','POST'])
@login_required
def get_jidres():
    return render_template('new_synccode.html')

#####################################################################################
# 代码同步
@salt.route('/synccode',methods=['GET','POST'])
@login_required
def synccode():
    if request.method == ['POST']:
        return render_template('new_synccode.html')
    return render_template('new_synccode.html')


#####################################################################################
# 配置推送
@salt.route('/pushcfg',methods=['GET','POST'])
@login_required
def pushcfg():
    if request.method == ['POST']:
        return render_template('new_pushcfg.html')
    return render_template('new_pushcfg.html')


#####################################################################################
# 配置推送
@salt.route('/services',methods=['GET','POST'])
@login_required
def services():
    if request.method == ['POST']:
        info = 'sleep 30s'
        return render_template('new_saltservice.html',info=info)
    return render_template('new_saltservice.html')

#####################################################################################
# 测试
@salt.route('/taskcenter',methods=['POST','GET'])
@login_required
def taskcenter():
    page = request.args.get('page', 1, type=int)
    res  = Tasks.query.order_by(Tasks.task_id.asc()).paginate(page, per_page=10, error_out=False)
    details = []
    [details.append(i.to_list()) for i in res.items ]

    for detail in details:
        print detail
    return render_template('new_taskcenter.html', details=details)


