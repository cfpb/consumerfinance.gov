class SectionLink {
  /**
   * @param {HTMLButtonElement} root Section link button
   */
  constructor( root ) {
    this.root = root;
  }

  markPreviousPage() {
    this.root.setAttribute( 'data-color', 'green' );
    this.markEditable();
    this.markDone();
  }

  /**
   * @param {boolean} done Is this section done?
   */
  markCurrentPage( done ) {
    this.root.setAttribute( 'data-color', 'blue' );
    if ( done ) {
      this.setStatus( 'complete' );
      this.markDone();
    } else {
      this.setStatus( 'in progress' );
    }
  }

  /**
   * @param {boolean} done Is this section done?
   * @param {boolean} visited Has this section begun?
   */
  markUpcomingPage( done, visited ) {
    if ( done ) {
      this.root.setAttribute( 'data-color', 'green' );
      this.markDone();
    } else if ( visited ) {
      this.root.setAttribute( 'data-color', 'white' );
      this.setStatus( 'in progress' );
    }
  }

  markDone() {
    this.root.setAttribute( 'data-checked', '1' );
    this.setStatus( 'complete' );
  }

  markEditable() {
    this.root.setAttribute( 'data-editable', '1' );
    this.root.tabIndex = 0;
    this.root.addEventListener( 'click', event => {
      event.preventDefault();
      location.href = this.root.dataset.href;
    } );
  }

  /**
   * @param {string} status Section status
   */
  setStatus( status ) {
    const el = this.root.querySelector( '.tdp-survey-section__status' );
    if ( el ) {
      el.textContent = `(${ status })`;
    }
  }

  /**
   * @param {number} from First question number
   * @param {number} to Last question number
   */
  setRange( from, to ) {
    const el = this.root.querySelector( '.tdp-survey-section__range' );
    if ( el ) {
      el.textContent = `Questions ${ from }–${ to }`;
    }
  }
}

/**
 * @type {number}
 */
let checkThreshold = 0;

/**
 * @type {SectionLink | null}
 */
let current = null;

/**
 * @param {SurveyData} data Survey data
 */
SectionLink.init = function( { numAnswered, pageIdx, questionsByPage } ) {
  let questionsFound = 0;
  const roots = document.querySelectorAll( '.tdp-survey-section' );

  [].forEach.call( roots, ( root, idx ) => {
    const questionsHere = questionsByPage[idx];
    const visited = numAnswered >= questionsFound;
    const done = numAnswered >= ( questionsFound + questionsHere );

    const sl = new SectionLink( root );
    sl.setRange( questionsFound + 1, questionsFound + questionsHere );

    if ( idx < pageIdx ) {
      sl.markPreviousPage();
    } else if ( pageIdx === idx ) {
      // Set up for marking done later
      current = sl;
      checkThreshold = questionsFound + questionsHere;

      sl.markCurrentPage( done );
    } else {
      sl.markUpcomingPage( done, visited );
    }

    questionsFound += questionsHere;
  } );
};

/**
 * Update the current SectionLink
 *
 * @param {number} numAnswered Num answered questions
 */
SectionLink.update = function( numAnswered ) {
  if ( current && numAnswered >= checkThreshold ) {
    current.markDone();
  }
};

module.exports = SectionLink;
