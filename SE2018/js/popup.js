function SEPopup(name, css)
{
    this.name = name;
    
    this.popup = document.createElement("div");
    this.popup.id = name
    this.popup.className = css
    
    this.popupContent = document.createElement("div");
    this.popupContent.id = name + "Content"
    this.popupContent.className = css + "Content"
    
    this.popup.appendChild(this.popupContent);
    
    document.body.appendChild(this.popup);
}

SEPopup.prototype.processJSON = function(payload)
{
    values = JSON.parse(payload)
    this.displaymessage(values['html'], values['time'])    
}


SEPopup.prototype.displaymessage = function(msg, time)
{
   
    this.popupContent.innerHTML = msg;
    this.popup.style.display = "block";
    setTimeout(this.hide.bind(this), time);
}
            
SEPopup.prototype.hide = function()
{
    this.popup.style.display = "none";
}

