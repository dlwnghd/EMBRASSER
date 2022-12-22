// 매칭성공률 도넛 차트 js
var Dial1 = function(ring1) {
    this.ring1 = ring1;
    this.size = this.ring1.dataset.size;
    this.strokeWidth = this.size / 8;
    this.radius = (this.size / 2) - (this.strokeWidth / 2);
    this.value = this.ring1.dataset.value;
    this.direction = this.ring1.dataset.arrow;
    this.svg;
    this.defs;
    this.slice;
    this.overlay;
    this.text;
    this.arrow;
    this.create();
}

Dial1.prototype.create = function() {
    this.createSvg();
    this.createDefs();
    this.createSlice();
    this.createOverlay();
    this.createText();
    this.createArrow();
    this.ring1.appendChild(this.svg);
};

Dial1.prototype.createSvg = function() {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute('width', this.size + 'px');
    svg.setAttribute('height', this.size + 'px');
    this.svg = svg;
};

Dial1.prototype.createDefs = function() {
    var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    var linearGradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
    linearGradient.setAttribute('id', 'gradient');
    var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
    stop1.setAttribute('stop-color', '#8a8bf3');
    stop1.setAttribute('offset', '0%');
    linearGradient.appendChild(stop1);
    var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
    stop2.setAttribute('stop-color', '#D2DAFF');
    stop2.setAttribute('offset', '100%');
    linearGradient.appendChild(stop2);
    var linearGradientBackground = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
    linearGradientBackground.setAttribute('id', 'gradient-background');
    var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
    stop1.setAttribute('stop-color', 'rgba(150, 150, 150, 0.15)');
    stop1.setAttribute('offset', '0%');
    linearGradientBackground.appendChild(stop1);
    var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
    stop2.setAttribute('stop-color', 'rgba(0, 0, 0, 0.05)');
    stop2.setAttribute('offset', '100%');
    linearGradientBackground.appendChild(stop2);
    defs.appendChild(linearGradient);
    defs.appendChild(linearGradientBackground);
    this.svg.appendChild(defs);
    this.defs = defs;
};

Dial1.prototype.createSlice = function() {
    var slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
    slice.setAttribute('fill', 'none');
    slice.setAttribute('stroke', 'url(#gradient)');
    slice.setAttribute('stroke-width', this.strokeWidth);
    slice.setAttribute('transform', 'translate(' + this.strokeWidth / 2 + ',' + this.strokeWidth / 2 + ')');
    slice.setAttribute('class', 'animate-draw');
    this.svg.appendChild(slice);
    this.slice = slice;
};

Dial1.prototype.createOverlay = function() {
    var r = this.size - (this.size / 2) - this.strokeWidth / 2;
    var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute('cx', this.size / 2);
    circle.setAttribute('cy', this.size / 2);
    circle.setAttribute('r', r);
    circle.setAttribute('fill', 'url(#gradient-background)');
    this.svg.appendChild(circle);
    this.overlay = circle;
};

Dial1.prototype.createText = function() {
    var fontSize = this.size / 3.5;
    var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute('x', (this.size / 2) + fontSize / 7.5);
    text.setAttribute('y', (this.size / 2) + fontSize / 4);
    text.setAttribute('font-family', 'Century Gothic, Lato');
    text.setAttribute('font-size', fontSize);
    text.setAttribute('fill', '#FFF');
    text.setAttribute('text-anchor', 'middle');
    var tspanSize = fontSize / 3;
    text.innerHTML = 0 + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
    this.svg.appendChild(text);
    this.text = text;
};

