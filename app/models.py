from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

  #  def __repr__(self):
   #     return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
       return '%r,%r' % (self.username,self.email)


class Random(db.Model):
    __tablename__ = 'random'
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.String(12), unique=False)
    num2 = db.Column(db.String(12), unique=False)
    num3 = db.Column(db.String(12), unique=False)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<num1 %r,num2 %r,num3 %r>' % (self.num1,self.num2,self.num3)


class Hostinfo(db.Model):
    __tablename__ = 'hostinfo'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(32), unique=True)
    public_ip = db.Column(db.String(32), unique=False)
    private_ip = db.Column(db.String(32), unique=False)
    mem_total = db.Column(db.String(32), unique=False)
    cpu_type = db.Column(db.String(32), unique=False)
    num_cpus = db.Column(db.Integer, unique=False)
    os_release = db.Column(db.String(32), unique=False)
    kernelrelease = db.Column(db.String(32), unique=False)


    def __repr__(self):
      return "%s,%s,%s,%s,%s,%s,%s,%s" % (self.hostname,
                                            self.public_ip,
                                            self.private_ip,
                                            self.mem_total,
                                            self.cpu_type,
                                            self.num_cpus,
                                            self.os_release,
                                            self.kernelrelease

                                            )
    def to_json(self):
        return {
                'hostname' : self.hostname,
                'public_ip' : self.public_ip,
                'private_ip' : self.private_ip,
                'mem_total' : self.mem_total,
                'cpu_type'  : self.cpu_type,
                'num_cpus' : self.num_cpus,
                'os_release': self.os_release,
                'kernelrelease': self.kernelrelease
        }

    def to_list(self):
        hosts = [
                self.id,
                self.hostname,
                self.public_ip,
                self.private_ip,
                self.mem_total,
                self.cpu_type,
                self.num_cpus,
                self.os_release,
                self.kernelrelease
                ]
        return hosts

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(32), unique=True)
    task_name = db.Column(db.String(32), unique=True)
    task_start_time = db.Column(db.DateTime)
    task_end_time = db.Column(db.DateTime)
    task_status = db.Column(db.String(32), unique=False)

    def to_list(self):
        tasks_info = [
            self.id,
            self.task_id,
            self.task_name,
            self.task_start_time,
            self.task_end_time,
            self.task_status,
        ]
        return tasks_info


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
