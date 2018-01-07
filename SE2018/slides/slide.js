function Slide()
{
    // Create a slide object
}

Slide.prototype.load = function()
{
    // Run when a slide is 'created'
    // Slides could persist for a long time, so don't hog resources!
    
}


Slide.prototype.unload = function()
{   
    // Run when a slide is removed permanently
}
            
Slide.prototype.prepareToDisplay = function(htmlElement, readycallback, neverreadycallback)
{
    // Run when a slide should be displayed on the htmlelement
    // Calls the ready call when done.
    // Calls neverreadycallback if there's an error and it should be skipped
    // (Side note - this allows us to use the new JS 'Promises')
    // Writes to the htmlElement provided
    

}

Slide.prototype.display = function()
{
    // Run when a slide is about to be displayed, should return the length of time in ms to display the slide for (Use case here might be video play time)
        
}

Slide.prototype.reDisplay = function()
{
    // Run if the slide content should be 'refreshed'. Return the length of time in ms to display the slide for. (Use case here might be video play time)
}


Slide.prototype.hide = function()
{
    // Run when a slide is about to be hidden again
}