Dial1.prototype.createArrow = function() {
    var arrowSize = this.size / 10;
    var arrowYOffset, m;
    if(this.direction === 'up') {
        arrowYOffset = arrowSize / 2;
        m = -1;
    }
    else if(this.direction === 'down') {
        arrowYOffset = 0;
        m = 1;
    }
    var arrowPosX = ((this.size / 2) - arrowSize / 2);
    var arrowPosY = (this.size - this.size / 3) + arrowYOffset;
    var arrowDOffset =  m * (arrowSize / 1.5);
    var arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
    arrow.setAttribute('d', 'M 0 0 ' + arrowSize + ' 0 ' + arrowSize / 2 + ' ' + arrowDOffset + ' 0 0 Z');
    arrow.setAttribute('fill', '#FFF');
    arrow.setAttribute('opacity', '0.6');
    arrow.setAttribute('transform', 'translate(' + arrowPosX + ',' + arrowPosY + ')');
    this.svg.appendChild(arrow);
    this.arrow = arrow;
};

Dial1.prototype.animateStart = function() {
    var v = 0;
    var self = this;
    var intervalOne = setInterval(function() {
        var p = +(v / self.value).toFixed(2);
        var a = (p < 0.95) ? 2 - (2 * p) : 0.05;
        v += a;
        // Stop
        if(v >= +self.value) {
            v = self.value;
            clearInterval(intervalOne);
        }
        self.setValue(v);
    }, 10);
};

Dial1.prototype.animateReset = function() {
    this.setValue(0);
};

Dial1.prototype.polarToCartesian = function(centerX, centerY, radius, angleInDegrees) {
  var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;
  return {
    x: centerX + (radius * Math.cos(angleInRadians)),
    y: centerY + (radius * Math.sin(angleInRadians))
  };
}

Dial1.prototype.describeArc = function(x, y, radius, startAngle, endAngle){
    var start = this.polarToCartesian(x, y, radius, endAngle);
    var end = this.polarToCartesian(x, y, radius, startAngle);
    var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
    var d = [
        "M", start.x, start.y, 
        "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
    ].join(" ");
    return d;       
}

Dial1.prototype.setValue = function(value) {   
      var c = (value / 100) * 360;
      if(c === 360)
         c = 359.99;
      var xy = this.size / 2 - this.strokeWidth / 2;
      var d = this.describeArc(xy, xy, xy, 180, 180 + c);
    this.slice.setAttribute('d', d);
    var tspanSize = (this.size / 3.5) / 3;
    this.text.innerHTML = Math.floor(value) + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
};

//
// Usage
//

var containers = document.getElementsByClassName("donutchart");
var dial = new Dial1(containers[0]);
dial.animateStart();

// =====================
// ring2
var Dial1 = function(ring1) {
  this.ring1 = ring1;
  this.size = this.ring1.dataset.size;
  this.strokeWidth = this.size / 8;
  this.radius = (this.size / 2) - (this.strokeWidth / 2);
  this.value = this.ring1.dataset.value;
  this.direction = this.ring1.dataset.arrow;
  this.svg;
  this.defs;
  this.slice;
  this.overlay;
  this.text;
  this.arrow;
  this.create();
}

Dial1.prototype.create = function() {
  this.createSvg();
  this.createDefs();
  this.createSlice();
  this.createOverlay();
  this.createText();
  this.createArrow();
  this.ring1.appendChild(this.svg);
};

Dial1.prototype.createSvg = function() {
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute('width', this.size + 'px');
  svg.setAttribute('height', this.size + 'px');
  this.svg = svg;
};

Dial1.prototype.createDefs = function() {
  var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  var linearGradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradient.setAttribute('id', 'gradient');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', '#6E4AE2');
  stop1.setAttribute('offset', '0%');
  linearGradient.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', '#78F8EC');
  stop2.setAttribute('offset', '100%');
  linearGradient.appendChild(stop2);
  var linearGradientBackground = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradientBackground.setAttribute('id', 'gradient-background');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', 'rgba(0, 0, 0, 0.2)');
  stop1.setAttribute('offset', '0%');
  linearGradientBackground.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', 'rgba(0, 0, 0, 0.05)');
  stop2.setAttribute('offset', '100%');
  linearGradientBackground.appendChild(stop2);
  defs.appendChild(linearGradient);
  defs.appendChild(linearGradientBackground);
  this.svg.appendChild(defs);
  this.defs = defs;
};

