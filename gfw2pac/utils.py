#!/usr/bin/python3
# -*- coding: utf-8 -*-
# change code form https://pypi.org/project/gfwlist2pac/ use python3
import pkgutil
from urllib import request, parse
import json
import logging
import base64

DEFAULT_URL = 'https://git.tuxfamily.org/gfwlist/gfwlist.git/plain/gfwlist.txt'

def get_gfwlist(fpath):
    # get gfwlist for local file or web file, then decode it, return readable gfwlist str.
    if (fpath == None or fpath ==''):
        fpath = DEFAULT_URL
    fpath_parse = parse.urlparse(fpath)
    # print(fpath_parse)
    content = ''; raw = ''
    if fpath_parse.scheme:
        # if scheme is not empyt, get gfwlist from url
        print('Downloading gfwlist from %s' % fpath)
        try:
            res = request.urlopen(fpath, timeout=10).read()
            raw = res.decode('utf-8')
        except Exception as e:
            raise e
            logging.error(e)
    else:
        # if schem if empty, use local file.
        try:
            with open(fpath, 'rb') as f:
                raw = f.read().decode('utf-8')
        except Exception as e:
            raise e
            logging.error(e)
    # if str has encode, decode it. 
    if '.' in raw:
        content = raw
    else:
        content = base64.b64decode(raw).decode('utf-8')
    return content


def add_domain_to_set(s, something):
    http = something.startswith("http:")
    https = something.startswith("https:")
    if (http or https):
        something = 'http://' + something
    u = parse.urlparse(something)
    hostname = u.hostname
    if hostname is not None:
        s.add(hostname)

def parse_gfwlist(gfwlist):
    domains = set()
    for line in gfwlist:
        if line.find('.*') >= 0:
            continue
        elif line.find('*') >= 0:
            line = line.replace('*', '/')
        if line.startswith('||'):
            line = line.lstrip('||')
        elif line.startswith('|'):
            line = line.lstrip('|')
        elif line.startswith('.'):
            line = line.lstrip('.')
        if line.startswith('!'):
            continue
        elif line.startswith('['):
            continue
        elif line.startswith('@'):
            # ignore white list
            continue
        add_domain_to_set(domains, line)
    return domains


def reduce_domains(domains):
    # reduce 'www.google.com' to 'google.com'
    # remove invalid domains
    raw = pkgutil.get_data(__package__, 'src/tld.txt')
    tld_content = raw.decode('utf-8').splitlines(False)
    # with open('resources/tld.txt','r') as f:
    #     tld_content = f.read()
    tlds = set(tld_content)
    new_domains = set()
    for domain in domains:
        domain_parts = domain.split('.')
        last_root_domain = None
        for i in range(0, len(domain_parts)):
            root_domain = '.'.join(domain_parts[len(domain_parts) - i - 1:])
            if i == 0:
                if not tlds.__contains__(root_domain):
                    # root_domain is not a valid tld
                    break
            last_root_domain = root_domain
            if tlds.__contains__(root_domain):
                continue
            else:
                break
        if last_root_domain is not None:
            new_domains.add(last_root_domain)
    return new_domains

def grep_rule(rule):
    if rule:
            # print("grep_rule@",rule)
            if rule.startswith('!'):
                return None
            if rule.startswith('['):
                return None
            return rule
    return None

def combine_lists(content, user_rule=None):
    all_rules = []
    if user_rule:
        # gfwlist.extend(user_rule.splitlines(False))
        raw = user_rule.splitlines(False)
        user_rule = list(filter(grep_rule,raw))
        all_rules.extend(user_rule)
    raw = content.splitlines(False)
    gfwlist = list(filter(grep_rule, raw))
    all_rules.extend(gfwlist)
    return all_rules

def generate_pac_fast(domains, proxy):
    # render the pac file
    raw = pkgutil.get_data(__package__, 'src/proxy.pac')
    proxy_content = raw.decode('utf-8')
    # with open('src/proxy.pac','r') as f:
    #     proxy_content = f.read()
    domains_dict = {}
    for domain in domains:
        domains_dict[domain] = 1
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__DOMAINS__',
                                          json.dumps(domains_dict, indent=2))
    return proxy_content


def generate_pac_precise(rules, proxy):
    # def grep_rule(rule):
    #     if rule:
    #             # print("grep_rule@",rule)
    #             if rule.startswith('!'):
    #                 return None
    #             if rule.startswith('['):
    #                 return None
    #             return rule
    #     return None
    # render the pac file
    raw = pkgutil.get_data(__package__,'src/abp.js')
    proxy_content = raw.decode('utf-8')
    # with open('resources/abp.js','r') as f:
    #     proxy_content = f.read()
    # rules = list(filter(grep_rule, rules))
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__RULES__', json.dumps(rules, indent=2))
    return proxy_content


def genpac(fin=None, proxy="SOCKS5 127.0.0.1:1080", fout=None, other=None,precise=True):
    gfw_rule = get_gfwlist(fin)
    if other:
        user_rule = get_gfwlist(other)
    else:
        user_rule=[]
    # if user_rule:
    #     userrule_parts = parse.urlsplit(user_rule)
    #     if not userrule_parts.scheme or not userrule_parts.netloc:
    #         # It's not an URL, deal it as local file
    #         with open(user_rule, 'rb') as f:
    #             user_rule = f.read()
    #     else:
    #         # Yeah, it's an URL, try to download it
    #         print('Downloading user rules file from %s' % user_rule)
    #         user_rule = request.urlopen(user_rule, timeout=10).read()

    gfwlist = combine_lists(gfw_rule, user_rule)
    if precise:
        pac_content = generate_pac_precise(gfwlist, proxy)
    else:
        domains = parse_gfwlist(gfwlist)
        domains = reduce_domains(domains)
        pac_content = generate_pac_fast(domains, proxy)
    if fout:
        with open(fout, 'w') as f:
            f.write(pac_content)
    return pac_content
