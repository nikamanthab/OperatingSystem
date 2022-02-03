import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
    print("add 1 and 2: %s" % str(proxy.add(1,2)))
    print("add 100 and 51: %s" % str(proxy.add(100, 51)))