# -*— coding:utf-8 -*-
from flask_script import Manager, Shell
from app import create_app, db
from app.models import User, Hostinfo, Random
from flask_migrate import Migrate, MigrateCommand, upgrade

import os
import os.path


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User,Random=Random,Hostinfo=Hostinfo)

manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)



@manager.command
def dev():
  from livereload import Server

  # 遍历所有文件进行watch,便于实施加载，开发
  live_server = Server(app.wsgi_app)
  for root, dirs, files in os.walk('/Volumes/data/study/devopsdemo_v2'):
      for name in files:
          filepath=os.path.join(root, name)
          live_server.watch(filepath,ignore=False)
  live_server.serve(open_url=False)



if __name__ == '__main__':
    manager.run()
