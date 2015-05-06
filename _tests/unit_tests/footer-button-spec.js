var chai = require('chai');
var expect = chai.expect;
var jsdom = require('mocha-jsdom');

describe('Footer Button Testing', function() {
    'use strict';

    var $, footerButton;

    jsdom();

    before(function (){
        $ = require('jquery');
        footerButton = require('../../src/static/js/modules/footer-button.js');
    });

    beforeEach(function(){
    });

  it('is a test', function(){
    expect(footerButton).to.be.ok;
  });
});