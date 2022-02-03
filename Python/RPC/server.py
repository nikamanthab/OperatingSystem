from xmlrpc.server import SimpleXMLRPCServer

def addition(a, b):
    return a+b

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(addition, "add")
server.serve_forever()