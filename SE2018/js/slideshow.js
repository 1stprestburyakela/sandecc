// This works on the principle of a 3 slide system

// At any given point, 3 slides are loaded. 'prev', 'current' and 'next'

// When the slide show is advanced, prev is unloaded prev := current, current := next and next is loaded
// If we go backwards, the reverse is true

// In automatic operation mode, the current slide determines the time we advance on. However, if the next slide
// has not finished loading we will wait an additional second. If that is not enough time, 'next' is dropped 
// and replaced, and the current slide 'plays again'.  TODO - make this true

// Note that for a transition, only two of the slides are visible. The last one can be reloading to the next
// slide content



function SESlideShow(divelement, paused, slides) {
    // Pass in the develement to run the show on, and true/false on whether we load paused
    // Please don't give the divelement any borders - if needed nest two!
    // The divelement must be have a style of position: absolute/relative
    
    
    // Apologies, there's a bit of dependancy ickiness here. Due a refactor.
    slidetypes = 
    {
        "clock" : ClockSlide,
        "image" : ImageSlide
        
    }
    
    
    
    this.divelement = divelement;
    
    
    this.slides = new Array();
    
    // Debugging - hard code some slides
    if (slides.length == 0)
    {
        this.slides.push(new ClockSlide(-60, "1, it's currently {clock} BST", 5000))
        this.slides.push(new ClockSlide(0, "2, it's currently {clock} GMT", 5000))
        this.slides.push(new ImageSlide("images/P1010647.jpg", 5000))
        this.slides.push(new ImageSlide("images/P1010938.jpg", 5000))
    }
    
    else
    {
        for (x in slides)
        {
            type = slides[x]["type"];
            args = slides[x]["args"];
            slide = new slidetypes[type](...args);
            this.slides.push(slide);
            
        }
        
    }
    
    
    this.slideindex = 0; // Index of currently displayed slide
    
    this.displaywidth = divelement.clientWidth;
    this.displayheight = divelement.clientHeight;
    
    console.log ("SESS: width: " + this.displaywidth)
    console.log ("SESS: width: " + this.displayheight)
    
    // Target locations for each of the slides. (After the transition). Relative to 0,0 which is covering the
    // divelement
    
    this.prevposx = -this.displaywidth;
    this.prevposy = 0;
    this.currentposx = 0;
    this.currentposy = 0;
    this.nextposx = this.displaywidth;
    this.nextposy = 0;
    
    
    
    // Settings for animations
    this.animationstepcount = 100;
    this.animationstepinterval = 20;
    
    
    
    // If we resize the window, 
    window.onresize = this.resize.bind(this); 
    
    
    // Create slide carriers
    
    
    this.slidecarrier1 = document.createElement("div");
    this.slidecarrier1.id = "slideshow_slide1"
    this.slidecarrier1.className = "slideshow"
    
    this.slidecarrier2 = document.createElement("div");
    this.slidecarrier2.id = "slideshow_slide2"
    this.slidecarrier2.className = "slideshow"
    
    this.slidecarrier3 = document.createElement("div");
    this.slidecarrier3.id = "slideshow_slide3"
    this.slidecarrier3.className = "slideshow"
    
    
    
    this.divelement.appendChild(this.slidecarrier1);
    this.divelement.appendChild(this.slidecarrier2);
    this.divelement.appendChild(this.slidecarrier3);
    
    this.prev = this.slidecarrier1;
    this.current = this.slidecarrier2;
    this.next = this.slidecarrier3;
    
    
    // Load the slides
    for (i = 0; i < this.slides.length; i++)
    {
        this.slides[i].load();
    }
    
    
    // Tell the first 3 slides to get ready!
    this.current.slide = this.slides[this.slideindex];
    this.next.slide = this.slides[(this.slideindex+1) % this.slides.length];
    this.prev.slide = this.slides[(this.slides.length + this.slideindex-1) % this.slides.length];
    
    
    // TODO callback funcs
    
    noop = function(){};
    
    
    // TODO order here is important for edge cases of 1 or 2 slides. Consider making that explicit. (Linked to how we cope if we remove slides down to 1 or 2)
    this.prev.slide.prepareToDisplay(this.prev, noop, noop);
    this.current.slide.prepareToDisplay(this.current, noop, noop);
    this.next.slide.prepareToDisplay(this.next, noop, noop);
    
    
    this.current.slide.display();

    
    
    this.settargets();
    this.snapall();
    
    
    // No slide timer to start with
    this.slidetimer = null;
    
    // Start the slideshow if needed
    this.paused=true; // As we have not yet started
    if (!paused)
    {
        
        this.resume();
    }
    
    
    
   
}

