import ExternalSite from '../../../../cfgov/unprocessed/js/modules/ExternalSite';

const HTML_SNIPPET = `
<main class="content external-site_container">
    <div class="wrapper content_wrapper">
        <div class="content_main ">
            <section class="padded-container">

                <h1>Thank you for visiting consumerfinance.gov.</h1>
                <p class="lead-paragraph">
                    You are leaving the CFPB web server.
                    You will now access
                    <span class="external-site_text"></span>,<br>
                    which may have different privacy policies.
                    We hope your visit was informative and enjoyable.
                </p>
                <p class="lead-paragraph u-js-only">
                    We’ll take you to the page in:
                    <span class="external-site_reload-container"></span>
                </p>
                <form method="POST" action="/external-site/" id="proceed">
                <input type="button" class="a-btn
                          a-btn__full-on-xs
                          external-site_proceed-btn" value="Proceed to external site">
                <input id="id_ext_url" name="ext_url" type="hidden">
                <input id="id_signature" name="signature" type="hidden">
                </form>

            </section>
        </div>
    </div>
</main>
`;

describe( 'ExternalSite', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'should initialize and count down', () => {
    const dom = document.querySelector( '.external-site_container' );
    const externalSite = new ExternalSite( dom );
    externalSite.init();
    expect( dom.querySelectorAll( '.external-site_reload-duration' ).length )
      .toBe( 0 );

    setTimeout( () => {
      expect( dom.querySelectorAll( '.external-site_reload-duration' ).length )
        .toBe( 1 );
    }, 1500 );
  } );
} );
