# -*- coding:utf-8 -*-
from flask_login import current_user, login_required
from . import dataapi
import json
from .. import db
from ..models import Random

@dataapi.route('/query1api',methods=['GET','POST'])
@login_required
def query1api():
    from app.scripts.zabbix_login import Zabbix

    zlogin = Zabbix('http://114.55.0.47:9986', 'Admin', 'ZTNiMGM0')
    zlogin.login()  # 登录Zabbix Api

    v = []
    for i in zlogin.item_get('10193'):  # 获取主机item ,代码中可以过滤掉特定的key_
        for s in zlogin.history_get(dict(i).values(), 0):
            # print s
            v.append(s['value'])

            data = {
                "legen": ["15 min", "1 min", "5 min"],
                "series": v
            }


    data = json.dumps(data, indent=4, encoding='utf-8')
    print data
    return data
    #return render_template('query1.html', posts=posts,data=data)


@dataapi.route('/query3api',methods=['GET','POST'])
@login_required
def query3api():
    #posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    import random
    r1 = random.randint(0, 9)
    r2 = random.randint(0, 9)
    r3 = random.randint(0, 9)

    # 实时入库
    # num = Random(num1=r1,num2=r2,num3=r3)
    # db.session.add(num)
    # db.session.commit()
    data = {
        "legen":["Chrome",'Firefox','IE10'],
        "series":[r1,r2,r3]
    }
    #print data
    data=json.dumps(data, indent=4 ,encoding='utf-8')
    return  data
    #return render_template('query4.html', posts=posts,data=data)


@login_required
def query4api():
    #posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    import random
    r1 = random.randint(0, 9)
    r2 = random.randint(0, 9)
    r3 = random.randint(0, 9)

    # 实时入库
    num = Random(num1=r1,num2=r2,num3=r3)
    db.session.add(num)
    db.session.commit()
    data = {
        "legen":["Chrome",'Firefox','IE10'],
        "series":[r1,r2,r3]
    }
    #print data
    data=json.dumps(data, indent=4 ,encoding='utf-8')
    return  data



@dataapi.route('/query4api',methods=['GET','POST'])
@login_required
def query4api():
    #posts = {'body': 'Bootstrap is beautiful, and Flask is cool!'}
    import random
    r1 = random.randint(0, 9)
    r2 = random.randint(0, 9)
    r3 = random.randint(0, 9)

    # 实时入库
    num = Random(num1=r1,num2=r2,num3=r3)
    db.session.add(num)
    db.session.commit()
    data = {
        "legen":["Chrome",'Firefox','IE10'],
        "series":[r1,r2,r3]
    }
    #print data
    data=json.dumps(data, indent=4 ,encoding='utf-8')
    return  data
    #return render_template('query4.html', posts=posts,data=data)

@dataapi.route('/query5api',methods=['GET','POST'])
@login_required
def query5api():

    import commands, time

    start_time = int(1000 * time.time())

    commands.getoutput('sleep 10')

    end_time = int(1000 * time.time())

    total_time = end_time - start_time

    data = {
        "total": total_time
    }
    #print data
    data=json.dumps(data, indent=4 ,encoding='utf-8')
    print data
    return  data
    #return render_template('query4.html', posts=posts,data=data)