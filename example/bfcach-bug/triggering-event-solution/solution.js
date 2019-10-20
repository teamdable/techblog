
// solution with simulating click
// touchend without touchmove
// -> make lazy-click event
// --> if there is no click event in time interval
//     triggering click event
// --> else (click event is triggered)
//     remove click trigger.

let addLazyClick = (ele) => {
  const target = ele;
  let isMoved = false;
  const timerInterval = 200;              // Allow to be Customized
  let preventInifite = 10;              // Allow to be Customized
  const triggeringEventName = "click";      // Allow to be Customized
  const  mediateEventName = "lazy-click";  // Allow to be Customized

  let isMediateEventNameVailable = () => {
    // warn to infinite loop
    while(ele["on"+mediateEventName] === "function") {
      mediateEventName = "-" + mediateEventName;
      preventInifite--;
      if(preventInifite === 0){
        throw new Error("custom event name could be not set.");
      }
    }
  };
  try{
    isMediateEventNameVailable()
  }catch(e) {
    console.error("mediateEvent could not be used in this page");
    return;
  }

  let eventDispatcher = (targetElement, eventName) => {
    console.info("triggering " + eventName);
    let evObj = document.createEvent('Events');
    evObj.initEvent(eventName, true, false);
    targetElement.dispatchEvent(evObj);
  };

  ele.addEventListener("touchmove", () => {
    isMoved = true;
  });

  ele.addEventListener("touchend", (_event_) => {
    if(isMoved === false) {
      let _lazyClickTimer_ = undefined;
      let _remove_timer_ = () => {
        if(_lazyClickTimer_){
          console.info("remove timer " + _lazyClickTimer_);
          clearTimeout(_lazyClickTimer_);
          _lazyClickTimer_ = undefined;
        }
      };
      _lazyClickTimer_ = setTimeout(() => {
        console.info("remove " + triggeringEventName + " handler for cleartimer");
        target.removeEventListener(triggeringEventName, _remove_timer_);

        console.info("start " + mediateEventName + " event triggering.");
        eventDispatcher(target, mediateEventName);
      }, timerInterval);

      target.addEventListener(triggeringEventName, _remove_timer_);
    }
    isMoved = false;
  });

  ele.addEventListener(mediateEventName, () => eventDispatcher(target, triggeringEventName) );
}


// iOS for iframe does not trigger click event with history back
let aElements = document.querySelectorAll("a");
aElements.forEach((ele) => addLazyClick(ele));

// for debug
//let attachEventHandler = (ele) => {
//  let _attachEventHandler = (_ele_, _name_, _func_) => _ele_.addEventListener(_name_, _func_);
//  let _checkEventTrigged = (_name_) => (__e__) => {
//    console.info(_name_ + " event is triggered");
//  };
//  let _event_list_ = ["click", /*"dbclick",*/
//                    /*"mouseenter","mouseleave","mousemove","mouseout","mouseover",*/"mouseup","mousedown",
//                    "touchcancel","touchend",/*"touchmove",*/"touchstart",
//                    "lazy-click"];
//  _event_list_.forEach((_event_name_) => {
//    _attachEventHandler(ele, _event_name_, _checkEventTrigged(_event_name_));
//  })
//};
//aElements.forEach(attachEventHandler);


