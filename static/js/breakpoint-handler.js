var modernBrowser = 'innerWidth' in window,
    viewportEl = modernBrowser ? window : (document.documentElement || document.body),
    propPrefix = modernBrowser ? 'inner' : 'client';
    
function getViewportDimensions() {
    return {width: viewportEl[propPrefix + 'Width'], height: viewportEl[propPrefix + 'Height']};
}


/**
 * @name BreakpointHandler
 *
 * @description On window resize, checks viewport
 * width against a specified breakpoint value or range, 
 * and calls `enter` or `leave` callback if breakpoint
 * region has just been entered or exited.
 *
 * @params {object} opts options object. Takes form:
 * {
 *  breakpoint: number (600) or range [600, 1023],
 *  type: range, max, or min (type of media query to emulate),
 *  enter: callback when breakpoint region entered,
 *  leave: callback when breakpoint region exited
 * }
 * 
 */

BreakpointHandler = function (opts) {
    opts || (opts = {});
    this.match = false;
    this.breakpoint = opts.breakpoint;
    this.enter = opts.enter;
    this.leave = opts.leave;
    this.type = opts.type || 'max';
    this.init();
};

BreakpointHandler.prototype.init = function () {
    this.handleViewportChange();
    this.watchWindowResize();
};

BreakpointHandler.prototype.watchWindowResize = function () {
    var self = this;
    $(window).bind("resize", function () {
        self.handleViewportChange();
    });
};

BreakpointHandler.prototype.handleViewportChange = function () {
    var width = viewportEl[propPrefix + 'Width'],
        match = this.testBreakpoint(width);
    if (match !== this.match) {
        if (match) {
            this.enter && this.enter();
        } else {
            this.leave && this.leave();
        }
    }
    this.match = match;
};

BreakpointHandler.prototype.testBreakpoint = function (width) {
    switch (this.type) {
        case 'max':
            return width <= this.breakpoint;
            break;
        case 'min':
            return width >= this.breakpoint;
            break;
        case 'range':
            return width >= this.breakpoint[0] && width <= this.breakpoint[1];
            break;
        default:
            return;
    }
};

/**
 * @name MobileOnlyExpandable
 *
 * @description Hides content in an expandable for mobile screens.
 * When viewport size drops below specified max-width breakpoint, 
 * visible expandable content is hidden.
 * When breakpoint is exceeded, expandable content is shown.
 * (Expandable trigger is currently hidden/shown via media query.)
 *
 * @params {object} elem jQuery `expandable` element
 * @params {number} breakpoint mobile max-width value
 * 
 * 
 */

function MobileOnlyExpandable(elem, breakpoint) {
    this.expandable = elem;
    this.expandableTarget = this.expandable.children('.expandable_target');
    this.breakpoint = breakpoint;
    this.init();
};

MobileOnlyExpandable.prototype.init = function () {
    // Make sure we have necessary elements before proceeding.
    if (this.expandable instanceof jQuery && this.expandableTarget instanceof jQuery) {
        this.breakpointHandler = new BreakpointHandler({
            breakpoint: this.breakpoint,
            type: "max",
            enter: $.proxy(this.closeExpandable, this),
            leave: $.proxy(this.openExpandable, this)
        });
    }
};

MobileOnlyExpandable.prototype.closeExpandable = function () {
    // Click to close expandable if it is open.
    // TODO: alternative to click event.
    var isExpanded = this.expandable.hasClass('expandable__expanded');
    if (isExpanded) {
        this.expandableTarget.click();
    }
};

MobileOnlyExpandable.prototype.openExpandable = function () {
    // Click to open expandable if it is closed.
    // TODO: alternative to click event.
    var isExpanded = this.expandable.hasClass('expandable__expanded');
    if (!isExpanded) {
        this.expandableTarget.click();
    }
};