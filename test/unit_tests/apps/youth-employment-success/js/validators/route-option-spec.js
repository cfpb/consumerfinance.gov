import
validate
  from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/validators/route-option';

describe( '.validate', () => {
  const data = {
    earned: '1',
    spent: '1',
    averageCost: '1',
    isMonthlyCost: true,
    transitTimeMinutes: '1',
    transitTimeHours: '1',
    transportation: 'Walk',
    actionPlanItems: []
  };

  it( 'validates data to true if all required fields are present', () => {
    expect( validate( data ) ).toBeTruthy();
  } );

  it( 'validates undefined data', () => {
    let UNDEFINED;
    expect( validate( {
      ...data,
      earned: UNDEFINED
    } ) ).toBeFalsy();
  } );

  it( 'validates data to false if not all required fields are present', () => {
    expect( validate( {} ) ).toBeFalsy();
    expect( validate( {
      earned: 1,
      spent: '',
      actionPlanItems: []
    } ) ).toBeFalsy();
  } );

  it( 'validates data to true if value is ' +
      'not present and action plan item exists', () => {
    expect(
      validate( {
        ...data,
        transitTimeHours: '',
        transitTimeMinutes: '',
        actionPlanItems: [ 'TIME' ]
      } )
    ).toBeTruthy();
  } );

  it( 'validates driving data correctly', () => {
    const driveData = {
      earned: 1,
      spent: 1,
      transitTimeMinutes: 1,
      transitTimeHours: 1,
      transportation: 'Drive',
      miles: 1,
      daysPerWeek: 1,
      actionPlanItems: []
    };

    expect( validate( driveData ) ).toBeTruthy();
    expect( validate( {
      ...driveData,
      miles: ''
    } ) ).toBeFalsy();
    expect( validate( {
      ...driveData,
      daysPerWeek: ''
    } ) ).toBeFalsy();
  } );

  it( 'validates non-driving data correctly', () => {
    expect( validate( {
      ...data,
      averageCost: ''
    } ) ).toBeFalsy();

    expect( validate( {
      ...data,
      averageCost: '',
      isMonthlyCost: null
    } ) ).toBeFalsy();

    expect( validate( {
      ...data,
      isMonthlyCost: null
    } ) ).toBeFalsy();

    expect( validate( {
      ...data,
      isMonthlyCost: false,
      daysPerWeek: ''
    } ) ).toBeFalsy();
  } );
} );
