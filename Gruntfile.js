module.exports = function(grunt) {

  'use strict';

  require( 'time-grunt' )( grunt );
  require( 'jit-grunt' )( grunt, {
    // Static mappings below;
    // needed because task name does not match package name.
    bower: 'grunt-bower-task',
    usebanner: 'grunt-banner'
  } );

  var path = require('path');

  // Allows a `--quiet` flag to be passed to Grunt from the command-line.
  // If the flag is present the value is true, otherwise it is false.
  // This flag can be used to, for example, suppress warning output
  // from linters.
  var env = {
    quiet: grunt.option('quiet') ? true : false
  };

  var config = {

    /**
     * Pull in the package.json file so we can read its metadata.
     */
    pkg: grunt.file.readJSON('bower.json'),

    /**
     * Set directory location variables.
     */
    loc: {
      src:  './src',
      dist: '.',
      lib:  grunt.file.readJSON('./.bowerrc').directory,
      test: './_tests'
    },

    /**
     * Bower: https://github.com/yatskevich/grunt-bower-task
     *
     * Migrate static assets to distribution directory.
     */
    bower: {
      process: {
        options: {
          targetDir: '<%= loc.lib %>',
          install: false,
          cleanTargetDir: false,
          // The `exportsOverride` section in `bower.json` is used to map
          // bower package components to types (js, css, less, img, fonts),
          // which can then be moved in the `layout` function below.
          //
          // TODO: Switch to maintained grunt bower task.
          // There is a bug in the `grunt-bower-task` which means
          // certain packages have to appear in the `exportsOverride`
          // section, even though they are only being copied in place.
          // This has occurred with the `history.js`,
          // and `string_score` packages. The consequence of this is that
          // they are listed in `bower.json` and in the `browser` field
          // in `package.json` when it shouldn't be necessary to list them
          // in both places.
          // Unfortunately, the `grunt-bower-task` is not being maintained
          // as of May, 2015, so this likely will not be fixed soon.
          // See background in issue:
          // https://github.com/yatskevich/grunt-bower-task/issues/159
          layout: function( type, component, source ) {
            var lib = config.loc.lib;
            var dist = config.loc.dist + '/static/';
            var assetPath = component;
            if ( ( type === 'img' || type === 'fonts' ) ||
                 ( type === 'js' && component === 'box-sizing-polyfill' ) ||
                 ( type === 'css' && component === 'slick-carousel' ) ||
                 ( type === 'js' && component === 'html5shiv') ) {
              assetPath = path.relative( lib , dist + type );
              grunt.log.writeln('Moving ./' + source + ' to ' + dist + type);
            }
            return assetPath;
          }
        }
      }
    },

    /**
     * String replace: https://github.com/erickrdch/grunt-string-replace
     *
     * Replace strings on files by using string or regex patters.
     */
    // TODO: Prefix replacement URLs with <%= loc.dist %> when `/dist`
    // directory exists.
    'string-replace': {
      chosen: {
        files: {
          '<%= loc.lib %>/chosen/': '<%= loc.lib %>/chosen/chosen.css'
        },
        options: {
          replacements: [{
            pattern: /url\('chosen-sprite.png'\)/ig,
            replacement: 'url("/static/img/chosen-sprite.png")'
          },
          {
            pattern: /url\('chosen-sprite@2x.png'\)/ig,
            replacement: 'url("/static/img/chosen-sprite@2x.png")'
          }]
        }
      },
      'slick-carousel': {
        files: {
          '<%= loc.dist %>/static/css/': '<%= loc.dist %>/static/css/slick.css'
        },
        options: {
          replacements: [{
            pattern: /url\(".\/ajax-loader.gif"\)/ig,
            replacement: 'url("/static/img/ajax-loader.gif")'
          }]
        }
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
          '<%= loc.lib %>/cf-*/*.less',
          '!<%= loc.lib %>/cf-core/*.less',
          '<%= loc.lib %>/cf-core/cf-core.less'
        ],
        dest: '<%= loc.lib %>/capital-framework/capital-framework.less',
        nonull: true
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
          // Specifies directories to scan for @import directives when parsing.
          // Additional paths can be passed to the array in `concat()`.
          paths: function( source ) {
            grunt.log.writeln( 'Processing ' + source );
            return grunt.file.expand( config.loc.lib + '/*' ).concat([])
          },
          compress: true,
          sourceMap: true,
          // Where the sourcemap file is generated and located.
          sourceMapFilename: '<%= loc.dist %>/static/css/main.css.map',
          // The complete URL and sourcemap filename put in the compiled CSS file.
          sourceMapURL: 'main.css.map',
        },
        files: {
          '<%= loc.dist %>/static/css/main.css': ['static/css/main.less']
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
      main: {
        // Prefix `static/css/main.css` and overwrite.
        expand: true,
        src: ['<%= loc.dist %>/static/css/main.css']
      },
    },

    /**
     * Browserify: https://github.com/jmreidy/grunt-browserify
     *
     * CommonJS JavaScript module manager.
     * Shared modules are in `common.js`, while page-specific
     * modules are in scripts that mirror the name of the
     * URL location path, but ending in `index.js`.
     */
    browserify: {
      build: {
        src: '<%= loc.src %>/static/js/routes/**/*.js',
        dest: '<%= loc.dist %>/static/js/routes/common.min.js'
      },
      options: {
        // Note: The transforms for minification and
        // the entire `browserify-shim` config is inside `package.json`.
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
      ' *               ad$$               $$\n' +
      ' *              d$"                 $$\n' +
      ' *              $$                  $$\n' +
      ' *   ,adPYba.   $$$$$  $$.,dPYba.   $$.,dPYba.\n' +
      ' *  aP′    `$:  $$     $$P′    `$a  $$P′    `$a\n' +
      ' *  $(          $$     $$(      )$  $$(      )$\n' +
      ' *  "b.    ,$:  $$     $$b.    ,$"  $$b.    ,$"\n' +
      ' *   `"Ybd$"′   $$     $$`"YbdP"′   $$`"YbdP"′\n' +
      ' *                     $$\n' +
      ' *                     $$\n' +
      ' *                     $$\n' +
      ' *\n' +
      ' *  <%= pkg.name %> - v<%= pkg.version %>\n' +
      ' *  <%= pkg.homepage %>\n' +
      ' *  A public domain work of the Consumer Financial Protection Bureau\n' +
      ' */',

    usebanner: {
      css: {
        options: {
          position: 'top',
          banner: '<%= banner %>',
          linebreak: true
        },
        files: {
          src: ['<%= loc.dist %>/static/css/*.min.css']
        }
      },
      js: {
        options: {
          position: 'top',
          banner: '<%= banner %>',
          linebreak: true
        },
        files: {
          src: ['<%= loc.dist %>/static/js/**/*.min.js']
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
          // All media queries over 960 will be excluded from the stylesheet.
          // EM calculation: 960 / 16 = 60
          legacyWidth: 60
        },
        files: {
          '<%= loc.dist %>/static/css/main.ie.css': '<%= loc.dist %>/static/css/main.css'
        }
      }
    },

    /**
     * Lint the JavaScript.
     */
    lintjs: {
      /**
       * Validate files with ESLint.
       * https://www.npmjs.com/package/grunt-contrib-eslint
       */
      eslint: {
        options: {
            quiet: env.quiet
        },
        src: [
            '<%= loc.src %>/static/js/**/*.js',
            '<%= loc.test %>/unit_tests/*.js'
        ]
      }
    },

    /**
     * Mocha_istanbul: Run mocha tests and spit out code coverage
     */
    mocha_istanbul: {
      coverage: {
        src: ['<%= loc.test %>/unit_tests/**/*.js'],
        options: {
          coverageFolder: '<%= loc.test %>/unit_test_coverage',
          excludes: ['<%= loc.test %>/unit_tests/**/*.js']
        }
      }
    },

    /**
     * Watch: https://github.com/gruntjs/grunt-contrib-watch
     *
     * Run predefined tasks whenever watched file patterns are added, changed or deleted.
     * Add files to monitor below.
     */
    watch: {
      all: {
        files: ['static/css/*.less', '<%= loc.src %>/static/js/**/*.js', 'Gruntfile.js'],
        tasks: ['default']
      },
      cssjs: {
        files: ['static/css/*.less', '<%= loc.src %>/static/js/**/*.js'],
        tasks: ['css', 'js']
      },
      css: {
        files: ['static/css/*.less'],
        tasks: ['css']
      },
      js: {
        files: ['<%= loc.src %>/static/js/**/*.js'],
        tasks: ['js']
      }
    },

    /**
     * See note below about creating a dynamic Topdoc options object.
     */
    topdoc_families: [
      'blog-docs',
      'calendar-icon',
      'cf-enhancements',
      'event-docs',
      'event-meta',
      'forms',
      'header',
      'lists',
      'media',
      'meta',
      'misc',
      'nav-secondary',
      'post',
      'print',
      'summary'
    ]
  };

  /**
   * Creates a dynamic Topdoc options object.
   * To add more subtasks add an item to the config.topdoc_families array.
   * For example if you created a new component with the family name of
   * "my-component" then you could add a new item to the config.topdoc_families
   * array called "my-component" and this function would automatically add a new
   * Topdoc subtask to the Topdoc task. You could then run `grunt topdoc:my-component`
   * to build it out separately or just `grunt topdoc` to run all topdoc tasks.
   */
  function dynamicTopdocTasks() {
    var topdoc = {},
        families = config.topdoc_families;
    for (var i = 0; i < families.length; i++) {
      var key = families[i];
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

  // TODO: `grunt topdoc` task is currently unused, the idea is docs would
  // be deployed to the gh-pages branch only. However, this is not currently
  // set up. The task used will be `concurrent:topdoc`, which is set up below.
  config.topdoc = dynamicTopdocTasks();

  /**
   * Create an array of all of the Topdoc subtasks.
   * This is useful for the concurrent task which needs to know all of the
   * tasks you want to run concurrently. Since these Topdics are dynamically
   * created we need a way to also dynamically update the concurrent task options.
   */
  function getTopdocSubtasks() {
    var families = config.topdoc_families,
        subtasks = [];
    for (var i = 0; i < families.length; i++) {
      subtasks.push( 'topdoc:' + families[i] );
    }
    return subtasks;
  }

  config.concurrent = {
    topdoc: getTopdocSubtasks()
  };

  /**
   * Initialize a configuration object for the current project.
   */
  grunt.initConfig(config);

  /**
   * Create custom task aliases and combinations.
   */
  grunt.registerTask('vendor', ['bower:process', 'string-replace:chosen',
                                'string-replace:slick-carousel', 'concat:cf-less']);
  grunt.registerTask('css', ['less', 'autoprefixer', 'legacssy', 'usebanner:css']);
  grunt.registerTask('js', ['browserify:build', 'usebanner:js']);
  grunt.registerTask('test', ['lintjs', 'mocha_istanbul']);
  grunt.registerMultiTask('lintjs', 'Lint the JavaScript', function(){
    grunt.config.set(this.target, this.data);
    grunt.task.run(this.target);
  });
  grunt.registerTask('build', ['test', 'css', 'js']);
  grunt.registerTask('default', ['build']);
};
