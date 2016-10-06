"use strict";

var Styler = function(){};


Styler.prototype.hasClass = function(element, className)
{
    if (!element || typeof element.className == 'undefined') return null;
    return element.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
};

Styler.prototype.addClass = function(element, className)
{
    if (!element || typeof element.className == 'undefined') return null;
    if (!this.hasClass(element, className)) element.className += " " + className;
};

Styler.prototype.removeClass = function(element, className)
{
    if (!element || typeof element.className == 'undefined') return null;
    if (this.hasClass(element, className))
    {
        var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
        element.className = element.className.replace(reg, ' ').trim();
    }
};
