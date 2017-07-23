'use strict';

var gradedInput = require( './inputs/input-graded' );
var notesInput = require( './inputs/input-notes' );
var editorTemplate =
  require( '../../templates/prepare-worksheets/worksheet-graded-editor.hbs' );
var notesEditorTemplate =
  require( '../../templates/prepare-worksheets/worksheet-notes-editor.hbs' );

var _self = this;

var grades = {
  goals: [ 'High', 'Med', 'Low' ],
  risks: [ 'Yes', 'Maybe', 'No' ]
};

this.errorMessages = {
  goals: {
    emptyInputs: {
      heading:   'You haven’t entered any goals.',
      paragraph: "To get the best results, please go back and <a href='#page1'>enter at least one goal</a>."
    },
    noGrade: {
      heading:   'You haven’t prioritized any goals.',
      paragraph: "To get the best results, please go back and <a href='#page1'>prioritize at least one goal</a>."
    }
  },
  flags: {
    noGrade: {
      heading:   'You haven’t indicated whether there are any red flags in your situation.',
      paragraph: "To get the best results, please go back and <a href='#page1flags'>assess the red flags</a>."
    }
  },
  risks: {
    noGrade: {
      heading:   'You haven’t indicated whether you are ready to accept the risks associated with homeownership.',
      paragraph: "To get the best results, please go back and <a href='#page1risks'>assess the risks</a>."
    }
  }
};

this.gradeSummaryLabels = {
  goals: [ 'High Priority', 'Medium Priority', 'Low Priority' ],
  flags: [ 'Likely to happen', 'Somewhat likely to happen', 'Not likely to happen' ],
  risks: [ 'Ready to accept', 'Somewhat ready to accept', 'Not ready to accept' ]
};

this.getWorksheetRowDefaults = function() {
  return {
    text:        '',
    grade:       null,
    altText:     '',
    alternative: '',
    explanation: ''
  };
};

this.worksheetData = {
  personal: function() {
    return {
      title:         'Personal Goal',
      prompt:        'Priority Level',
      placeholder:   'Write your own goal',
      grades:        grades.goals,
      errorMessages: _self.errorMessages.goals
    };
  },
  financial: function() {
    return {
      title:         'Financial Goal',
      prompt:        'Priority Level',
      placeholder:   'Write your own goal',
      grades:        grades.goals,
      errorMessages: _self.errorMessages.goals
    };
  },
  alternatives: function() {
    return {
      title:       'Goal',
      prompt:      'How else can I achieve this goal?',
      placeholder: 'Write an alternative to this goal'
    };
  },
  risks: function() {
    return {
      title:         'Issue',
      prompt:        'Are you ready to accept this risk?',
      placeholder:   'Identify your own risk',
      grades:        grades.risks,
      errorMessages: _self.errorMessages.risks
    };
  },
  flags: function() {
    return {
      title:         'Issue',
      prompt:        'Is this likely?',
      placeholder:   'Identify your own flag',
      grades:        grades.risks,
      errorMessages: _self.errorMessages.flags
    };
  }
};

this.worksheetModules = {
  personal: function() {
    return {
      inputType:         'graded',
      worksheetTemplate: editorTemplate,
      InputModule:       gradedInput
    };
  },
  financial: function() {
    return {
      inputType:         'graded',
      worksheetTemplate: editorTemplate,
      InputModule:       gradedInput
    };
  },
  alternatives: function() {
    return {
      inputType:         'notes',
      worksheetTemplate: notesEditorTemplate,
      InputModule:       notesInput
    };
  },
  risks: function() {
    return {
      inputType:         'graded',
      worksheetTemplate: editorTemplate,
      InputModule:       gradedInput
    };
  },
  flags: function() {
    return {
      inputType:         'graded',
      worksheetTemplate: editorTemplate,
      InputModule:       gradedInput
    };
  }
};

