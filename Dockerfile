# The FROM instruction sets the Base Image for subsequent instructions.
FROM centos:6

MAINTAINER Lanway <115564098@qq.com>

#���û�����װ����
RUN yum -y  groupinstall "Development tools"
RUN yum -y install zlib-devel
RUN yum -y install bzip2-devel
RUN yum -y install openssl-devel
RUN yum -y install ncurses-devel
RUN yum -y install sqlite-devel
RUN yum -y install wget

#����python
WORKDIR /opt
RUN wget --no-check-certificate https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
RUN tar xf Python-2.7.9.tar.xz
WORKDIR Python-2.7.9
RUN ./configure --prefix=/usr/local
RUN make && make altinstall
RUN ln -s /usr/local/bin/python2.7 /usr/local/bin/python

#����pip
WORKDIR /usr/local/src
RUN wget "https://pypi.python.org/packages/source/p/pip/pip-1.5.4.tar.gz#md5=834b2904f92d46aaa333267fb1c922bb" --no-check-certificate
RUN wget http://pypi.python.org/packages/source/s/setuptools/setuptools-2.0.tar.gz
RUN tar zxvf setuptools-2.0.tar.gz
WORKDIR setuptools-2.0
RUN python setup.py build
RUN python setup.py install
WORKDIR /usr/local/src
RUN tar -xzvf pip-1.5.4.tar.gz
WORKDIR pip-1.5.4
RUN python setup.py install

#����mysql
RUN yum install -y mysql-server mysql mysql-devel

#����mysqldb
RUN pip install mysql-python==1.2.3

#����request
RUN pip install requests==2.12.0

#����sqlalchemy
RUN pip install sqlalchemy==1.1.0

#����tornado
RUN pip install tornado==4.0

#����redis
RUN pip install redis==2.10.5

#����һ��ָ�����ļ������ڷ��ô���
RUN mkdir -p /app
WORKDIR /app
COPY . /app

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime
EXPOSE 800

# The CMD instruction provides default execution command for an container
# Start Nginx and keep it from running background
                                                                             