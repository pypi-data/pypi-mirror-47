
Command line network lookups and operations
===========================================

This python tool implements pretty much same things as `netcalc` and `netblocks` libraries, but
with minor differences in the way things are done.

The library is intended to be usable both as a command line tool `netlookup` and as a library from
server code.

Installing
----------
    
    pip install netlookup

Command line tool `netlookup` basic usage
=========================================

Following examples illustrate Usage of netlookup tool.

Lookup details for IPv4 host with CIDR mask and IPv6 subnet:

    netlookup info 172.31.1.19/17 2c0f:fb50:4000::/56
             CIDR 172.31.0.0/17
          Netmask 255.255.128.0
          Network 172.31.0.0
        Broadcast 172.31.127.255
       First host 172.31.0.1
        Last host 172.31.127.254
      Total hosts 32766
             Next 172.31.128.0/17
         Previous 172.30.128.0/17
             Bits 10101100.00011111.00000000.00000000
      Reverse DNS 0.0.31.172.in-addr.arpa.
             CIDR 2c0f:fb50:4000::/56
          Netmask ffff:ffff:ffff:ff00::
          Network 2c0f:fb50:4000::
        Broadcast 2c0f:fb50:4000:ff:ffff:ffff:ffff:ffff
       First host 2c0f:fb50:4000::1
        Last host 2c0f:fb50:4000:ff:ffff:ffff:ffff:fffe
      Total hosts 4722366482869645213694
             Next 2c0f:fb50:4000:100::/56
         Previous 2c0f:fb50:3fff:ff00::/56
             Bits 0010110000001111:1111101101010000:0100000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000:0000000000000000
      Reverse DNS 0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.4.0.5.b.f.f.0.c.2.ip6.arpa.

Split subnet with defaults (to next smaller subnet / larger prefix):

    > netlookup split 172.31.1.19/17 2c0f:fb50:4000::/56
    172.31.0.0/18
    172.31.64.0/18
    2c0f:fb50:4000::/57
    2c0f:fb50:4000:80::/57

Split IPv4 subnets with specific prefix:

    > netlookup split --subnet-prefix 19 172.31.1.19/17 172.31.5.39/17
    172.31.0.0/19
    172.31.32.0/19
    172.31.64.0/19
    172.31.96.0/19
    172.31.0.0/19
    172.31.32.0/19
    172.31.64.0/19
    172.31.96.0/19
    
Using the python library
------------------------

TODO