Dial1.prototype.createSlice = function() {
  var slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
  slice.setAttribute('fill', 'none');
  slice.setAttribute('stroke', 'url(#gradient)');
  slice.setAttribute('stroke-width', this.strokeWidth);
  slice.setAttribute('transform', 'translate(' + this.strokeWidth / 2 + ',' + this.strokeWidth / 2 + ')');
  slice.setAttribute('class', 'animate-draw');
  this.svg.appendChild(slice);
  this.slice = slice;
};

Dial1.prototype.createOverlay = function() {
  var r = this.size - (this.size / 2) - this.strokeWidth / 2;
  var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  circle.setAttribute('cx', this.size / 2);
  circle.setAttribute('cy', this.size / 2);
  circle.setAttribute('r', r);
  circle.setAttribute('fill', 'url(#gradient-background)');
  this.svg.appendChild(circle);
  this.overlay = circle;
};

Dial1.prototype.createText = function() {
  var fontSize = this.size / 3.5;
  var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute('x', (this.size / 2) + fontSize / 7.5);
  text.setAttribute('y', (this.size / 2) + fontSize / 4);
  text.setAttribute('font-family', 'Century Gothic, Lato');
  text.setAttribute('font-size', fontSize);
  text.setAttribute('fill', '#FFF');
  text.setAttribute('text-anchor', 'middle');
  var tspanSize = fontSize / 3;
  text.innerHTML = 0 + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
  this.svg.appendChild(text);
  this.text = text;
};

Dial1.prototype.createArrow = function() {
  var arrowSize = this.size / 10;
  var arrowYOffset, m;
  if(this.direction === 'up') {
      arrowYOffset = arrowSize / 2;
      m = -1;
  }
  else if(this.direction === 'down') {
      arrowYOffset = 0;
      m = 1;
  }
  var arrowPosX = ((this.size / 2) - arrowSize / 2);
  var arrowPosY = (this.size - this.size / 3) + arrowYOffset;
  var arrowDOffset =  m * (arrowSize / 1.5);
  var arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
  arrow.setAttribute('d', 'M 0 0 ' + arrowSize + ' 0 ' + arrowSize / 2 + ' ' + arrowDOffset + ' 0 0 Z');
  arrow.setAttribute('fill', '#FFF');
  arrow.setAttribute('opacity', '0.6');
  arrow.setAttribute('transform', 'translate(' + arrowPosX + ',' + arrowPosY + ')');
  this.svg.appendChild(arrow);
  this.arrow = arrow;
};

Dial1.prototype.animateStart = function() {
  var v = 0;
  var self = this;
  var intervalOne = setInterval(function() {
      var p = +(v / self.value).toFixed(2);
      var a = (p < 0.95) ? 2 - (2 * p) : 0.05;
      v += a;
      // Stop
      if(v >= +self.value) {
          v = self.value;
          clearInterval(intervalOne);
      }
      self.setValue(v);
  }, 10);
};

Dial1.prototype.animateReset = function() {
  this.setValue(0);
};

Dial1.prototype.polarToCartesian = function(centerX, centerY, radius, angleInDegrees) {
var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;
return {
  x: centerX + (radius * Math.cos(angleInRadians)),
  y: centerY + (radius * Math.sin(angleInRadians))
};
}

Dial1.prototype.describeArc = function(x, y, radius, startAngle, endAngle){
  var start = this.polarToCartesian(x, y, radius, endAngle);
  var end = this.polarToCartesian(x, y, radius, startAngle);
  var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  var d = [
      "M", start.x, start.y, 
      "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
  ].join(" ");
  return d;       
}

Dial1.prototype.setValue = function(value) {   
    var c = (value / 100) * 360;
    if(c === 360)
       c = 359.99;
    var xy = this.size / 2 - this.strokeWidth / 2;
    var d = this.describeArc(xy, xy, xy, 180, 180 + c);
  this.slice.setAttribute('d', d);
  var tspanSize = (this.size / 3.5) / 3;
  this.text.innerHTML = Math.floor(value) + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
};

//
// Usage
//

var containers = document.getElementsByClassName("donutchart1");
var dial = new Dial1(containers[0]);
dial.animateStart();




