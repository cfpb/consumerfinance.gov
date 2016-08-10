
/**
 * A custom object to help with our analytics dom selectors
 * 
 * - makes it a little easier and less error-prone to add or remove selectors in a list
 * - builds tedious selectors like: 'a[href]:not(.js-videoreplace,a[href^="tel:"])'
 * 
 * Usage notes
 * 
 * var bodyTargets = new AnalyticsTarget({
 *     containers: [ '.wrapper-body' ],
 *     targets: [ 'a[href]' ],
 *     exceptions: [
 *         'a[lang="es"]',
 *         'a[href^="tel:"]'
 *     ]
 * });
 * 
 * bodyTargets.selectContainers();
 * // returns: '.wrapper-body'
 * 
 * bodyTargets.selectTargets();
 * // returns: 'a[href]'
 * 
 * bodyTargets.selectTargetsForDelegate();
 * // returns: 'a[href]:not(a[lang="es"],a[href^="tel:"])'
 * 
 * @todo use try/catch and create custom errors
 * 
 */

function AnalyticsTarget( t ) {

    this.containers = t.containers || [];
    this.targets = t.targets || [];
    this.exceptions = t.exceptions || [];

}

AnalyticsTarget.prototype.selectContainers = function() {
    return this.containers.join(',');
};

AnalyticsTarget.prototype.selectTargets = function() {
    return this.targets.join(',');
};

AnalyticsTarget.prototype.selectTargetsForDelegate = function() {

    /**
     * Create a selector for this.targets for use in a jquery delegate()
     * function. This mainly means that this.container is not used because it
     * is called separately in the delegate function. This also means that
     * we can't use the not() function and should instead us the :not()
     * selector string.
     */

    var targetsWithExceptions = [],
        totalTargets = this.targets.length,
        i;
    for ( i = 0; i < totalTargets; i++ ) {
        targetsWithExceptions .push( this.targets[i] + ':not(' + this.exceptions.join(',') + ')' );
    }
    return targetsWithExceptions.join(',');
};
