# -*- coding: utf-8 -*-

import telnetlib
from distutils.version import StrictVersion


def discover(configuration_endpoint, time_to_timeout=None, exclude_hostnames=False):
    host, port = configuration_endpoint.split(':')
    client = telnetlib.Telnet(host, int(port), time_to_timeout)
    try:
        client.write("version\n")
        version = client.read_until("\r\n", time_to_timeout).strip()
        version_list = version.split(" ")
        version = StrictVersion(version_list[1])
        if version >= StrictVersion('1.4.14'):
            cmd = 'config get cluster'
        else:
            cmd = 'get AmazonElastiCache:cluster'
        client.write(cmd + '\n')
        response = client.read_until("END\r\n",
                                     time_to_timeout).strip().split('\r\n')[1]
        response = response[response.find("\n"):].strip()
        r = []
        for server in response.split(' '):
            hostname, ip, port = server.split('|')
            port = int(port)
            if exclude_hostnames:
                r.append([ip, port])
            else:
                r.append([hostname, ip, port])
        return r
    finally:
        client.close()


if __name__ == '__main__':
    import sys
    memcache_servers = discover(sys.argv[1])
    print memcache_servers