// ==========
// ring2

var Dial2 = function(ring2) {
  this.ring2 = ring2;
  this.size = this.ring2.dataset.size;
  this.strokeWidth = this.size / 8;
  this.radius = (this.size / 2) - (this.strokeWidth / 2);
  this.value = this.ring2.dataset.value;
  this.direction = this.ring2.dataset.arrow;
  this.svg;
  this.defs;
  this.slice;
  this.overlay;
  this.text;
  this.arrow;
  this.create();
}

Dial2.prototype.create = function() {
  this.createSvg();
  this.createDefs();
  this.createSlice();
  this.createOverlay();
  this.createText();
  this.createArrow();
  this.ring2.appendChild(this.svg);
};

Dial2.prototype.createSvg = function() {
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute('width', this.size + 'px');
  svg.setAttribute('height', this.size + 'px');
  this.svg = svg;
};

Dial2.prototype.createDefs = function() {
  var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  var linearGradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradient.setAttribute('id', 'gradient');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', '#6E4AE2');
  stop1.setAttribute('offset', '0%');
  linearGradient.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', '#78F8EC');
  stop2.setAttribute('offset', '100%');
  linearGradient.appendChild(stop2);
  var linearGradientBackground = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradientBackground.setAttribute('id', 'gradient-background');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', 'rgba(0, 0, 0, 0.2)');
  stop1.setAttribute('offset', '0%');
  linearGradientBackground.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', 'rgba(0, 0, 0, 0.05)');
  stop2.setAttribute('offset', '100%');
  linearGradientBackground.appendChild(stop2);
  defs.appendChild(linearGradient);
  defs.appendChild(linearGradientBackground);
  this.svg.appendChild(defs);
  this.defs = defs;
};

Dial2.prototype.createSlice = function() {
  var slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
  slice.setAttribute('fill', 'none');
  slice.setAttribute('stroke', 'url(#gradient)');
  slice.setAttribute('stroke-width', this.strokeWidth);
  slice.setAttribute('transform', 'translate(' + this.strokeWidth / 2 + ',' + this.strokeWidth / 2 + ')');
  slice.setAttribute('class', 'animate-draw');
  this.svg.appendChild(slice);
  this.slice = slice;
};

Dial2.prototype.createOverlay = function() {
  var r = this.size - (this.size / 2) - this.strokeWidth / 2;
  var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  circle.setAttribute('cx', this.size / 2);
  circle.setAttribute('cy', this.size / 2);
  circle.setAttribute('r', r);
  circle.setAttribute('fill', 'url(#gradient-background)');
  this.svg.appendChild(circle);
  this.overlay = circle;
};

Dial2.prototype.createText = function() {
  var fontSize = this.size / 3.5;
  var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute('x', (this.size / 2) + fontSize / 7.5);
  text.setAttribute('y', (this.size / 2) + fontSize / 4);
  text.setAttribute('font-family', 'Century Gothic, Lato');
  text.setAttribute('font-size', fontSize);
  text.setAttribute('fill', '#FFF');
  text.setAttribute('text-anchor', 'middle');
  var tspanSize = fontSize / 3;
  text.innerHTML = 0 + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
  this.svg.appendChild(text);
  this.text = text;
};

Dial2.prototype.createArrow = function() {
  var arrowSize = this.size / 10;
  var arrowYOffset, m;
  if(this.direction === 'up') {
      arrowYOffset = arrowSize / 2;
      m = -1;
  }
  else if(this.direction === 'down') {
      arrowYOffset = 0;
      m = 1;
  }
  var arrowPosX = ((this.size / 2) - arrowSize / 2);
  var arrowPosY = (this.size - this.size / 3) + arrowYOffset;
  var arrowDOffset =  m * (arrowSize / 1.5);
  var arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
  arrow.setAttribute('d', 'M 0 0 ' + arrowSize + ' 0 ' + arrowSize / 2 + ' ' + arrowDOffset + ' 0 0 Z');
  arrow.setAttribute('fill', '#FFF');
  arrow.setAttribute('opacity', '0.6');
  arrow.setAttribute('transform', 'translate(' + arrowPosX + ',' + arrowPosY + ')');
  this.svg.appendChild(arrow);
  this.arrow = arrow;
};

