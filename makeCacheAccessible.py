#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import stat

"""
GOAL: automate all steps needed to open Cache - see if can change
settings through Python too
"""

"""
if vista data in /u01/vista in vaa etc then pass in /u01/vista
and this will check that all dirs are group r+x and all their
CACHE.dat's are a+rw
"""
def checkVistADBs(vistaLocn):
    cntDirs = 0
    cntDirsWithCacheDAT = 0
    dirsNotGRX = []
    dirsCDNotARW = []
    for fl in os.listdir(vistaLocn):
        qdr = "{}/{}".format(vistaLocn, fl)
        if not os.path.isdir(qdr):
            continue
        cntDirs += 1
        cacheDatFL = "{}/{}".format(qdr, "CACHE.DAT")
        if not os.path.isfile(cacheDatFL):
            continue # want there to be a CACHE.DAT
        perm = os.stat(qdr)
        if not bool((perm.st_mode & stat.S_IRGRP) and (perm.st_mode & stat.S_IXGRP)):
            dirsNotGRX.append(qdr)
            continue
        perm = os.stat(cacheDatFL)
        if not bool((perm.st_mode & stat.S_IROTH) and (perm.st_mode & stat.S_IWOTH)):
            dirsCDNotARW.append(qdr)
    if len(dirsCDNotARW) or len(dirsNotGRX):
        print("{:,} directories, {:,} with CACHE.DAT, {:,} of which aren't g+rx and {:,} of whose CACHE.DAT's aren't a+rw".format(
                   cntDirs, 
                   cntDirsWithCacheDAT,
                   len(dirsNotGRX),
                   len(dirsCDNotARW)
        ))
        if len(dirsNotGRX):
            for qdr in dirsNotGRX:
                print("\tDirectory {} lacks g+rx".format(qdr))
        if len(dirsCDNotARW):
            for qdr in dirsCDNotARW:
                print("\tCache Dat in {} lacks a+rw".format(qdr))
       
        
# ################################# DRIVER #######################
               
def main():

    try:
        vistaLocn = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ <vistalocn>")

    try:
        if not os.path.isdir(vistaLocn):
            raise SystemExit("<vistalocn> not a (accessible) directory")
    except:
        raise SystemExit("<vistalocn> not a (accessible) directory")
        
    checkVistADBs(vistaLocn)
        
if __name__ == "__main__":
    main()
