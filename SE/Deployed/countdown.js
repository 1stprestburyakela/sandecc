function getTimeRemaining(endtime){
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor( (t/1000) % 60 );
  var minutes = Math.floor( (t/1000/60) % 60 );
  var hours = Math.floor( (t/(1000*60*60)) );
  //var days = Math.floor( t/(1000*60*60*24) );
  return {
    'total': t,
    //'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(id, endtime, postmessage){
  var clock = document.getElementById(id);
  var timeinterval = setInterval(function(){
    var t = getTimeRemaining(endtime);
    if (t.total < 0)
    {
        clock.innerHTML = postmessage;   
    }
    else
    {
        /*clock.innerHTML = t.hours>0 ?('hours: '+ t.hours + '<br>'):('') +
                          t.minutes>0 ?('minutes: ' + t.minutes + '<br>'):('') +
                          t.seconds>0 ?('seconds: ' + t.seconds):('');*/
          clock.innerHTML = (t.hours>=0 ? t.hours.toString() + ':':'') +
                            (t.minutes>=0 ?('0' + t.minutes.toString()).slice(-2) + ':':'') +
                            (t.seconds>=0 ?('0' + t.seconds.toString()).slice(-2):'');
    }
    if(t.total<=0){
      clearInterval(timeinterval);
    }
  },1000);
}