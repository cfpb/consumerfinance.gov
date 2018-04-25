let open;
let send;
let onload;
let onerror;

/**
 * Mock XMLHttpRequest requests so that the calls can be tested.
 * Adopted from https://stackoverflow.com/questions/28584773/xhr-testing-in-jest
 * @return {Function} Return a
 */
function createXHRMock() {
    open = jest.fn();

    /* Note: use *function* because we need to get *this*
       from *new XmlHttpRequest()* call. */
    send = jest.fn().mockImplementation( function() {
      onload = this.onload.bind( this );
      onerror = this.onerror.bind( this );
    } );

    const xhrMockClass = () => {
      return {
        open: this.open,
        send: this.send
      };
    };

    window.XMLHttpRequest = jest.fn().mockImplementation( xhrMockClass );

    this.open = open;
    this.send = send;
    this.onload = onload;
    this.onerror = onerror;
    return this;
}

module.exports = createXHRMock;