SESlideShow.prototype.resize = function()
{
    // TODO recalculate stuff
    console.log ("SESS: Window resize")
}

SESlideShow.prototype.forward = function()
{
    // If we are already mid transition, finish immediately
    this.snapall();
    
    
    if (this.slides.length <= 1)
    {
        return;
        // Don't do anything
    }
    else if (this.slides.length == 2)
    {
        // Swap next and current only
        temp = this.current;
        this.current = this.next;
        this.next = temp;        
    }    
    else
    {    
        temp = this.prev;
        this.prev = this.current;
        this.current = this.next;
        this.next = temp;
    }
    
    // Tell the slides where they want to go
    this.settargets();
    
    // Stop the one we're about to unload
    this.next.slide.hide();
    // Display the one that's about to appear
    displayTime = this.current.slide.display();
    // swap the next
    this.slideindex += 1;
    loadindex = (this.slideindex + 1) % this.slides.length;
    this.next.slide = this.slides[loadindex];
    
    // TODO callback funcs
    
    noop = function(){};
    this.next.slide.prepareToDisplay(this.next, noop, noop);
    
    
    
    // We have a new next, snap that to the next position
    this.snap(this.next);
    
    // Animate the other two
    this.animate(this.current);
    this.animate(this.prev);
    
    return displayTime;
    
    
    //loadNext = new Promise(nextslide.prepareToDisplay.bind(nextslide, targetdiv)
    //loadNext.then(//func to clal when ready, func to call to skip)
}

SESlideShow.prototype.backward = function()
{
    // If we are already mid transition, finish immediately
    this.snapall();
    
    if (this.slides.length <= 2)
    {
        // Don't do anything
        return;
    }
    else
    {    
        temp = this.next;
        this.next = this.current;
        this.current = this.prev;
        this.prev = temp;        
    }
    
    this.settargets();
    
    // Stop the one we're about to unload
    this.prev.slide.hide();
    // Display the ones that's about to appear
    displayTime = this.current.slide.display();
    // swap the previous
    this.slideindex -= 1;
    loadindex = (this.slideindex -1 + this.slides.length) % this.slides.length;
    this.prev.slide = this.slides[loadindex];
    
    // TODO callback funcs
    
    noop = function(){};
    this.prev.slide.prepareToDisplay(this.prev, noop, noop);
    
    
    
    
    // We have a new previous, snap that to the next position
    this.snap(this.prev);
    
    this.animate(this.current);
    this.animate(this.next);
    return displayTime;
    
}

SESlideShow.prototype.settargets = function()
{
    this.prev.targety = this.prevposy;
    this.prev.targetx = this.prevposx;
    this.current.targety = this.currentposy;
    this.current.targetx = this.currentposx;
    this.next.targety = this.nextposy;
    this.next.targetx = this.nextposx;
    
}

SESlideShow.prototype.snapall = function()
{    
    this.snap(this.prev);
    this.snap(this.current);
    this.snap(this.next);    
}

SESlideShow.prototype.snap = function(slide)
{
    // Stop any running animation
    clearTimeout(slide.animator);
    slide.style.top = slide.targety +"px";
    slide.style.left = slide.targetx +"px";     
}

SESlideShow.prototype.animate = function(slide)
{
    
    slide.frame=0;
    clearTimeout(slide.animator);
    
    slide.originaly = parseInt(slide.style.top)
    slide.originalx = parseInt(slide.style.left)
    
    slide.animator = setTimeout(this.animateframe.bind(this,slide), this.animationstepinterval);
    
}

SESlideShow.prototype.animateframe = function(slide)
{
    slide.frame += 1;
    //debugger
    
    
    
    if (slide.frame < this.animationstepcount)
    {
        slide.style.top = (slide.originaly  + slide.frame * ((slide.targety - slide.originaly)/this.animationstepcount)) + "px"
        slide.style.left = (slide.originalx  + slide.frame * ((slide.targetx - slide.originalx)/this.animationstepcount)) + "px"
    
        slide.animator = setTimeout(this.animateframe.bind(this,slide), this.animationstepinterval);
    }
    else
    {
        // In case of rounding errors, on the last step do a snap as well.
        this.snap(slide);
    }
}


SESlideShow.prototype.animateprev = function()
{
    
}


SESlideShow.prototype.pause = function()
{
    if (!this.paused)
    {
        this.paused = true;
        clearTimeout(this.slidetimer);
    }
    
}

SESlideShow.prototype.resume = function()
{
    if (this.paused)
    {
        this.paused = false;
        this.slidetimer = setTimeout(this.autoslide.bind(this), this.forward());
    }
    
}

SESlideShow.prototype.autoslide = function()
{
    this.slidetimer = setTimeout(this.autoslide.bind(this), this.forward());
    
}