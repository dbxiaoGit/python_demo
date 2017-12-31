#!/usr/bin/env python2.7

import os
import sys
import time
import shlex
import socket
import shutil
import tarfile
import argparse
import ConfigParser
import psutil
import urllib
from time import sleep
from datetime import datetime
from subprocess import Popen, STDOUT

BASE_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
DEFAULT_CONFIG_FILE = '%s/test-project.conf.default' % BASE_PATH
CONFIG_FILE = '%s/test-project.conf' % BASE_PATH
BACKUP_PATH = '/wls/backup'
ACTION_LIST = ['start', 'stop', 'restart', 'kill', 'status', 'info', 'backup', 'dump', 'pid', 'debug']
STARTUP_TIMEOUT = 120
STOP_TIMEOUT = 10

class PidError(Exception):
    pass

class Output(object):
    stdout = sys.stdout
    stderr = sys.stderr

    @classmethod
    def _write(cls, msg, color_id=37, newline=True):
        if cls.stdout is None: return
        n = '\n' if newline else ''
        cls.stdout.write('\033[1;%s;40m%s\033[0m%s' % (color_id, msg, n))
        cls.stdout.flush()

    @classmethod
    def echo(cls, msg='', newline=True):
        cls._write(msg, newline=newline)

    @classmethod
    def msg(cls, msg):
        cls._write(msg, 32)

    @classmethod
    def warn(cls, msg):
        cls._write(msg, 33)

    @classmethod
    def error(cls, msg, exit_code=1):
        if cls.stderr is None: return
        cls.stderr.write('\033[1;31;40m%s\033[0m\n' % msg)
        cls.stderr.flush()
        if exit_code:
            cls.stderr.write('\n')
            sys.exit(exit_code)

class Cfg(object):
    def __init__(self, cfg_items):
        for cfg_item in cfg_items:
            if cfg_item[0] in ('http_port', 'jmx_port'):
                setattr(self, cfg_item[0], int(cfg_item[1]))
            else:
                setattr(self, cfg_item[0], cfg_item[1])

