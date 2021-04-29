/**
 * Constructs a search query to append to a link to College Scorecard that looks
 * for schools that offer a given program near a given ZIP.
 * @param {string} pcip The given program's two-digit PCIP code
 * @param {string} zip A five-digit ZIP code to search near
 * @param {string} radius Radius in miles to search around the given ZIP
 * @returns {string} The search query (or false if PCIP and ZIP are missing)
 */
function constructScorecardSearch( pcip, zip, radius ) {
  const searchParameters = [];
  // Use a 50-mile radius, the most common Scorecard search, as a default
  const searchRadius = radius || '50';
  const pcipData = {
    '01': {
      label:  'Agriculture, Agriculture Operations, and Related Sciences',
      urlKey: 'agriculture'
    },
    '03': {
      label:  'Natural Resources and Conservation',
      urlKey: 'resources'
    },
    '04': {
      label:  'Architecture and Related Services',
      urlKey: 'architecture'
    },
    '05': {
      label:  'Area, Ethnic, Cultural, Gender, and Group Studies',
      urlKey: 'ethnic_cultural_gender'
    },
    '09': {
      label:  'Communication, Journalism, and Related Programs',
      urlKey: 'communication'
    },
    '10': {
      label:
    'Communications Technologies/Technicians and Support Services',
      urlKey: 'communications_technology'
    },
    '11': {
      label:  'Computer and Information Sciences and Support Services',
      urlKey: 'computer'
    },
    '12': {
      label:  'Personal and Culinary Services',
      urlKey: 'personal_culinary'
    },
    '13': {
      label:  'Education',
      urlKey: 'education'
    },
    '14': {
      label:  'Engineering',
      urlKey: 'engineering'
    },
    '15': {
      label:  'Engineering Technologies and Engineering-Related Fields',
      urlKey: 'engineering_technology'
    },
    '16': {
      label:  'Foreign Languages, Literatures, and Linguistics',
      urlKey: 'language'
    },
    '19': {
      label:  'Family and Consumer Sciences/Human Sciences',
      urlKey: 'family_consumer_science'
    },
    '22': {
      label:  'Legal Professions and Studies',
      urlKey: 'legal'
    },
    '23': {
      label:  'English Language and Literature/Letters',
      urlKey: 'english'
    },
    '24': {
      label:  'Liberal Arts and Sciences, General Studies and Humanities',
      urlKey: 'humanities'
    },
    '25': {
      label:  'Library Science',
      urlKey: 'library'
    },
    '26': {
      label:  'Biological and Biomedical Sciences',
      urlKey: 'biological'
    },
    '27': {
      label:  'Mathematics and Statistics',
      urlKey: 'mathematics'
    },
    '29': {
      label:  'Military Technologies and Applied Sciences',
      urlKey: 'military'
    },
    '30': {
      label:  'Multi/Interdisciplinary Studies',
      urlKey: 'multidiscipline'
    },
    '31': {
      label:  'Parks, Recreation, Leisure, and Fitness Studies',
      urlKey: 'parks_recreation_fitness'
    },
    '38': {
      label:  'Philosophy and Religious Studies',
      urlKey: 'philosophy_religious'
    },
    '39': {
      label:  'Theology and Religious Vocations',
      urlKey: 'theology_religious_vocation'
    },
    '40': {
      label:  'Physical Sciences',
      urlKey: 'physical_science'
    },
    '41': {
      label:  'Science Technologies/Technicians',
      urlKey: 'science_technology'
    },
    '42': {
      label:  'Psychology',
      urlKey: 'psychology'
    },
    '43': {
      label:  'Homeland Security, Law Enforcement, Firefighting and Related Protective Services',
      urlKey: 'security_law_enforcement'
    },
    '44': {
      label:  'Public Administration and Social Service Professions',
      urlKey: 'public_administration_social_service'
    },
    '45': {
      label:  'Social Sciences',
      urlKey: 'social_science'
    },
    '46': {
      label:  'Construction Trades',
      urlKey: 'construction'
    },
    '47': {
      label:  'Mechanic and Repair Technologies/Technicians',
      urlKey: 'mechanic_repair_technology'
    },
    '48': {
      label:  'Precision Production',
      urlKey: 'precision_production'
    },
    '49': {
      label:  'Transportation and Materials Moving',
      urlKey: 'transportation'
    },
    '50': {
      label:  'Visual and Performing Arts',
      urlKey: 'visual_performing'
    },
    '51': {
      label:  'Health Professions and Related Programs',
      urlKey: 'health'
    },
    '52': {
      label:
    'Business, Management, Marketing, and Related Support Services',
      urlKey: 'business_marketing'
    },
    '54': {
      label:  'History',
      urlKey: 'history'
    }
  };
  if ( !pcip && !zip ) {
    return false;
  }
  if ( pcipData[pcip] ) {
    searchParameters.push( 'major=' + pcipData[pcip].urlKey );
  }
  if ( zip ) {
    searchParameters.push( 'zip=' + zip );
    searchParameters.push( 'distance=' + searchRadius );
  }
  return 'search/?' + searchParameters.join( '&' );
}

module.exports = constructScorecardSearch;