Dial2.prototype.animateStart = function() {
  var v = 0;
  var self = this;
  var intervalOne = setInterval(function() {
      var p = +(v / self.value).toFixed(2);
      var a = (p < 0.95) ? 2 - (2 * p) : 0.05;
      v += a;
      // Stop
      if(v >= +self.value) {
          v = self.value;
          clearInterval(intervalOne);
      }
      self.setValue(v);
  }, 10);
};

Dial2.prototype.animateReset = function() {
  this.setValue(0);
};

Dial2.prototype.polarToCartesian = function(centerX, centerY, radius, angleInDegrees) {
var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;
return {
  x: centerX + (radius * Math.cos(angleInRadians)),
  y: centerY + (radius * Math.sin(angleInRadians))
};
}

Dial2.prototype.describeArc = function(x, y, radius, startAngle, endAngle){
  var start = this.polarToCartesian(x, y, radius, endAngle);
  var end = this.polarToCartesian(x, y, radius, startAngle);
  var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  var d = [
      "M", start.x, start.y, 
      "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
  ].join(" ");
  return d;       
}

Dial2.prototype.setValue = function(value) {   
    var c = (value / 100) * 360;
    if(c === 360)
       c = 359.99;
    var xy = this.size / 2 - this.strokeWidth / 2;
    var d = this.describeArc(xy, xy, xy, 180, 180 + c);
  this.slice.setAttribute('d', d);
  var tspanSize = (this.size / 3.5) / 3;
  this.text.innerHTML = Math.floor(value) + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
};

//
// Usage
//

var containers = document.getElementsByClassName("donutchart2");
var dial = new Dial2(containers[0]);
dial.animateStart();

// ==========
// ring3

var Dial3 = function(ring3) {
  this.ring3 = ring3;
  this.size = this.ring3.dataset.size;
  this.strokeWidth = this.size / 8;
  this.radius = (this.size / 2) - (this.strokeWidth / 2);
  this.value = this.ring3.dataset.value;
  this.direction = this.ring3.dataset.arrow;
  this.svg;
  this.defs;
  this.slice;
  this.overlay;
  this.text;
  this.arrow;
  this.create();
}

Dial3.prototype.create = function() {
  this.createSvg();
  this.createDefs();
  this.createSlice();
  this.createOverlay();
  this.createText();
  this.createArrow();
  this.ring3.appendChild(this.svg);
};

Dial3.prototype.createSvg = function() {
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute('width', this.size + 'px');
  svg.setAttribute('height', this.size + 'px');
  this.svg = svg;
};

Dial3.prototype.createDefs = function() {
  var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  var linearGradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradient.setAttribute('id', 'gradient');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', '#6E4AE2');
  stop1.setAttribute('offset', '0%');
  linearGradient.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', '#78F8EC');
  stop2.setAttribute('offset', '100%');
  linearGradient.appendChild(stop2);
  var linearGradientBackground = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradientBackground.setAttribute('id', 'gradient-background');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', 'rgba(0, 0, 0, 0.2)');
  stop1.setAttribute('offset', '0%');
  linearGradientBackground.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', 'rgba(0, 0, 0, 0.05)');
  stop2.setAttribute('offset', '100%');
  linearGradientBackground.appendChild(stop2);
  defs.appendChild(linearGradient);
  defs.appendChild(linearGradientBackground);
  this.svg.appendChild(defs);
  this.defs = defs;
};

Dial3.prototype.createSlice = function() {
  var slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
  slice.setAttribute('fill', 'none');
  slice.setAttribute('stroke', 'url(#gradient)');
  slice.setAttribute('stroke-width', this.strokeWidth);
  slice.setAttribute('transform', 'translate(' + this.strokeWidth / 2 + ',' + this.strokeWidth / 2 + ')');
  slice.setAttribute('class', 'animate-draw');
  this.svg.appendChild(slice);
  this.slice = slice;
};

