#!/usr/bin/env python
#
# Service Activation Engine
#
import os,sys,getopt

def usage():
    print "USAGE:"
    print "%s [-h] [-v] [-f] [-c <config>]"%sys.argv[0]
    print "\t-h\t\t- Help screen"
    print "\t-f\t\t- Do not daemonize, run at the foreground"
    print "\t-c <config>\t\t- Read <config> file (etc/noc-activator.conf by default)"

#
def main():
    daemonize=True
    config_path=None

    optlist,optarg=getopt.getopt(sys.argv[1:],"hfc:")
    for k,v in optlist:
        if k=="-h":
            usage()
            sys.exit(0)
        elif k=="-f":
            daemonize=False
        elif k=="-c":
            config_path=v
    from noc.sa.activator import Activator
    activator=Activator(config_path,daemonize)
    activator.run()
    
if __name__ == '__main__':
    d=os.path.dirname(sys.argv[0])
    sys.path.insert(0,os.path.join(d,"..",".."))
    sys.path.insert(0,os.path.join(d,".."))
    sys.path.insert(0,d)
    main()