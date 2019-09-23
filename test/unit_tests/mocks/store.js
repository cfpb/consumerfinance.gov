const dispatch = jest.fn();
const subscribe = jest.fn();
let subscriberFn;

function mockStore() {
  return {
    subscriber() {
      return subscriberFn;
    },
    dispatch,
    subscribe: subscribe.mockImplementation( fn => {
      subscriberFn = fn;
    } ),
    mockReset() {
      dispatch.mockReset();
      subscribe.mockReset();
      subscriberFn = null;
    }
  };
}

export default mockStore;
