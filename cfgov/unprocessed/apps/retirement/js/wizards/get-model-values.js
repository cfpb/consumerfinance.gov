import benefitsModel from '../models/benefits-model.js';
import lifetimeModel from '../models/lifetime-model.js';

const getModel = {
  benefits: () => benefitsModel.values,
  lifetime: () => lifetimeModel.values,
};

export default getModel;