Dial3.prototype.createOverlay = function() {
  var r = this.size - (this.size / 2) - this.strokeWidth / 2;
  var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  circle.setAttribute('cx', this.size / 2);
  circle.setAttribute('cy', this.size / 2);
  circle.setAttribute('r', r);
  circle.setAttribute('fill', 'url(#gradient-background)');
  this.svg.appendChild(circle);
  this.overlay = circle;
};

Dial3.prototype.createText = function() {
  var fontSize = this.size / 3.5;
  var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute('x', (this.size / 2) + fontSize / 7.5);
  text.setAttribute('y', (this.size / 2) + fontSize / 4);
  text.setAttribute('font-family', 'Century Gothic, Lato');
  text.setAttribute('font-size', fontSize);
  text.setAttribute('fill', '#FFF');
  text.setAttribute('text-anchor', 'middle');
  var tspanSize = fontSize / 3;
  text.innerHTML = 0 + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
  this.svg.appendChild(text);
  this.text = text;
};

Dial3.prototype.createArrow = function() {
  var arrowSize = this.size / 10;
  var arrowYOffset, m;
  if(this.direction === 'up') {
      arrowYOffset = arrowSize / 2;
      m = -1;
  }
  else if(this.direction === 'down') {
      arrowYOffset = 0;
      m = 1;
  }
  var arrowPosX = ((this.size / 2) - arrowSize / 2);
  var arrowPosY = (this.size - this.size / 3) + arrowYOffset;
  var arrowDOffset =  m * (arrowSize / 1.5);
  var arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
  arrow.setAttribute('d', 'M 0 0 ' + arrowSize + ' 0 ' + arrowSize / 2 + ' ' + arrowDOffset + ' 0 0 Z');
  arrow.setAttribute('fill', '#FFF');
  arrow.setAttribute('opacity', '0.6');
  arrow.setAttribute('transform', 'translate(' + arrowPosX + ',' + arrowPosY + ')');
  this.svg.appendChild(arrow);
  this.arrow = arrow;
};

Dial3.prototype.animateStart = function() {
  var v = 0;
  var self = this;
  var intervalOne = setInterval(function() {
      var p = +(v / self.value).toFixed(2);
      var a = (p < 0.95) ? 2 - (2 * p) : 0.05;
      v += a;
      // Stop
      if(v >= +self.value) {
          v = self.value;
          clearInterval(intervalOne);
      }
      self.setValue(v);
  }, 10);
};

Dial3.prototype.animateReset = function() {
  this.setValue(0);
};

Dial3.prototype.polarToCartesian = function(centerX, centerY, radius, angleInDegrees) {
var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;
return {
  x: centerX + (radius * Math.cos(angleInRadians)),
  y: centerY + (radius * Math.sin(angleInRadians))
};
}

Dial3.prototype.describeArc = function(x, y, radius, startAngle, endAngle){
  var start = this.polarToCartesian(x, y, radius, endAngle);
  var end = this.polarToCartesian(x, y, radius, startAngle);
  var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  var d = [
      "M", start.x, start.y, 
      "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
  ].join(" ");
  return d;       
}

Dial3.prototype.setValue = function(value) {   
    var c = (value / 100) * 360;
    if(c === 360)
       c = 359.99;
    var xy = this.size / 2 - this.strokeWidth / 2;
    var d = this.describeArc(xy, xy, xy, 180, 180 + c);
  this.slice.setAttribute('d', d);
  var tspanSize = (this.size / 3.5) / 3;
  this.text.innerHTML = Math.floor(value) + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
};

//
// Usage
//

var containers = document.getElementsByClassName("donutchart3");
var dial = new Dial3(containers[0]);
dial.animateStart();


// ==========
// ring4

var Dial4 = function(ring4) {
  this.ring4 = ring4;
  this.size = this.ring4.dataset.size;
  this.strokeWidth = this.size / 8;
  this.radius = (this.size / 2) - (this.strokeWidth / 2);
  this.value = this.ring4.dataset.value;
  this.direction = this.ring4.dataset.arrow;
  this.svg;
  this.defs;
  this.slice;
  this.overlay;
  this.text;
  this.arrow;
  this.create();
}

