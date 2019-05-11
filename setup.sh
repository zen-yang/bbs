#!/usr/bin/env bash

# 换 apt 源
ln -f -s /var/www/bbs/misc/sources.list /etc/apt/sources.list
# 换 pip 源
mkdir -p /root/.pip
ln -f -s /var/www/bbs/misc/pip.conf /root/.pip/pip.conf

# 装python 3.6
add-apt-repository -y ppa:deadsnakes/ppa # 添加第三方仓库
apt update # 更新apt
apt install -y python3.6 # 安装3.6
curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py # 下载pip文件
python3.6 /tmp/get-pip.py
# 安装pip，为什么不用apt install python3-pip？因为这个是针对系统内置的python3.5的，怕有时候会出问题

# 装依赖包
pip3 install gunicorn gevent flask pytest sqlalchemy pymysql

# 装软件
apt install -y git supervisor nginx zsh curl ufw
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# MySQL
#your_password用你自己的密码
apt install -y debconf
debconf-set-selections <<< 'mysql-server mysql-server/root_password password your_password'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password your_password'
apt -y install mysql-server

# 配置防火墙
ufw allow 22
ufw allow 80
ufw allow 443
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
ln -s -f  /var/www/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf
# 不要再 sites-available 里面放任何东西
ln -s -f  /var/www/bbs/bbs.nginx /etc/nginx/sites-enabled/bbs

# 重启服务器
service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I
