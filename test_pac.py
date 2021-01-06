from gfw2pac import genpac
# c=genpac('./resources/pac/gfwlist.txt', 'SOCKS5 127.0.0.1:90', './tt',precise=False)
# c=genpac('./resources/pac/gfwlist.txt', 'SOCKS5 127.0.0.1:90', './tt2',precise=True)
# c=genpac(proxy='SOCKS5 127.0.0.1:90', fout='./tt3',precise=True)
c=genpac(fin = './resources/pac/gfwlist.txt',
        fout = './t121', 
        proxy = 'SOCKS5 127.0.0.1:90',
        other = 'resources/pac/user-rules.txt', 
        precise = False)
# print(c)