Dial4.prototype.create = function() {
  this.createSvg();
  this.createDefs();
  this.createSlice();
  this.createOverlay();
  this.createText();
  this.createArrow();
  this.ring4.appendChild(this.svg);
};

Dial4.prototype.createSvg = function() {
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute('width', this.size + 'px');
  svg.setAttribute('height', this.size + 'px');
  this.svg = svg;
};

Dial4.prototype.createDefs = function() {
  var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  var linearGradient = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradient.setAttribute('id', 'gradient');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', '#6E4AE2');
  stop1.setAttribute('offset', '0%');
  linearGradient.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', '#78F8EC');
  stop2.setAttribute('offset', '100%');
  linearGradient.appendChild(stop2);
  var linearGradientBackground = document.createElementNS("http://www.w3.org/2000/svg", "linearGradient");
  linearGradientBackground.setAttribute('id', 'gradient-background');
  var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute('stop-color', 'rgba(0, 0, 0, 0.2)');
  stop1.setAttribute('offset', '0%');
  linearGradientBackground.appendChild(stop1);
  var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute('stop-color', 'rgba(0, 0, 0, 0.05)');
  stop2.setAttribute('offset', '100%');
  linearGradientBackground.appendChild(stop2);
  defs.appendChild(linearGradient);
  defs.appendChild(linearGradientBackground);
  this.svg.appendChild(defs);
  this.defs = defs;
};

Dial4.prototype.createSlice = function() {
  var slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
  slice.setAttribute('fill', 'none');
  slice.setAttribute('stroke', 'url(#gradient)');
  slice.setAttribute('stroke-width', this.strokeWidth);
  slice.setAttribute('transform', 'translate(' + this.strokeWidth / 2 + ',' + this.strokeWidth / 2 + ')');
  slice.setAttribute('class', 'animate-draw');
  this.svg.appendChild(slice);
  this.slice = slice;
};

Dial4.prototype.createOverlay = function() {
  var r = this.size - (this.size / 2) - this.strokeWidth / 2;
  var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  circle.setAttribute('cx', this.size / 2);
  circle.setAttribute('cy', this.size / 2);
  circle.setAttribute('r', r);
  circle.setAttribute('fill', 'url(#gradient-background)');
  this.svg.appendChild(circle);
  this.overlay = circle;
};

Dial4.prototype.createText = function() {
  var fontSize = this.size / 3.5;
  var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute('x', (this.size / 2) + fontSize / 7.5);
  text.setAttribute('y', (this.size / 2) + fontSize / 4);
  text.setAttribute('font-family', 'Century Gothic, Lato');
  text.setAttribute('font-size', fontSize);
  text.setAttribute('fill', '#FFF');
  text.setAttribute('text-anchor', 'middle');
  var tspanSize = fontSize / 3;
  text.innerHTML = 0 + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
  this.svg.appendChild(text);
  this.text = text;
};

Dial4.prototype.createArrow = function() {
  var arrowSize = this.size / 10;
  var arrowYOffset, m;
  if(this.direction === 'up') {
      arrowYOffset = arrowSize / 2;
      m = -1;
  }
  else if(this.direction === 'down') {
      arrowYOffset = 0;
      m = 1;
  }
  var arrowPosX = ((this.size / 2) - arrowSize / 2);
  var arrowPosY = (this.size - this.size / 3) + arrowYOffset;
  var arrowDOffset =  m * (arrowSize / 1.5);
  var arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
  arrow.setAttribute('d', 'M 0 0 ' + arrowSize + ' 0 ' + arrowSize / 2 + ' ' + arrowDOffset + ' 0 0 Z');
  arrow.setAttribute('fill', '#FFF');
  arrow.setAttribute('opacity', '0.6');
  arrow.setAttribute('transform', 'translate(' + arrowPosX + ',' + arrowPosY + ')');
  this.svg.appendChild(arrow);
  this.arrow = arrow;
};

