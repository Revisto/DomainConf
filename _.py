from os import system 
import sys


def Bind9(Domain,Ip):
    dbData='''
$ORIGIN {Domain}.
$TTL    604800

@       IN      SOA     ns1.{Domain}. root.{Domain}. (
                        401         ; Serial
                        604800         ; Refresh
                        86400         ; Retry
                    2419200         ; Expire
                        604800 )       ; Negative Cache TTL

;

{Domain}.       IN      NS      ns1.{Domain}.
{Domain}.       IN      NS      ns2.{Domain}.
{Domain}.       IN      A       {Ip}
ns1.{Domain}.   IN      A       {Ip}
ns2.{Domain}.   IN      A       {Ip}
www.{Domain}.   IN      A       {Ip}
mail	IN	A	{Ip}
@       IN        MX 5 mail
        '''.format(Domain=Domain,Ip=Ip)
        
    with open('/etc/bind/'+'db.'+Domain,'w') as f:
        f.write(str(dbData))
        f.close()
        
    local='''
    
zone "'''+Domain+'''" {
    type master;
    file "/etc/bind/db.'''+Domain+'''";
    allow-transfer { '''+Ip+''';};
};

    '''
    
    with open('/etc/bind/named.conf.local', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(local + '\n' + content)
        f.close()
        
    system('sudo systemctl restart bind9')
    
def Nginx(Domain,PortForReverseProxy):
    
    NginxConf='''
    
server {
	
    server_name www.'''+Domain+''' '''+Domain+''';

    location / {
       proxy_pass http://127.0.0.1:'''+PortForReverseProxy+''';
    }
    }

    '''

    with open('/etc/nginx/sites-available/'+Domain,'w') as f:
        f.write(str(NginxConf))
        f.close()
        
    system('sudo ln -s /etc/nginx/sites-available/{Domain} /etc/nginx/sites-enabled/'.format(Domain=Domain))
    system('systemctl restart nginx.service')



if len(sys.argv)==4:
    Bind9(sys.argv[1],sys.argv[2])
    Nginx(sys.argv[1],sys.argv[3])

else:
    print ("python ME.py Domain Ip PortForReverseProxy")