class App(Output):
    def __init__(self, cfg):
        self.cfg = cfg
        self._proc = None

    @property
    def proc(self):
        if self._proc and self._proc.is_running(): return self._proc
        for proc in psutil.process_iter():
            # try:
            #     proc_name = proc.cmdline[0]
            # except IndexError:
            #     continue
            # if proc_name == self.cfg.appname:
            #     self._proc = proc
            #     return self._proc
            try:
                if '-Dapp.name='+self.cfg.appname in proc.cmdline():
                        self._proc = proc
                        return self._proc
            except psutil.AccessDenied:
                pass
        return None

    def pid(self):
        if self.proc:
            self.echo(self.proc.pid)

    def getProcessInfo(self):
        if self.proc:
            proc_info = {
                          'status':str(self.proc.status),
                          'create_time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(self.proc.create_time()))),
                          #'ports':[ conn.local_address[1] for conn in self.proc.get_connections() ],
                          #'ports':[ conn.local_address[1] for conn in self.proc.connections() ],
                          'cpu_usage':self.proc.cpu_percent(),
                          'cpu_time_system':self.proc.cpu_times().system,
                          'cpu_time_user':self.proc.cpu_times().user,
                          'memory_rss':self.proc.memory_info().rss,
                          'memory_vms':self.proc.memory_info().vms,
                          'memory_usage':'%.2f' % self.proc.memory_percent(),
                          # 'io_read_count':self.proc.io_counters().read_count,
                          # 'io_read_bytes':self.proc.io_counters().read_bytes,
                          # 'io_write_count':self.proc.io_counters().write_count,
                          # 'io_write_bytes':self.proc.io_counters().write_bytes,
                          #  for Linux
                          'fds_num':self.proc.num_fds(),
                          'threads_num':self.proc.num_threads(),
                        }
            return proc_info
        return None

    def checkPort(self, port):
        s = socket.socket()
        try:
            s.connect(('127.0.0.1', port))
        except:
            return False
        s.close()
        return True

    def execute(self, action, output=sys.stdout):
        java_opts = '%s %s' % (self.cfg.java_opts, self.cfg.spring_boot_jmx_opts) if action == 'start' else self.cfg.java_opts
        cmd = '%s %s -classpath %s -Dapp.name=%s -Djava.io.tmpdir=%s   -Dserver.port=%s -Djava.security.egd=file:/dev/./urandom -Dserver.undertow.accesslog.dir=%s org.springframework.boot.loader.JarLauncher %s' % \
              (self.cfg.appname, java_opts, self.cfg.classpath, self.cfg.appname, self.cfg.spring_boot_temp,self.cfg.http_port,self.cfg.log_path, action)
        cmd = shlex.split(cmd)
        return Popen(cmd, stdin=None, stdout=output, stderr=STDOUT, executable=self.cfg.java_bin, cwd=self.cfg.spring_boot_base)

    def info(self):
        self.msg('Application Name: %s' % self.cfg.appname)
        self.msg('Using SPRING_BOOT_BASE: %s' % self.cfg.spring_boot_base)
        #self.msg('Using CATALINA_HOME: %s' % self.cfg.catalina_home)
        self.msg('Using SPRING_BOOT_TMPDIR: %s' % self.cfg.spring_boot_temp)
        #self.msg('Using JAVA_HOME: %s' % self.cfg.java_home)
        self.msg('Using JAVA_OPTS: %s' % self.cfg.java_opts)
        self.msg('Using CLASSPATH: %s' % self.cfg.classpath)
        self.msg('Using LOG_FILE: %s' % self.cfg.spring_boot_out)
        self.msg('Using HTTP_PORT: %s' % self.cfg.http_port)
        #self.msg('Using SHUTDOWN_PORT: %s' % self.cfg.shutdown_port)
        self.msg('Using JMX_PORT: %s' % self.cfg.jmx_port)
        self.msg('Using classpath:%s' % self.cfg.classpath)

    def status(self):
        self.echo('Checking PID:'.ljust(30, '.'), False)
        if self.proc:
            self.msg(self.proc.pid)
        else:
            self.error('Not Found', 0)
        
        self.echo('Checking HTTP Port:'.ljust(30, '.'), False)
        if self.checkPort(self.cfg.http_port):
            self.msg(self.cfg.http_port)
        else:
            self.error('Not Open', 0)
        
        # self.echo('Checking SHUTDOWN Port:'.ljust(30, '.'), False)
        # if self.checkPort(self.cfg.shutdown_port):
        #     self.msg(self.cfg.shutdown_port)
        # else:
        #     self.error('Not Open', 0)

        self.echo('Checking JMX Port:'.ljust(30, '.'), False)
        if self.checkPort(self.cfg.jmx_port):
            self.msg(self.cfg.jmx_port)
        else:
            self.error('Not Open', 0)
        
        if not self.proc: return
        proc_info = self.getProcessInfo()
        self.echo('Process Status:'.ljust(30, '.'), False)
        self.msg(proc_info['status'])

        self.echo('Process Create Time:'.ljust(30, '.'), False)
        self.msg(proc_info['create_time'])

        self.echo('CPU Usage:'.ljust(30, '.'), False)
        self.msg('%s %%' % proc_info['cpu_usage'])

        self.echo('CPU Time System:'.ljust(30, '.'), False)
        self.msg('%s s' % proc_info['cpu_time_system'])

        self.echo('CPU Time User:'.ljust(30, '.'), False)
        self.msg('%s s' % proc_info['cpu_time_user'])

        self.echo('Memory Usage:'.ljust(30, '.'), False)
        self.msg('%s %%' % proc_info['memory_usage'])

        self.echo('Memory RSS:'.ljust(30, '.'), False)
        self.msg('%.2f MB' % (float(proc_info['memory_rss']) / 1048576))

        self.echo('Memory VSS:'.ljust(30, '.'), False)
        self.msg('%.2f MB' % (float(proc_info['memory_vms']) / 1048576))

        self.echo('Threads Number:'.ljust(30, '.'), False)
        self.msg(proc_info['threads_num'])

    # def cleanwork(self):
    #     self.echo('Clean Work directory:'.ljust(30, '.'), False)
    #     try:
    #         if os.path.isdir('%s/Catalina/' % self.cfg.catalina_work):
    #             shutil.rmtree('%s/Catalina/' % self.cfg.catalina_work)
    #     except:
    #         self.error('Failed')
    #     else:
    #         self.msg('Done')

    def backup(self):
        def backup_filter(tarinfo):
            exclude_ext = ('.bak', '.old', '.log', '.pid')
            exclude_dir = ('logs', 'temp', 'work')
            path = tarinfo.name.split('/')
            if len(path) > 2 and path[1] in exclude_dir:
                return None
            if os.path.splitext(tarinfo.name)[1] in exclude_ext:
                return None 
            self.echo(tarinfo.name)
            return tarinfo
        if not os.path.exists(BACKUP_PATH):
            os.mkdir(BACKUP_PATH)
        backup_file = '%s/%s_%s.tgz' % (BACKUP_PATH, self.cfg.appname, datetime.now().strftime('%Y-%m-%d'))
        self.msg('Backup %s ...' % self.cfg.appname)
        try:
            with tarfile.open(backup_file, 'w:gz') as backup_fp:
                backup_fp.add(self.cfg.spring_boot_base, self.cfg.appname, filter=backup_filter)
        except Exception, e:
            self.error('ERROR: %s' % e)
        else:
            self.msg('Done')
            self.msg('Backup file: %s' % backup_file)

    def dump(self):
        self.echo('Searching PID'.ljust(30, '.'), False)
        if not self.proc:
            self.error('Not Found.')
        self.msg(self.proc.pid)
        for i in range(1,4):
            self.echo('Dump %s time'.ljust(30, '.') % i, False)
            self.proc.send_signal(3)
            sleep(5)
            self.msg('Done')

    def start(self):
        self.msg('Starting Application: %s\n' % self.cfg.appname)
        if self.proc:
            self.error('spring-boot appears to still be running with PID %s. Start aborted.' % self.proc.pid)
        if self.checkPort(self.cfg.http_port):
            self.error('HTTP Port %s already in use. Start aborted.' % self.cfg.http_port)
        # if self.checkPort(self.cfg.shutdown_port):
        #     self.error('SHUTDOWN Port %s already in use. Start aborted.' % self.cfg.shutdown_port)

        self.info()
        #self.echo()
        # self.cleanwork()
        self.echo()
        spring_boot_out = open(self.cfg.spring_boot_out, 'a')
        spring_boot_out.write('spring-boot Start at %s'.center(100, '*') % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        spring_boot_out.write('\n')
        spring_boot_out.flush()
        log_fp = open(self.cfg.spring_boot_out, 'r')
        log_fp.seek(0, os.SEEK_END)
        start_time = time.time()
        instance = self.execute('start', spring_boot_out)
        while True:
            log = log_fp.readline()
            if log:
                self.echo(log, False)
                if log.find('Tomcat started on port') != -1 or log.find('Undertow started on port') !=-1:
                    break
            if time.time() - start_time > STARTUP_TIMEOUT:
                instance.kill()
                self.error('\nApplication: %s cannot statup in %s seconds. The process is killed.' % (self.cfg.appname, STARTUP_TIMEOUT))
        self.msg('\nApplication: %s statup in %.2f seconds with PID %s.' % (self.cfg.appname, time.time() - start_time, instance.pid))

    def stop(self):
        self.msg('Stopping Application: %s\n' % self.cfg.appname)
        if not self.proc:
            self.error('No matching process was found. Is spring_boot running? Stop aborted.')

        try:
            log_fp = open(self.cfg.spring_boot_out, 'r')
        except IOError:
            self.warn('Cannot open log file: %s.' % self.cfg.spring_boot_out)
            log_fp = type('evil', (object,), {'__getattr__':lambda *x:lambda *y:None})()
        log_fp.seek(0, os.SEEK_END)
        start_time = time.time()
        # instance = self.execute('stop')
        # self.proc.kill()
        data = {}
        url = 'http://127.0.0.1:%s/shutdown' % self.cfg.http_port
        post_data = urllib.urlencode(data)
        response = urllib.urlopen(url,post_data)
        result = response.read()
        response.close()
        if result.find('Shutting down, bye') == -1:
                App.error('Application:%s stop fail' % self.cfg.appname)
        while True:
            log = log_fp.readline()
            if log:
                self.echo(log, False)
            if not self.proc:
                break
            if time.time() - start_time > STOP_TIMEOUT:
                self.error('\nApplication: %s cannot stopped in %s seconds.' % (self.cfg.appname, STOP_TIMEOUT))
        self.msg('\nApplication: %s stopped.' % self.cfg.appname)

    def restart(self):
        try:
            self.stop()
        except SystemExit:
            pass
        sleep(1)
        self.start()

    def kill(self):
        self.echo('Searching PID'.ljust(30, '.'), False)
        if not self.proc:
            self.error('Not Found.')
        self.msg(self.proc.pid)
        self.echo('Killing PID'.ljust(30, '.'), False)
        self.proc.kill()
        for i in range(3):
            if not self.proc:
                break
            sleep(1)
        else:
            self.error('Failed')
        self.msg('Success')
    def debug(self):
        self.msg('do not support')

def main():
    parser = argparse.ArgumentParser(description='Control spring-boot to %s.' % ', '.join(ACTION_LIST), epilog='Version %s Build %s By %s.' % (__version__, __build__, __author__))    
    parser.add_argument('appname', metavar='AppName', help='AppName defind in test-project.conf or all')
    parser.add_argument('action', metavar='Action', help='Action in %s' % ', '.join(ACTION_LIST))
    parser.add_argument('-t', '--timeout', dest='timeout', type=int, default=0, help='Timeout for start or stop')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true', help='Run in silently without stdout')
    args = parser.parse_args()

    if not os.path.isfile(DEFAULT_CONFIG_FILE):
        App.error('Default config file: %s not found.' % DEFAULT_CONFIG_FILE)
    if not os.path.isfile(CONFIG_FILE):
        App.error('Config file: %s not found.' % CONFIG_FILE)
    config = ConfigParser.SafeConfigParser(allow_no_value=True)
    config.readfp(open(DEFAULT_CONFIG_FILE))
    config.read(CONFIG_FILE)
    appname=args.appname
    jar_path=config.get(appname,'jar_path')
    if not jar_path.endswith('/'):
        jar_path = jar_path + '/'
    jars=[]
    if os.path.isdir(jar_path):
        for jar in (jarName for jarName in os.listdir(jar_path) if jarName.endswith('.jar')):
                jars.append(jar_path+jar)
    else:
        App.error('jar_path:%s is not a dictory!' % jar_path)

    jars_str=':'.join(jars)
    if jars_str!='':
        classpath=config.get(appname,'classpath')
        if classpath.endswith(":"):
                classpath=classpath+jars_str
        else:
                classpath=classpath+':'+jars_str
    else:
        App.error('jar_path:%s has no jar!' % jar_path)
    config.set(appname,'classpath',classpath)

    if not config.has_section(args.appname) and args.appname != 'all':
        App.error('AppName: %s not found in %s or all' % (args.appname, CONFIG_FILE))
    if args.action not in ACTION_LIST:
        App.error('Action: %s must in %s' % (args.action, ', '.join(ACTION_LIST)))
    if args.timeout:
        global STARTUP_TIMEOUT, STOP_TIMEOUT
        STARTUP_TIMEOUT = STOP_TIMEOUT = args.timeout
    if args.silent:
        App.stdout = None

    if args.appname == 'all':
        print
        for appname in config.sections():
            print appname.center(100, '*')
            try:
                exec('App(Cfg(config.items(\'%s\'))).%s()' % (appname, args.action))
            except SystemExit:
                pass
            except Exception, e:
                App.error(str(e))
                pass
            print '*' * 100,'\n'
    else:
        print
        exec('App(Cfg(config.items(\'%s\'))).%s()' % (args.appname, args.action))
        print

if __name__=='__main__':
    main()
