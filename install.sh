# #!/bin/bash
logfile="/var/log/devopsdemo_install.log"

mysql_exec="create database flask;
             grant all on flask.* to flask@'127.0.0.1' identified by 'flask';
             grant all on flask.* to flask@'localhost' identified by 'flask';
             flush privileges;"

echo -e "\033[32;32m --> 安装依赖包...\033[0m"
yum groupinstall "Development tools" -y >> ${logfile}
yum install python-devel pyOpenSSL libffi-devel openssl-devel ntp -y >> ${logfile}

echo -e "\033[32;32m --> 时间同步...\033[0m"
/bin/cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && service ntpd start

echo -e "\033[32;32m --> 禁用selinux...\033[0m"


echo -e "\033[32;32m --> 安装virtual环境...\033[0m"
pip install virtualenv --trusted-host  pypi.douban.com 2>> ${logfile}
virtualenv /usr/local/flask



echo -e "\033[32;32m --> 安装mysql服务...\033[0m"
Release=`cat /etc/redhat-release | awk -F '.' '{print $1}'`
if [[ $Release == "CentOS Linux release 7" ]];then
  yum install -y mariadb mariadb-server mysql-devel >> ${logfile}
  sed -i "s@https:\/\/pypi.python.org\/@http:\/\/pypi.douban.com\/@g" /usr/local/flask/lib/python2.7/site-packages/pip/models/index.py
  systemctl start mariadb.service && mysql -e "${mysql_exec}" && echo "Db service done!"
  flag=1
else
  sed -i "s@https:\/\/pypi.python.org\/@http:\/\/pypi.douban.com\/@g" /usr/local/flask/lib/python2.6/site-packages/pip/models/index.py
  yum install -y mysql mysql-devel mysql-server >> ${logfile}
  rpm -e Percona-Server-shared-51-5.1.73 --nodeps
  sed -i "s@enabled = 1@enabled = 0@g" /etc/yum.repos.d/percona-release.repo
  yum -y install mysql-libs >> ${logfile}
  service mysqld start && mysql -e "${mysql_exec}" && echo "Db service done!"
  
fi

echo -e "\033[32;32m --> 安装devopsdemo依赖第三方包...\033[0m"
/usr/local/flask/bin/pip install -r requirements.txt --trusted-host pypi.douban.com 2>> ${logfile} 



echo -e "\033[32;32m --> 初始化devopsdemo所需数据库...\033[0m"
for i in "init" "migrate" "upgrade";do
 /usr/local/flask/bin/python manager.py db $i
done


echo -e "\033[32;32m --> 安装supervisor后台管理服务...\033[0m"
/usr/local/flask/bin/pip install supervisor --trusted-host pypi.douban.com  2>> ${logfile}
ln -sv /usr/local/flask/bin/supervisorctl /usr/bin/supervisorctl
ln -sv /usr/local/flask/bin/supervisord /usr/bin/supervisord
ln -sv /usr/local/flask/bin/gunicorn /usr/bin/gunicorn


echo -e "\033[32;32m --> 启动supervisor服务...\033[0m"
cp app/scripts/supervisor.conf /etc/
supervisord -c /etc/supervisor.conf 
supervisorctl -c /etc/supervisor.conf start all

echo -e "\033[32;32m --> 安装nginx服务...\033[0m"
yum install -y nginx >> ${logfile} 
mv app/scripts/nginx.conf /etc/nginx/nginx.conf


echo -e "\033[32;32m --> 启动nginx服务...\033[0m"
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
service nginx start
