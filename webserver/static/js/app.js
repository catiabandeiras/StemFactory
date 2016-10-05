"use strict";
/* app.js - main application scripting */

var App = function(){
    this.b_isTouchTerminal = null;

    this.styler = new Styler();
    this.panelNav = new PanelNavigation(this);
};


App.prototype.isTouchTerminal = function()
{
    if (null === this.b_isTouchTerminal)
    {
        if (!!('ontouchstart' in document.documentElement))
            this.b_isTouchTerminal = true;
        else
            this.b_isTouchTerminal = false;
    }
    return this.b_isTouchTerminal;
};


App.prototype.attachTouchEvent = function(element, action)
{
    var elem, eventName;

    if (typeof element == 'object')
        elem = element;
    else
        elem = document.getElementById(element);

    if (!elem) return console.error("Couldn't find element " + element);

    if (this.isTouchTerminal())
    {
        eventName = 'touchend';//start';
    }
    else
        eventName = 'click';

    elem.addEventListener(eventName, action);
};


var app = new App();

