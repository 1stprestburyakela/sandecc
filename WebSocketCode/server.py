from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

clients = []
class SimpleChat(WebSocket):

    def handleMessage(self):
       print self.data
       for client in clients:
          if client != self:
             #client.sendMessage(self.address[0] + u' - ' + self.data)
             client.sendMessage(self.data)

    def handleConnected(self):
       print(self.address, 'connected')
       #self.sendMessage("hello")
       self.sendMessage(u'{"type":"location","location":"' +self.address[0]+ '"}')
       for client in clients:
          client.sendMessage(self.address[0] + u' - connected')
       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')

server = SimpleWebSocketServer('', 8000, SimpleChat)
server.serveforever()