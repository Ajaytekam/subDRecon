#!/usr/bin/python3  

from libs.telegramText import NotifyTelegramBot 
import libs.coloredOP as co
from pathlib import Path
import dnsgen 
import os
import datetime
import re
import requests
import subprocess 
import argparse 
import sys

def executeCommand(COMMAND, verbose=False):
    try:
        subprocess.run(COMMAND, shell=True, check=True, text=True)
        if verbose:
            print("\t"+co.bullets.OK+co.colors.GREEN+"Command Executed Successfully."+co.END)
    except subprocess.CalledProcessError as e:
        print("\t"+co.bullets.ERROR+co.colors.BRED+"Error During Command Execution.!!"+co.END)
        print(e.output)
    return 

def ValideteDomain(domain):
    regex =  "^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}"
    d = re.compile(regex)
    if(re.search(d, domain)):
        return True
    else:
        return False

def PassiveRecon(Domain, OPDir):
    os.chdir(OPDir)
    # Amass Scan
    COMMAND = 'amass enum --passive -o amass.txt -d {} > /dev/null 2>&1'.format(Domain)
    print(co.bullets.CProcess, co.colors.GREEN+"Passive subdomain enum with amass"+co.END)
    executeCommand(COMMAND)
    # assetfinder scan 
    COMMAND = 'assetfinder --subs-only {} >> assetfinder.txt'.format(Domain)
    print(co.bullets.CProcess, co.colors.GREEN+"Passive subdomain enum with assetfinder"+co.END)
    executeCommand(COMMAND)
    # findomain scan 
    COMMAND = 'findomain -q --target {} --threads 20 >> findomain.txt'.format(Domain)
    print(co.bullets.CProcess, co.colors.GREEN+"Passive subdomain enum with findomain"+co.END)
    executeCommand(COMMAND)
    # merging and sorting all files       
    COMMAND = 'cat amass.txt assetfinder.txt findomain.txt | sort -u >> PassiveSubD.txt'
    print(co.bullets.CProcess, co.colors.GREEN+"Merging all Subdomain files"+co.END)
    executeCommand(COMMAND)
    # delete all tem files 
    if os.path.isfile("amass.txt"):
        os.remove("amass.txt")
    if os.path.isfile("assetfinder.txt"):
        os.remove("assetfinder.txt")
    if os.path.isfile("findomain.txt"):
        os.remove("findomain.txt")
    os.chdir("..")

def ActiveRecon(Domain, OPDir):
    os.chdir(OPDir)
    # Generating domains with dnsgen 
    print(co.bullets.CProcess, co.colors.GREEN+"Generating subdomain with dnsgen"+co.END)
    with open("dnsgen_subs.txt", "w") as f:
        for r in dnsgen.generate([Domain]):
            f.write("{}\n".format(r))
    # Generate CommonSpeak2 subdomain list
    # CommonSpeak2 repo : 
    print(co.bullets.CProcess, co.colors.GREEN+"Generating subdomain using CommanSpeak2 wordlist"+co.END)
    WordList = "/root/tools/wordlists/commonspeak2.txt"
    if os.path.isfile(WordList):
        with open("commonspeak2_subd.txt", "w") as f:
            for word in open(WordList, "r"):
                f.write("{}.{}\n".format(word.strip("\n"), Domain))
    # merging and sorting all files       
    COMMAND = 'cat dnsgen_subs.txt commonspeak2_subd.txt PassiveSubD.txt | sort -u >> AllSubD.txt'
    print(co.bullets.CProcess, co.colors.GREEN+"Merging all Subdomain files"+co.END)
    executeCommand(COMMAND)
    # run Massdns scan on AllSubD.txt list
    # resolver is downloaded from repository : https://github.com/janmasarik/resolvers
    COMMAND = 'wget https://raw.githubusercontent.com/janmasarik/resolvers/master/resolvers.txt > /dev/null 2>&1'
    print(co.bullets.CProcess, co.colors.GREEN+"Downloading working resolver list"+co.END)
    executeCommand(COMMAND)
    COMMAND = 'massdns -s 15000 -r resolvers.txt -t A AllSubD.txt -o S -w massdnsResults.txt > /dev/null 2>&1'
    print(co.bullets.CProcess, co.colors.GREEN+"Running massdns on collected subdomains"+co.END)
    executeCommand(COMMAND)
    # delete temp files 
    if os.path.isfile("dnsgen_subs.txt"):
        os.remove("dnsgen_subs.txt")
    if os.path.isfile("commonspeak2_subd.txt"):
        os.remove("commonspeak2_subd.txt")
    if os.path.isfile("resolvers.txt"):
        os.remove("resolvers.txt")
    os.chdir("..")

