function ImageSlide(imageurl, displayTime)
{
     this.imageurl = imageurl;
     this.displayTime = displayTime;
    // Create a slide object
}

ImageSlide.prototype.load = function()
{
   
    
    // Run when a slide is 'created'
    // Slides could persist for a long time, so don't hog resources!
    
}


ImageSlide.prototype.unload = function()
{   
    // Run when a slide is removed permanently
}
            
ImageSlide.prototype.prepareToDisplay = function(htmlElement, readycallback, neverreadycallback)
{
    // Run when a slide should be displayed on the htmlelement
    // Calls the ready call when done.
    // Calls neverreadycallback if there's an error and it should be skipped
    // (Side note - this allows us to use the new JS 'Promises')
    // Writes to the htmlElement provided
    
    htmlElement.innerHTML = '<div class="imageslide"><img src="' + this.imageurl + '" class="imageslide"></img></div>'
    readycallback();
    

}

ImageSlide.prototype.display = function()
{
    // Run when a slide is about to be displayed, should return the length of time in ms to display the slide for (Use case here might be video play time)
    return this.displayTime;    
}

ImageSlide.prototype.reDisplay = function()
{
    // Run if the slide content should be 'refreshed'. Return the length of time in ms to display the slide for. (Use case here might be video play time)
}


ImageSlide.prototype.hide = function()
{
    // Run when a slide is about to be hidden again
}
