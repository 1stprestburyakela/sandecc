var timeoffset = Date.parse(new Date()) - Date.parse(new Date());

// This function returns the hours, minutes and seconds until the specified endtime, using timeoffset to ensure an accurate result. days = true means hours are capped at 24
// 0<=Seconds<60
// 0<=Minutes<60
// 0<=Hours <24 if days = true, else < ??
// 0<= Days if days = true, else = 0
// Hours can be more than 24!

function getTimeRemaining(endtime, days)
{
  var t = Date.parse(endtime) - (Date.parse(new Date()) - timeoffset);
  var seconds = Math.floor( ( t / (1000)) % 60 );
  var minutes = Math.floor( ( t / (1000*60)) % 60 );
  var hours   = Math.floor( ( t / (1000*60*60)) % (days==true?24:99999));
  var days    = days==true ? Math.floor( ( t / (1000*60*60*24))) : 0;
  return {
    'total': t,
    'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

// Call this function with a parsable DateTime string to initialise the timeoffset - this allows us 
// to work even if the system local time is not accurate
function setTimeOffset(serverTime)
{
    timeoffset = Date.parse(new Date()) - Date.parse(serverTime);
    console.log(timeoffset);
}

// Converts a number into a 2 digit string, with preceding zeros
function padded(value)
{
    return '0' + value.toString().slice(-2);    
}

// Set an id on the page to be a basic clock
// postmessage is the message that replaces the time when it hits 0
// WARNING - may not work well with the 4 slide model, left here as an example really
function initializeClock(id, endtime, postmessage){
  var clock = document.getElementById(id);
  var timeinterval = setInterval(
  // Run this function every second
  function(){
    var t = getTimeRemaining(endtime);
    if (t.total <= 0)
    {
        clock.innerHTML = postmessage;   
    }
    else
    {
        /*clock.innerHTML = t.hours>0 ?('hours: '+ t.hours + '<br>'):('') +
                          t.minutes>0 ?('minutes: ' + t.minutes + '<br>'):('') +
                          t.seconds>0 ?('seconds: ' + t.seconds):('');*/
          // Only display hours if above zero
          clock.innerHTML = (t.hours > 0 ? t.hours.toString() + ':' : '') +
                            (padded(t.minutes) + ':') +
                            (padded(t.seconds));
    }
    // When we hit 0, clear the ticking. No point.
    if(t.total<=0){
      clearInterval(timeinterval);
    }
  }
  ,1000);
}