'use strict';

// TODO: Move this into cfgov-refresh's utils to encourage reuse
class Store {
  constructor( mid = [] ) {
    this.subscribers = [];
    this.middlewares = mid;
    if ( this.middlewares.length > 0 ) {
      this.dispatch = this._combineMiddlewares();
    }
  }
}

Store.prototype._combineMiddlewares = function() {
  var self = this;
  var dispatch = this.dispatch;
  var middlewareAPI = {
    getState: this.getState.bind( this ),
    dispatch: function( action ) {
      return dispatch.call( self, action );
    }
  };

  // Inject store "proxy" into all middleware
  var chain = this.middlewares.map( function( middleware ) {
    return middleware( middlewareAPI );
  } );

  // Init reduceRight with middlewareAPI.dispatch as initial value
  dispatch = chain.reduceRight( function( composed, fn ) {
    return fn( composed );
  }, dispatch.bind( this ) );

  return dispatch;
};

Store.prototype.getState = function() {
  return this.state;
};

Store.prototype.dispatch = function( action ) {
  this.prevState = this.state;
  this.state = this.reduce( this.state, action );
  this.notifySubscribers();
  return action;
};

Store.prototype.subscribe = function( fn ) {
  this.subscribers.push( fn );
};

Store.prototype.notifySubscribers = function() {
  this.subscribers.forEach( function( subscriber ) {
    subscriber( this.prevState, this.state );
  }.bind( this ) );
};

module.exports = Store;
