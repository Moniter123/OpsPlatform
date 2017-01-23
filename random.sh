for i in {2s3..254};do
	mysql -uroot -pguo.150019 -e "insert into flask.hostinfo(hostname,public_ip,private_ip,mem_total,cpu_type,num_cpus,os_release,kernelrelease) values('shipgs-tw-${i}-23','118.12.3.${i}','10.${i}.1.34','4000','Intel(R) Xeon(R) CPU E5-2670 v2','1','CentOS 6.8','2.6.32-642.3.1.el6.x86_64');"
done
