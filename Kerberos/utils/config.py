#!/usr/bin/python3

'''
Initially 3 Keys are shared amony 4 parties
----------------------------------------------------
1. Client & Auth server : Password of the Client
2. Auth server & TGS    : Secret Key only known to both 
3. TGS & server         : Secret Key only known to both
'''


# No.of connections to accept before timeout
MAX_CONNECTIONS = 5

# Auth server run on
AS_ADD = ('localhost', 4444)