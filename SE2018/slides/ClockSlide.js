// Ensure time.js is also included!

function ClockSlide(utcMinutesOffset, contentString)
{
    //console.log("ClockSlide: constructor")
    // Create a clockslide object
    
    // utcMinutesOffset is the offset in minutes of the timezone you wish to display from UTC
    // i.e BST is -60
    
    // contentString is freeform html that must contain one {0} for patching in the time
    
    this.offset = utcMinutesOffset;  // BST (GMT+1) would be -60
    this.htmlElement = null;
    this.contentString = contentString;
}

ClockSlide.prototype.load = function()
{
    //console.log("ClockSlide: load")
    // Run when a slide is 'created'
    // Slides could persist for a long time, so don't hog resources!
    // Dont need to do anything
}


ClockSlide.prototype.unload = function()
{   
    //console.log("ClockSlide: unload")
    // Run when a slide is removed permanently
    // Dont need to do anything
}
            
ClockSlide.prototype.prepareToDisplay = function(htmlElement, readycallback, neverreadycallback)
{
    //console.log("ClockSlide: prepareToDisplay")
    // Run when a slide should be displayed on the htmlelement
    // Calls the ready call when done.
    // Writes to the htmlElement provided
    
    this.htmlElement = htmlElement;
    this.updateTime();
    readycallback();
    
    
}

ClockSlide.prototype.display = function()
{
    console.log("ClockSlide: display")
    // Run when a slide is about to be displayed, should return the length of time in ms to display the slide for (Use case here might be video play time)
    this.updateTime();
    clearInterval(this.updater);
    this.updater = setInterval(this.updateTime.bind(this), 1000);
}

ClockSlide.prototype.reDisplay = function()
{
    // TODO - might get canned and rolled into display()
    //console.log("ClockSlide: reDisplay")
    // Run if the slide content should be 'refreshed'. Return the length of time in ms to display the slide for. (Use case here might be video play time)
}


ClockSlide.prototype.hide = function()
{
    console.log("ClockSlide: hide")
    
    //console.log("ClockSlide: hide")
    // Run when a slide is about to be hidden again
    clearInterval(this.updater);
}

ClockSlide.prototype.updateTime = function()
{
    //console.log("ClockSlide: update")
    date = getSyncDate()
    localoffset = date.getTimezoneOffset();
    
    // We add the localoffset, then subtract the desired offset. This creates a Date object that 
    // who's local time matches the desired time. 
    //( For example Because GMT-5 has a positive TimezoneOffset, we 'add' 5 hours so our new local time matches UTC time, then 
    // then subtract 60 minutes )
    newtime = date.getTime() + localoffset*60000 - 60000*this.offset;    
    localTime = new Date(newtime);
    clock = localTime.toLocaleTimeString("uk");   
    this.htmlElement.innerHTML = this.contentString.replace("{clock}", clock);
}
