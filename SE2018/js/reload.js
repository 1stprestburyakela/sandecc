// Poll a file called version.txt - if it changes, reload the entire page.
// Poll every 15 seconds

var version;
var xhttp=new XMLHttpRequest();
xhttp.onreadystatechange = function() {
  if (xhttp.readyState == 4 && xhttp.status == 200) {
     version = xhttp.responseText;;
  }
  
};
xhttp.open("GET", "version.txt?t="+Date(), true);
xhttp.send();


var reload = function(){

        var xhttp=new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (xhttp.readyState == 4 && xhttp.status == 200) {
             if (version != xhttp.responseText)
                {
                    window.location.reload();
                }
			}
          
        };
        xhttp.open("GET", "version.txt?t="+Date(), true);
        xhttp.send();
}

setInterval(reload, 15000);


// Use websockets to reload the page
var SEReload = function(payload)
{
    // This function is only called if the correct message type is received
    window.location.reload();  
}