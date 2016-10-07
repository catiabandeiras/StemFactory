"use strict";
/* panel_navigation.js - Handles panel tabs */

var PanelNavigation = function(app){
    this.app = app;

    this.activeClass = 'active';
    this.activeElement = null;

    this.initNavigation();
};


PanelNavigation.prototype.initNavigation = function()
{
    this.panelNavs = document.querySelectorAll('.panel-tabs-container > li > a');
    this.panelNavSelected(this.panelNavs[0]);
    for (var p = 0, l = this.panelNavs.length; p < l; p++)
    {
        var panelNavAnchor = this.panelNavs[p];
        console.log('panel tab', panelNavAnchor);
        this.app.attachTouchEvent(panelNavAnchor, this.panelNavSelected.bind(this, panelNavAnchor));
    }
}

PanelNavigation.prototype.panelNavSelected = function(panelNavAnchor)
{
    var tab, panel;

    console.log("panelNavSelected", panelNavAnchor)
    try {
        // reset styles
        if (this.activeElement)
        {
            tab = this.activeElement;/*.parentNode;*/
            this.panelFromTab(tab).style.display = 'none';
            this.app.styler.removeClass(tab, this.activeClass);
        }

        //set style on selected tab and panel
        tab = panelNavAnchor.parentNode;
        this.panelFromTab(tab).style.display = 'block';
        this.app.styler.addClass(tab, this.activeClass);

        this.activeElement = tab;
    } catch (e) { console.error(e); }
}

PanelNavigation.prototype.panelFromTab = function(tab)
{
    if (!tab) throw Error("Invalid Tab");

    var panelId = tab.getAttribute('data-target-panel');
    var panel = document.getElementById(panelId);
    if (!panel) throw Error("Invalid Panel " + panelId);

    return panel;
}
