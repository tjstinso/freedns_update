import configparser,os,hashlib,ipgetter,xml.etree.ElementTree as ET,urllib.request as request

#get user options from config file
def get_user_options():
    cfg = configparser.ConfigParser()
    cfg.read_file(open('config.py'))
    opt = cfg.options('user')
    return [cfg.get('user', i) for i in opt]
    
#build sha1 hash string
def hash_str(st):
    return hashlib.sha1(st.encode('utf-8'))

#generate string for url request
def build_url_str(st):
    return 'https://freedns.afraid.org/api/?action=getdyndns&v=2&sha={}&style=xml'.format(hash_str(st).hexdigest())

#get correct elements in tree: addr, ip, update_addr
def get_request_elements(url_request):
    with request.urlopen(url_request) as f:
        root = ET.fromstring(f.read().decode('utf-8'))[0]
        return [j.text for j in [i for i in root]]

#if ips are not equal, update else, nothing
def update(ip_new, ip_old, update_url):
    print(ip_new, ip_old)
    if ip_new != ip_old:
        req = request.urlopen(update_url + '&{}'.format(ip_new))
        print(req.read())
    else:
        print('nothing to do: exiting')
    
#return string to sha1 hash
def build_hash_string(user, passwd):
    return '{}|{}'.format(user, passwd)

user_login, _password = get_user_options()
host, old_ip, url = get_request_elements(build_url_str(build_hash_string(user_login,_password)))
new_ip = ipgetter.myip()
update(new_ip, old_ip, url)


