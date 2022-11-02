import Store from './store';

const updateGeo = (geo, action) => {
  switch (action.type) {
    case 'CLEAR_GEO':
      return {
        type: null,
        id: null,
        name: null,
      };
    case 'UPDATE_CHART':
      return {
        type: action.geo.type || geo.type,
        id: action.geo.id,
        name: action.geo.name,
      };
    case 'ZOOM_CHART':
      return {
        type: geo.type,
        id: '',
        name: '',
      };
    default:
      return geo;
  }
};

const updateDate = (date, action) => {
  switch (action.type) {
    case 'UPDATE_DATE':
      return action.date;
    default:
      return date;
  }
};

const isLoadingMetros = (action) => {
  switch (action.type) {
    case 'REQUEST_METROS':
      return true;
    default:
      return false;
  }
};

const isLoadingCounties = (action) => {
  switch (action.type) {
    case 'REQUEST_COUNTIES':
      return true;
    default:
      return false;
  }
};

const isLoading = (action) => {
  switch (action.type) {
    case 'REQUEST_DATA':
      return action.isLoading;
    default:
      return false;
  }
};

const updateZoomTarget = (prevTarget, action) => {
  switch (action.type) {
    case 'ZOOM_CHART':
      return action.target;
    default:
      return null;
  }
};

const updateMetros = (metros, action) => {
  switch (action.type) {
    case 'SET_METROS':
      return action.metros;
    case 'UPDATE_CHART':
      return action.metros || metros;
    case 'FETCH_METROS':
    case 'REQUEST_METROS':
    default:
      return metros;
  }
};

const updateCounties = (counties, action) => {
  switch (action.type) {
    case 'SET_COUNTIES':
      return action.counties;
    case 'UPDATE_CHART':
      return action.counties || counties;
    case 'FETCH_COUNTIES':
    case 'REQUEST_COUNTIES':
    default:
      return counties;
  }
};

const initialState = {
  geo: {
    type: 'state',
    id: null,
    name: null,
  },
  date: '2008-01',
  counties: [],
  metros: [],
  isLoadingCounties: false,
  isLoadingChart: false,
};

class MapStore extends Store {
  constructor({ date, middleware }) {
    super(middleware);
    this.prevState = {};
    this.state = initialState;
    this.state.date = date;
    this.state = this.reduce(this.state, {});
  }

  reduce(state, action) {
    const newState = {
      geo: updateGeo(state.geo, action),
      date: updateDate(state.date, action),
      isLoadingMetros: isLoadingMetros(action),
      isLoadingCounties: isLoadingCounties(action),
      isLoading: isLoading(action),
      zoomTarget: updateZoomTarget(state.zoomTarget, action),
      counties: updateCounties(state.counties, action),
      metros: updateMetros(state.metros, action),
    };
    return newState;
  }
}

export default MapStore;
