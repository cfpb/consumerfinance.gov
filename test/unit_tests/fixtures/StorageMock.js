'use strict';


function StorageMock() {
  this.storage = {};
}

function setItem( _key, value ) {
  this.storage[_key] = value.toString() || '';
}

function getItem( _key ) {
  return this.storage[_key];
}

function removeItem( _key ) {
  delete this.storage[_key];
}

function length() {
  return Object.keys( this.storage ).length;
}

function key( index ) {
  var keys = Object.keys( this.storage );
  return keys[index] || null;
}

StorageMock.prototype.setItem = setItem;
StorageMock.prototype.getItem = getItem;
StorageMock.prototype.removeItem = removeItem;
StorageMock.prototype.length = length;
StorageMock.prototype.key = key;

module.exports = StorageMock;
