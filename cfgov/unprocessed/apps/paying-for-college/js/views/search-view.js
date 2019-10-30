import { schoolSearch } from '../dispatchers/get-api-values';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const searchView = {
	searchSection: null,
	searchBox: null,
	searchResults: null,
	keyupDelay: null,

	formatSearchResults: function( responseText ) {
		const obj = JSON.parse( responseText );
		let html;
		for ( let key in obj ) {
			html += '\n<option value="' + obj[key]['id'] + '">' + obj[key]['schoolname'] + '</option>';
			console.log( html );
		}
	},

	handleInputChange: function( event ) {
		clearTimeout( this.keyupDelay );
		this.keyupDelay = setTimeout( function() {
			const searchTerm = searchView.searchBox.value;
			// TODO - clean up searchbox text, remove non-alphanumeric characters
			schoolSearch( searchTerm )
				.then( ( resp ) => {
					searchView.formatSearchResults( resp.responseText );
				} );
		}, 500 );
	},

	_addKeyListener: function() {
		const events = {
			keyup: this.handleInputChange,
			focusout: this.handleInputChange
		}
		bindEvent( this.searchBox, events );
	},

	init: function( body ) {
		this.searchSection = body.querySelector( '#college-costs__school-search' );
		this.searchBox = body.querySelector( '#search__school-name' );
		this.searchResults = body.querySelector( '#tmp__search-results' );
		this._addKeyListener();
	}

};

export {
	searchView
};