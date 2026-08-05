describe('web-storage-proxy', () => {
  beforeEach(() => {
    window.sessionStorage.clear();
    window.localStorage.clear();
  });

  it('has jsdom', () => {
    console.log(window.constructor.name);
    console.log(window.location.href);
  });

  it('has storage', () => {
    expect(window.sessionStorage).toBeDefined();
    expect(window.localStorage).toBeDefined();
  });
});
