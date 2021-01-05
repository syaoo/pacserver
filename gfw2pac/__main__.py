#!/usr/bin/python3
# -*- coding: utf-8 -*-
# change code form https://pypi.org/project/gfwlist2pac/ use python3
from utils import genpac
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                        help='path to gfwlist', metavar='GFWLIST')
    parser.add_argument('-f', '--file', dest='output', required=True,
                        help='path to output pac', metavar='PAC')
    parser.add_argument('-p', '--proxy', dest='proxy', required=True,
                        help='the proxy parameter in the pac file, '
                             'for example, "SOCKS5 127.0.0.1:1080;"',
                        metavar='PROXY')
    parser.add_argument('--user-rule', dest='user_rule',
                        help='user rule file, which will be appended to'
                             ' gfwlist')
    parser.add_argument('--precise', dest='precise', action='store_true',
                        help='use adblock plus algorithm instead of O(1)'
                             ' lookup')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    # genpac(fin=None, proxy="SOCKS5 127.0.0.1:1080", fout=None, other=None,precise=True)
    genpac(fin = args.input,
            fout = args.output, 
            proxy = args.proxy,
            other = args.user_rule, 
            precise = args.precise)
    # c=genpac('./resources/pac/gfwlist.txt', 'SOCKS5 127.0.0.1:90', './tt',precise=False)
    # c=main('', 'SOCKS5 127.0.0.1:90', './pac/tt',precise=True)