var waveBtn = (function () {
    'use strict';
    var btn = document.querySelectorAll('.wave'),
        tab = document.querySelector('.tab-bar'),
        indicator = document.querySelector('.indicator'),
        indi = 0;
    indicator.style.marginLeft = indi + 'px';
  
    for(var i = 0; i < btn.length; i++) {
      btn[i].onmousedown = function (e) {
        var newRound = document.createElement('div'),x,y;
  
        newRound.className = 'cercle';
        this.appendChild(newRound);
  
        x = e.pageX - this.offsetLeft;
        y = e.pageY - this.offsetTop;
  
        newRound.style.left = x + "px";
        newRound.style.top = y + "px";
        newRound.className += " anim";
  
        indicator.style.marginLeft = indi + (this.dataset.num-1) * 150 + 'px';
  
        setTimeout(function() {
          newRound.remove();
        }, 1200);
      };
    }
  }());