Dial4.prototype.animateStart = function() {
  var v = 0;
  var self = this;
  var intervalOne = setInterval(function() {
      var p = +(v / self.value).toFixed(2);
      var a = (p < 0.95) ? 2 - (2 * p) : 0.05;
      v += a;
      // Stop
      if(v >= +self.value) {
          v = self.value;
          clearInterval(intervalOne);
      }
      self.setValue(v);
  }, 10);
};

Dial4.prototype.animateReset = function() {
  this.setValue(0);
};

Dial4.prototype.polarToCartesian = function(centerX, centerY, radius, angleInDegrees) {
var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;
return {
  x: centerX + (radius * Math.cos(angleInRadians)),
  y: centerY + (radius * Math.sin(angleInRadians))
};
}

Dial4.prototype.describeArc = function(x, y, radius, startAngle, endAngle){
  var start = this.polarToCartesian(x, y, radius, endAngle);
  var end = this.polarToCartesian(x, y, radius, startAngle);
  var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  var d = [
      "M", start.x, start.y, 
      "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y
  ].join(" ");
  return d;       
}

Dial4.prototype.setValue = function(value) {   
    var c = (value / 100) * 360;
    if(c === 360)
       c = 359.99;
    var xy = this.size / 2 - this.strokeWidth / 2;
    var d = this.describeArc(xy, xy, xy, 180, 180 + c);
  this.slice.setAttribute('d', d);
  var tspanSize = (this.size / 3.5) / 3;
  this.text.innerHTML = Math.floor(value) + '<tspan font-size="' + tspanSize + '" dy="' + -tspanSize * 1.2 + '">%</tspan>';
};

//
// Usage
//

var containers = document.getElementsByClassName("donutchart4");
var dial = new Dial4(containers[0]);
dial.animateStart();



// 전체 가입자수 js
$('.count').each(function () {
    $(this).prop('Counter',0).animate({
        Counter: $(this).text()
    }, {
        duration: 1500,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
    });
});



// 성비 파이그래프
function sliceSize(dataNum, dataTotal) {
  return (dataNum / dataTotal) * 360;
}
function addSlice(sliceSize, pieElement, offset, sliceID, color) {
  $(pieElement).append("<div class='slice "+sliceID+"'><span></span></div>");
  var offset = offset - 1;
  var sizeRotation = -179 + sliceSize;
  $("."+sliceID).css({
    "transform": "rotate("+offset+"deg) translate3d(0,0,0)"
  });
  $("."+sliceID+" span").css({
    "transform"       : "rotate("+sizeRotation+"deg) translate3d(0,0,0)",
    "background-color": color
  });
}
function iterateSlices(sliceSize, pieElement, offset, dataCount, sliceCount, color) {
  var sliceID = "s"+dataCount+"-"+sliceCount;
  var maxSize = 179;
  if(sliceSize<=maxSize) {
    addSlice(sliceSize, pieElement, offset, sliceID, color);
  } else {
    addSlice(maxSize, pieElement, offset, sliceID, color);
    iterateSlices(sliceSize-maxSize, pieElement, offset+maxSize, dataCount, sliceCount+1, color);
  }
}
function createPie(dataElement, pieElement) {
  var listData = [];
  $(dataElement+" span").each(function() {
    listData.push(Number($(this).html()));
  });
  var listTotal = 0;
  for(var i=0; i<listData.length; i++) {
    listTotal += listData[i];
  }
  var offset = 0;
  var color = [
    "cornflowerblue", 
    "olivedrab", 
    "orange", 
    "tomato", 
    "crimson", 
    "purple", 
    "turquoise", 
    "forestgreen", 
    "navy", 
    "gray"
  ];
  for(var i=0; i<listData.length; i++) {
    var size = sliceSize(listData[i], listTotal);
    iterateSlices(size, pieElement, offset, i, 0, color[i]);
    $(dataElement+" li:nth-child("+(i+1)+")").css("border-color", color[i]);
    offset += size;
  }
}
createPie(".pieID.legend", ".pieID.pie");
