(function(){
  const ua=navigator.userAgent||'';
  window.MIYT_PLATFORM={
    isTizen:/Tizen|SMART-TV/i.test(ua),
    isWebOS:/Web0S|webOS|NetCast/i.test(ua),
    exit:function(){
      try{if(window.tizen&&tizen.application){tizen.application.getCurrentApplication().exit();return;}}catch(e){}
      try{if(window.webOS&&webOS.platformBack){webOS.platformBack();return;}}catch(e){}
      try{window.close();}catch(e){}
    }
  };
})();