this.worksheetDefaults = {
  personal: function() {
    return [
      {
        text:        'I want more space (e.g., for a growing family).',
        grade:       null,
        alternative: 'I could move to a larger rental unit instead.',
        explanation: ''
      },
      {
        text:        'I want certain features (e.g., a yard).',
        grade:       null,
        alternative: 'I could find these features in a rental unit in my community.',
        explanation: ''
      },
      {
        text:        'I want to live in a particular area (e.g., a certain school district).',
        grade:       null,
        alternative: 'There are rental units available in my desired location.',
        explanation: ''
      },
      {
        text:        'I want the freedom to decorate or renovate.',
        grade:       null,
        alternative: 'There are things I could do to make my rental feel more like my own.',
        explanation: ''
      }
    ];
  },

  financial: function() {
    return [
      {
        text:        'I want to build wealth in the form of equity',
        grade:       null,
        alternative: '',
        altText:     '',
        explanation: '<strong>Learn more:</strong> In the long term, owning a home can be a great way to build wealth.  However, it’s important to know that during the first several years of a mortgage, <a href=#>most of your payment goes to interest, not equity</a>.  Also, remember that if home prices go down instead of up – as they did in 2008-2012 – you could lose all of your equity, including your down payment.'
      },
      {
        text:        'I believe I can buy a nicer home for the same cost as my rent',
        grade:       null,
        alternative: '',
        altText:     '',
        explanation: '<strong>Learn more:</strong> This is often true.  However, it’s important to factor in the total costs of ownership – including insurance, taxes, maintenance, and discretionary improvements – as well as increases in other costs, such as commuting, that may result from buying.  And depending on the real estate market, sometimes renting can actually be cheaper.'
      },
      {
        text:         'I want to save money on my taxes with the mortgage deduction',
        grade:        null,
        alternative:  '',
        altText:      '',
        explanation:  '<strong>Learn more:</strong> You can only claim the mortgage interest tax deduction if you itemize your deductions.  For a typical $200,000 mortgage at 4.5%, you’d be able to deduct about $8900 for interest in the first year, and less in future years.  The standard deduction for a married couple is $12,600 in tax year 2015, so unless that couple has at least $4700 in other deductions, having a mortgage won’t lower their taxes.  For heads of household, the standard deduction is $9,250, and for singles it is $6,300.'
      }
    ];
  },

  flags: function() {
    return [
      {
        text:        'There is a chance I might move within the next few years',
        grade:       null,
        alternative: 'Renters have more flexibility. It can be risky and expensive to buy if you end up needing to move again within a few years.',
        altText:     '',
        explanation: '',
        required:    true
      },
      {
        text:        'My current employment is short-term or unstable',
        grade:       null,
        alternative: 'Owning a home is a long-term financial commitment. If you’re not confident that you’ll be able to continue earning at a similar level for the foreseeable future, it might make more sense to keep renting.',
        altText:     '',
        explanation: '',
        required:    true
      },
      {
        text:        'I will have little to no savings left over after making a down payment',
        grade:       null,
        alternative: '',
        altText:     '',
        explanation: '',
        required:    true
      },
      {
        text:        'I find fixing things and doing yardwork to be a real hassle',
        grade:       null,
        alternative: 'In a lot of ways, it’s simpler and more financially predictable to rent.',
        altText:     '',
        explanation: '',
        required:    true
      }
    ];
  },

  risks: function() {
    return [
      {
        text:        'My home value could decline and I could lose my equity',
        grade:       null,
        alternative: 'You could even find yourself owing more than your home is worth. In 2008-2012, house prices declined dramatically nationwide, with up to X% declines in some areas.',
        altText:     '',
        explanation: '',
        required:    true
      },
      {
        text:        'Major repairs can be urgent, expensive, and unexpected',
        grade:       null,
        alternative: 'When the furnace springs a leak or a tree falls on the roof, these aren’t repairs that you can wait to make. New homeowners consistently say that they were surprised how much maintenance costs.',
        altText:     '',
        explanation: '',
        required:    true
      },
      {
        text:        'Minor repairs add up quickly, in terms of time and money',
        grade:       null,
        alternative: 'Think of all the little things that you are used to calling your landlord to deal with: a cracked window, a broken dishwasher, or a clogged toilet. As a homeowner, you will either have to fix these yourself or call and pay for a professional.',
        altText:     '',
        explanation: '',
        required:    true
      }
    ];
  }
};

this.getAllWorksheetDefaults = function() {
  var data = _self.worksheetDefaults;
  var obj = {};
  for ( var key in data ) {
    if ( data.hasOwnProperty( key ) ) {
      obj[key] = data[key]();
    }
  }
  return obj;
};
