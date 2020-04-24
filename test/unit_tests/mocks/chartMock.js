const chartMock = {};

const props = [
  'renderer',
  'g',
  'translate',
  'add',
  'path',
  'label',
  'attr',
  'rect',
  'addClass',
  'text'
];

for ( let i = 0; i < props.length; i++ ) {
  const propName = props[i];
  chartMock[propName] = jest.fn( () => chartMock );
}

export default chartMock;
