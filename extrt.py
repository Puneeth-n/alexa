#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi:et:sw=4 ts=4
# Copyright (C) 2014 Puneeth Nanjundaswamy <puneeth@netapp.com>
#
#CONFIGURATION SECTION
url = 'www.alexa.com/topsites'
#
#
#
#
#
#
#
#Beautifulsoup imports
from bs4 import BeautifulSoup

#python imports
import argparse
import requests
import os,sys
import textwrap
import re

class FetchData():
    """ This class has various functions that can be used to fetch data from
        Alexa"""

    def __init__(self):
        """Constructor of the object"""
        description = textwrap.dedent("""crawl Alexa to fetch top websites in
                                      one/all categories.""")

        self.parser = argparse.ArgumentParser(description=description)

        self.parser.add_argument("-c", "--category", choices=['country','category','top_sites','all'],
                                 required=True,metavar='CATEGORY',
                                 action="store", help="%(choices)s")

        self.parser.add_argument("-s", "--sub_category", metavar='SUB-CATEGORY',
                                 action="store", help="Ex: country codes, Games,Arts, Business")

        self.url = url

    def parse_options(self, args=None):
        """Parse options for generic Application object"""

        # parse options
        self.args = self.parser.parse_args(args)

    def apply_options(self):
        """Configure generic Application object based on the options from
        the argparser"""
        if 'top_sites' in self.args.category:
            pass

        if 'all' in self.args.category:
            raise NotImplementedError("To be implemented!")

        if 'country' in self.args.category:
            self.url = self.url + "/countries/"
            if not self.args.sub_category:
                print ('No country code provided. Fetching country codes\n')
                string = '/topsites/countries/'
                soup = self.fetch_data(self.url)
                for link in soup.find_all(re.compile('^a')):
                    if (link.get('href') is not None) and (string in link.get('href')):
                        print link.string + ' = ' + link.get('href').replace(string, '')

                exit(1)
            self.url = self.url + self.args.sub_category.upper()

        if 'category' in self.args.category:
            self.url = self.url + "/category/Top/"
            if not self.args.sub_category:
                print ('No sub-category provided. Fetching categories\n')
                string = '/topsites/category/Top/'
                soup = self.fetch_data(self.url)
                for link in soup.find_all(re.compile('^a')):
                    if (link.get('href') is not None) and (string in link.get('href')):
                        print link.get('href').replace(string, '')

                exit(1)
            self.url = self.url + self.args.sub_category

    def fetch_data(self,url):
        r = requests.get("http://" + url)
        data = r.text
        return BeautifulSoup(data)

    def parse_data(self,soup,string):
        for link in soup.find_all(re.compile('^a')):
            if (link.get('href') is not None) and (string in link.get('href')):
                #print link.string
                print (link.get('href')).replace(string, '')

    def run(self):
        soup = self.fetch_data(self.url)
        self.parse_data(soup,'/siteinfo/')


    def main(self):
        self.parse_options()
        self.apply_options()
        self.run()

if __name__ == "__main__":
    FetchData().main()