def Banner():
    print("############################################")
    print("# "+co.BOLD+co.colors.GREEN+"subDRecon : SubDomain Reconnaissance Tool"+co.END)
    print("# Author  : "+co.colors.CYAN+"Ajay Kumar Tekam [ ajaytekam.github.io ]"+co.END)
    print("# Version : 0.1")
    print("############################################\n")

def printInfo(Domain, OPDir):
    print(co.bullets.INFO, co.colors.CYAN+"Target Domain : {}".format(Domain)+co.END)
    print(co.bullets.INFO, co.colors.CYAN+"Result Dir    : {}\n".format(OPDir)+co.END)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Domain name to perform reconnaissance")
    parser.add_argument("-o", "--out", help="Filename to perform operations on")
    parser.add_argument("-p", "--passive", help="Perform only Passive Reconnaissance on target domain", action="store_true")
    args = parser.parse_args()
    # Check argument
    if args.url is None:
        Banner()
        parser.print_help()
        sys.exit()
    ## GLOBAL Vars
    Banner()
    Domain = ""  # Domain name with protocol 
    OPDir = ""   # Output Directory 
    # validae url
    if(ValideteDomain(args.url)):
        Domain = args.url 
    else:
        print(co.bullets.ERROR, co.colors.BRED+"Invalid Domain:{}".format(args.url)+co.END)
        sys.exit()
    # Create output dir 
    if args.out is not None:
        OPDir = args.out
        if os.path.isdir(OPDir):
            print(co.bullets.INFO, co.colors.CYAN+"{} already exists...".format(OPDir)+co.END)
            print(co.bullets.INFO, co.colors.CYAN+"Adding time-stamp into the directory name as suffix"+co.END)
            Date = str(datetime.datetime.now())
            WORKDIR = re.sub("-|:|\.|\ ", "_", Date)
            OPDir += "_{}".format(WORKDIR)
    else:
        OPDir = "./subDomainrecon_{}".format(Domain)
        if os.path.isdir(OPDir):
            print(co.bullets.INFO, co.colors.CYAN+"{} already exists...".format(OPDir)+co.END)
            print(co.bullets.INFO, co.colors.CYAN+"Adding time-stamp into the directory name as suffix"+co.END)
            Date = str(datetime.datetime.now())
            WORKDIR = re.sub("-|:|\.|\ ", "_", Date)
            OPDir += "_{}".format(WORKDIR)
    os.mkdir(OPDir) 
    # starts reconnaissance
    txtmessage = "Active subdomain Reconnaissance Staretd for domain : {}".format(Domain)
    NotifyTelegramBot(txtmessage)
    if args.passive:
        printInfo(Domain, OPDir)
        PassiveRecon(Domain, OPDir)
    else:
        printInfo(Domain, OPDir)
        PassiveRecon(Domain, OPDir)
        ActiveRecon(Domain, OPDir)
    txtmessage = "SubDomain reconnaissance Completed : {}".format(Domain)
    NotifyTelegramBot(txtmessage)
    
if __name__ == "__main__":
    main()
