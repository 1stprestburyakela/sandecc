/*
 WebSocket wrapper for S+E
 Messages should be sent as JSON is the format:
 'type':'string'
 'location':['string']
 'payload':???
 
 Location can be thought of as the address, and if the intersection of location with this.locations is non empty
 then the message will be processed.
*/

/* We assume all inbound messages to be authenic, so do no authentication on the client side.
This means anyone who can get the WebSocketServer to send a message can do anything to this client */

function SEWebSocket(url, uselocalipaslocation) {
    this.url = url;
    this.messagehandlers = {};   // Map of types to lists of functions
    this.locations = new Set(['all', 'backdoor'])  // backdoor can never be removed, ensuring we don't accidentally lock ourselves out
    
    if (uselocalipaslocation)
    {
        this.getIP();
    }
    
    // Add in two functions that allow us to add and remove locations remotely
    this.addRoute('addLocation', this.addLocation.bind(this));
    this.addRoute('removeLocation', this.removeLocation.bind(this));
   
}

// Basic functions ------------------------------------------
// open the socket
SEWebSocket.prototype.open = function()
{
    console.log("SEW: Opening SEWebsocket to " + this.url)
    // Ensures only one connection is open at a time
    if(this.websocket !== undefined && this.websocket.readyState !== WebSocket.CLOSED){
       console.log("SEW: Can't open an open socket")
       return;
    }
    
    
    this.websocket = new WebSocket(this.url);
    
    
 
    this.websocket.onmessage = this.onMessage.bind(this);
    this.websocket.onclose = this.onClose.bind(this);
    this.websocket.onerror = this.onError.bind(this);
    this.websocket.onopen = this.onOpen.bind(this);
};

// close the socket
SEWebSocket.prototype.close = function()
{
    this.webSocket.close();        
};

// send a message
SEWebSocket.prototype.send = function(message) 
{
    this.websocket.send(message);
};

// Receive a message
SEWebSocket.prototype.onMessage = function(event) 
{
    message = event.data;    
    console.log("SEW: Message received: " + message)
    
    try
    {
        messageParsed = JSON.parse(message)
        
        // Check we have a matching location
        for (loc of messageParsed['location'])
        {
            if (this.locations.has(loc))
            {
                console.log("SEW: Message for this location")
                // Now call all handlers for that type
                if (messageParsed['type'] in this.messagehandlers)
                {
                    for (handler of this.messagehandlers[messageParsed['type']])
                    {
                        // Don't let one bad handler stop us
                        try
                        {
                            handler(messageParsed['payload'])
                        }
                        catch (e)
                        {
                            console.log("Handler error: " + e.toString())
                        }
                    }
                }
                
                
                // Don't want to process the message twice, so stop now
                break
            }
        }
    
    }
    catch (e)
    {
        console.log("Could not process message: " +e.toString())
    }
};

// Websocket functions ----------------------------------------

// Channel opened
SEWebSocket.prototype.onOpen = function(event) 
{
    console.log("SEW: Connection open");
};

// Channel closed - try to reopen in 5 seconds
SEWebSocket.prototype.onClose = function(event) 
{
    console.log("SEW: Connection closed");    
    setTimeout(this.open.bind(this), 5000);    
};

// Channel error - try to reopen in 5 seconds
SEWebSocket.prototype.onError = function(event) 
{
    console.log(event);  
    setTimeout(this.open.bind(this), 5000);        
};

// Location functions -----------------------------------------------

// Add a new location
SEWebSocket.prototype.addLocation = function(name) 
{
    this.locations.add(name)
    console.log("SEW locations: " + [...this.locations])
};

// Remove a location
SEWebSocket.prototype.removeLocation = function(name) 
{
    // Don't allow 'backdoor' to be removed
    if (name != "backdoor")
    {
        this.locations.delete(name)
    }
    
    console.log("SEW locations: " + [...this.locations])
};

SEWebSocket.prototype.getIP = function(){
    
    window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;   //compatibility for firefox and chrome
    var pc = new RTCPeerConnection({iceServers:[]})
    var noop = function(){};      
    
    pc.createDataChannel("");    //create a bogus data channel
    pc.createOffer(pc.setLocalDescription.bind(pc), noop);    // create offer and set local description
    
    SEW = this
    pc.onicecandidate = function (ice) 
        {  //listen for candidate events
        try
            {
                if(!ice || !ice.candidate || !ice.candidate.candidate)  return;
                
                ip = ice.candidate.candidate.split(" ")[4]
                console.log('SEW: my IP: ', ip);
                
                SEW.addLocation(ip)
            }
            catch(e)
            {
                
            }
        };
}




// Message routing --------------------------------------------------

// Add a listener for a specific message type.
// Messages can be addressed by location, name, or 'all'

// Add the handler 'func' for message of specified type. Func takes one argument, which will be the payload of the message
SEWebSocket.prototype.addRoute = function(type, func)
{
    if (type in this.messagehandlers)
    {
        current = this.messagehandlers[type]
    }
    else
    {
        current = new Set()
    }
    
    current.add(func);    
    this.messagehandlers[type] = current;    
    
}

// And the inverse, remove
SEWebSocket.prototype.removeRoute = function(type, func)
{
    if (type in this.messagehandlers)
    {
        current = this.messagehandlers[type]
    }
    else
    {
        return
    }
    
    current.delete(func);    
    this.messagehandlers[type] = current;    
    
}