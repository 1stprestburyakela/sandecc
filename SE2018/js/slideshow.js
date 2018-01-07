// This works on the principle of a 3 slide system

// At any given point, 3 slides are loaded. 'prev', 'current' and 'next'

// When the slide show is advanced, prev is unloaded prev := current, current := next and next is loaded
// If we go backwards, the reverse is true

// In automatic operation mode, the current slide determines the time we advance on. However, if the next slide
// has not finished loading we will wait an additional second. If that is not enough time, 'next' is dropped 
// and replaced, and the current slide 'plays again'. 

// Note that for a transition, only two of the slides are visible. The last one can be reloading to the next
// slide content


function SESlideShow(divelement, paused) {
    // Pass in the develement to run the show on, and true/false on whether we load paused
    // Please don't give the divelement any borders - if needed nest two!
    // The divelement must be have a style of position: absolute/relative
    
    this.divelement = divelement;
    this.paused = paused;
    
    this.slides = new Array();
    
    // Debugging - hard code some slides
    this.slides.push(new ClockSlide(-60, "1, it's currently {clock} BST"))
    this.slides.push(new ClockSlide(-60, "2, it's currently {clock} BST"))
    this.slides.push(new ClockSlide(-60, "3, it's currently {clock} BST"))
    
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
    this.animationstepcount = 50;
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
    
    this.current.slide.prepareToDisplay(this.current, noop, noop);
    this.next.slide.prepareToDisplay(this.next, noop, noop);
    this.prev.slide.prepareToDisplay(this.prev, noop, noop);
    
    this.current.slide.display();

    
    
    this.settargets();
    this.snapall();
    
    
    
    
    
    
    
   
}

SESlideShow.prototype.resize = function()
{
    // TODO recalculate stuff
    console.log ("SESS: Window resize")
}

SESlideShow.prototype.forward = function()
{
    // If we are already mid transition, finish immediately
    this.snapall()
    
    temp = this.prev;
    this.prev = this.current;
    this.current = this.next;
    this.next = temp;
    this.settargets();
    
    
    this.next.slide.hide();
    this.current.slide.display();
    // swap the next
    this.next.slide.prepareToDisplay;
    
    
    // We have a new next, snap that to the next position
    this.snap(this.next);
    
    
    this.animate(this.current);
    this.animate(this.prev);
    
    //loadNext = new Promise(nextslide.prepareToDisplay.bind(nextslide, targetdiv)
    //loadNext.then(//func to clal when ready, func to call to skip)
}

SESlideShow.prototype.backward = function()
{
    // If we are already mid transition, finish immediately
    
    temp = this.next;
    this.next = this.current;
    this.current = this.prev;
    this.prev = temp;
    this.settargets();
    
    this.prev.slide.hide();
    this.current.slide.display();
    // swap the previous
    this.prev.slide.prepareToDisplay;
    
    // We have a new previous, snap that to the next position
    this.snap(this.prev);
    
    this.animate(this.current);
    this.animate(this.next);
    
    
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
    
}

SESlideShow.prototype.resume = function()
{
    
}