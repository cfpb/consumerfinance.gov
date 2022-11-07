const dispatch = jest.fn();
const subscribe = jest.fn();
const getState = jest.fn();
let subscriberFn;
let state = {};

/**
 * @returns {object} The mocked store object.
 */
function mockStore() {
  return {
    subscriber() {
      return subscriberFn;
    },
    getState: getState.mockImplementation(() => state),
    dispatch,
    mockState(newState) {
      state = newState;
    },
    subscribe: subscribe.mockImplementation((fn) => {
      subscriberFn = fn;
    }),
    mockReset() {
      dispatch.mockReset();
      subscribe.mockClear();
      subscriberFn = null;
      state = {};
    },
  };
}

export default mockStore;
