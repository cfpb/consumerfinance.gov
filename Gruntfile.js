module.exports = function(grunt) {

  'use strict';

  var path = require('path');

  var config = {

    /**
     * Pull in the package.json file so we can read its metadata.
     */
    pkg: grunt.file.readJSON('bower.json'),
    
    /**
     * Bower: https://github.com/yatskevich/grunt-bower-task
     * 
     * Install Bower packages and migrate static assets.
     */
    bower: {
      install: {
        options: {
          targetDir: './vendor/',
          install: true,
          verbose: true,
          cleanBowerDir: true,
          cleanTargetDir: true,
          layout: function(type, component) {
            if (type === 'img') {
              return path.join('../static/img');
            } else if (type === 'fonts') {
              return path.join('../static/fonts');
            } else {
              return path.join(component);
            }
          }
        }
      }
    },

    /**
     * String replace: https://github.com/erickrdch/grunt-string-replace
     * 
     * Replace strings on files by using string or regex patters.
     */
    'string-replace': {
      chosen: {
        files: {
          'vendor/chosen/': 'vendor/chosen/chosen.css'
        }
      },
      options: {
        replacements: [{
          pattern: /url\('chosen-sprite.png'\)/ig,
          replacement: 'url("../img/chosen-sprite.png")'
        },
        {
          pattern: /url\('chosen-sprite@2x.png'\)/ig,
          replacement: 'url("../img/chosen-sprite@2x.png")'
        }]
      }
    },

    /**
     * Concat: https://github.com/gruntjs/grunt-contrib-concat
     * 
     * Concatenate cf-* Less files prior to compiling them.
     */
    concat: {
      'cf-less': {
        src: [
          'vendor/cf-*/*.less'
        ],
        dest: 'vendor/cf-concat/cf.less',
      },
      bodyScripts: {
        src: [
          'vendor/jquery/jquery.js',
          'vendor/chosen/chosen.jquery.js',
          'vendor/cf-*/*.js',
          'static/js/jquery.custom-input.js',
          'static/js/app.js'
        ],
        dest: 'static/js/main.js'
      }
    },

    /**
     * Less: https://github.com/gruntjs/grunt-contrib-less
     * 
     * Compile Less files to CSS.
     */
    less: {
      main: {
        options: {
          paths: grunt.file.expand('vendor/**/'),
        },
        files: {
          'static/css/main.css': ['static/css/main.less']
        }
      }
    },

    /**
     * Autoprefixer: https://github.com/nDmitry/grunt-autoprefixer
     * 
     * Parse CSS and add vendor-prefixed CSS properties using the Can I Use database.
     */
    autoprefixer: {
      options: {
        // Options we might want to enable in the future.
        diff: false,
        map: false
      },
      multiple_files: {
        // Prefix all CSS files found in `static/css` and overwrite.
        expand: true,
        src: ['static/css/*.css', '!static/css/*.min.css']
      },
    },

    /**
     * Uglify: https://github.com/gruntjs/grunt-contrib-uglify
     * 
     * Minify JS files.
     * Make sure to add any other JS libraries/files you'll be using.
     * You can exclude files with the ! pattern.
     */
    uglify: {
      options: {
        preserveComments: 'some'
      },
      // headScripts: {
      //   src: 'vendor/html5shiv/html5shiv-printshiv.js',
      //   dest: 'static/js/html5shiv-printshiv.js'
      // },
      bodyScripts: {
        src: ['static/js/main.js'],
        dest: 'static/js/main.min.js'
      }
    },

    /**
     * Banner: https://github.com/mattstyles/grunt-banner
     *
     * Here's a banner with some template variables.
     * We'll be inserting it at the top of minified assets.
     */
    banner: 
      '/*!\n' +
      ' *              ad$$             $$\n' +
      ' *             d$"               $$\n' +
      ' *             $$                $$\n' +
      ' *   ,adPYba,  $$$$$ $b,dPYba,   $$,dPYba,\n' +
      ' *  aP\'    \'$: $$    $$P\'   \'$a  $$P\'   \'$a\n' +
      ' *  $(         $$    $$(     )$  $$(     )$\n' +
      ' *  "b,    ,$: $$    $$b,   ,$"  $$b,   ,$"\n' +
      ' *   `"Ybd$"\'  $$    $$`YbdP"\'   $$`Ybd$"\'\n' +
      ' *                   $$\n' +
      ' *                   $$\n' +
      ' *                   ""\n' +
      ' *\n' +
      ' *  <%= pkg.name %> - v<%= pkg.version %>\n' +
      ' *  <%= pkg.homepage %>' +
      ' *  A public domain work of the Consumer Financial Protection Bureau\n' +
      ' */',

    usebanner: {
      taskName: {
        options: {
          position: 'top',
          banner: '<%= banner %>',
          linebreak: true
        },
        files: {
          src: [ 'static/css/*.min.css', 'static/js/*.min.js' ]
        }
      }
    },

    /**
     * CSS Min: https://github.com/gruntjs/grunt-contrib-cssmin
     *
     * Compress CSS files.
     */
    cssmin: {
      main: {
        options: {
          processImport: false
        },
        files: {
          'static/css/main.min.css': ['static/css/main.css'],
        }
      },
      'ie-alternate': {
        options: {
          processImport: false
        },
        files: {
          'static/css/main.ie.min.css': ['static/css/main.ie.css'],
        }
      }
    },

    /**
     * Legacssy: https://github.com/robinpokorny/grunt-legacssy
     *
     * Fix your CSS for legacy browsers.
     */
    legacssy: {
      'ie-alternate': {
        options: {
          // Flatten all media queries with a min-width over 960 or lower.
          // All media queries over 960 will be excluded fromt he stylesheet.
          // EM calculation: 960 / 16 = 60
          legacyWidth: 60
        },
        files: {
          'static/css/main.ie.css': 'static/css/main.css'
        }
      }
    },

    /**
     * Copy: https://github.com/gruntjs/grunt-contrib-copy
     * 
     * Copy files and folders.
     */
    copy: {
      vendor: {
        files:
        [
          {
            expand: true,
            cwd: '',
            src: [
              // Only include vendor files that we use independently
              'vendor/html5shiv/html5shiv-printshiv.min.js',
              'vendor/box-sizing-polyfill/boxsizing.htc'
            ],
            dest: 'static'
          }
        ]
      }
    },

    /**
     * JSHint: https://github.com/gruntjs/grunt-contrib-jshint
     * 
     * Validate files with JSHint.
     * Below are options that conform to idiomatic.js standards.
     * Feel free to add/remove your favorites: http://www.jshint.com/docs/#options
     */
    jshint: {
      options: {
        camelcase: false,
        curly: true,
        forin: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        quotmark: true,
        sub: true,
        boss: true,
        strict: true,
        evil: true,
        eqnull: true,
        browser: true,
        plusplus: false,
        globals: {
          jQuery: true,
          $: true,
          module: true,
          require: true,
          define: true,
          console: true,
          EventEmitter: true
        }
      },
      all: ['static/js/main.js']
    },

    /**
     * Watch: https://github.com/gruntjs/grunt-contrib-watch
     * 
     * Run predefined tasks whenever watched file patterns are added, changed or deleted.
     * Add files to monitor below.
     */
    watch: {
      gruntfile: {
        files: ['Gruntfile.js', 'static/css/*.less', '<%= uglify.bodyScripts.src %>'],
        tasks: ['default']
      },
      css: {
        files: ['static/css/*.less'],
        tasks: ['cssdev', 'topdoc']
      }
    }
  };

  /*
   * Creates a dynamic topdoc options object.
   * To add more subtasks add an item to the subtasks array.
   * For example if you created a new component with the family name of
   * "my-component" then you could add a new item to the subtasks array called
   * "my-component" and this function would automatically add a new topdoc
   * subtask to the topdoc task. You could then run `grunt topdoc:my-component`
   * to build it out separately or just `grunt topdoc` to run all topdoc tasks.
   */
  function dynamicTopdocTasks() {
    var topdoc = {};
    var subtasks = [
      'blog-docs',
      'media-object',
      'meta',
      'misc',
      'post',
      'summary',
      'utilities'
    ];
    for (var i = 0; i < subtasks.length; i++) {
      var key = subtasks[i];
      topdoc[key] = {
        options: {
          source: 'static/css/',
          destination: 'docs/' + key + '/',
          template: 'node_modules/cf-component-demo/docs/',
          templateData: {
            family: 'cfgov-' + key,
            description: key + ' for cfgov-refresh.',
            title: 'cfgov-refresh / ' + key + ' docs',
            repo: '<%= pkg.homepage %>'
          }
        }
      };
    }
    return topdoc;
  }

  config.topdoc = dynamicTopdocTasks();

  grunt.initConfig(config);

  /**
   * The above tasks are loaded here.
   */
  grunt.loadNpmTasks('grunt-autoprefixer');
  grunt.loadNpmTasks('grunt-banner');
  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-legacssy');
  grunt.loadNpmTasks('grunt-string-replace');
  grunt.loadNpmTasks('grunt-topdoc');

  /**
   * Create custom task aliases and combinations
   */
  grunt.registerTask('vendor', ['bower:install', 'string-replace:chosen', 'concat:cf-less']);
  grunt.registerTask('cssdev', ['less', 'autoprefixer', 'legacssy', 'cssmin']);
  grunt.registerTask('jsdev', ['concat:bodyScripts', 'uglify', 'usebanner']);
  grunt.registerTask('default', ['cssdev', 'jsdev', 'copy:vendor', 'topdoc']);
  grunt.registerTask('test', ['jshint']);

};
