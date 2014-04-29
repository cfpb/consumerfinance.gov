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
          'vendor/cf-*/*.js',
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
      },
      ie8: {
        options: {
          banner: '<%= banner.cfpb %>',
          paths: ['static'],
        },
        files: {
          'static/css/ie8.css': ['static/css/ie/ie8.less']
        }
      }
    },

    /**
     * String Replace: https://github.com/erickrdch/grunt-string-replace
     * 
     * Rewrite CSS asset paths.
     */
    'string-replace': {
      vendor: {
        files: {
          'static/css/': ['static/css/main.css']
        },
        options: {
          replacements: [
            {
              pattern: 'url(/cf-grid/custom-demo/static/css/boxsizing.htc);',
              replacement: 'url(/cfgov-refresh/static/vendor/box-sizing-polyfill/boxsizing.htc);'
            },
            {
              pattern: /url\((.*?)\)/ig,
              replacement: function (match, p1, offset, string) {
                var path, pathParts, pathLength, filename, newPath;
                path = p1.replace(/["']/g,''); // Removes quotation marks if there are any
                pathParts = path.split('/'); // Splits the path so we can find the filename
                pathLength = pathParts.length;
                filename = pathParts[pathLength-1]; // The filename is the last item in pathParts

                // Rewrite the path based on the file type
                // Note that .svg can be a font or a graphic, not sure what to do about this.
                if (filename.indexOf('.eot') !== -1 ||
                    filename.indexOf('.woff') !== -1 ||
                    filename.indexOf('.ttf') !== -1 ||
                    filename.indexOf('.svg') !== -1)
                {
                  newPath = 'url("../fonts/'+filename+'")';
                  grunt.verbose.ok('Replaced:',match,'\n    with:',newPath);
                  grunt.verbose.writeln('');
                  return newPath;
                } else if (filename.indexOf('.png') !== -1 ||
                    filename.indexOf('.gif') !== -1 ||
                    filename.indexOf('.jpg') !== -1)
                {
                  newPath = 'url("../img/'+filename+'")';
                  grunt.verbose.ok('Replaced:',match,'\n    with:',newPath);
                  grunt.verbose.writeln('');
                  return newPath;
                } else {
                  grunt.verbose.warn('No filetype matches for:',match,'\n');
                  grunt.verbose.writeln('');
                  return match;
                }
              }
            }
          ]
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
        src: 'static/css/*.css'
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
     * Minify CSS and optionally rewrite asset paths.
     */
    cssmin: {
      combine: {
        options: {
          processImport: false
        },
        files: {
          'static/css/main.min.css': ['static/css/main.css'],
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
     * grunt-cfpb-internal: https://github.com/cfpb/grunt-cfpb-internal
     * 
     * Some internal CFPB tasks.
     */
    'build-cfpb': {
      prod: {
        options: {
          commit: false,
          tag: false,
          push: false
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
      'vars',
      'utilities',
      'meta',
      'media-object'
    ];
    for (var i = 0; i < subtasks.length; i++) {
      var key = subtasks[i];
      topdoc[key] = {
        options: {
          source: 'static/css/',
          destination: 'docs/' + key + '/',
          template: 'node_modules/cf-component-demo/code_examples/',
          templateData: {
            family: 'cfgov-' + key,
            description: key + ' for cfgov-refresh.',
            title: 'cfgov-refresh ' + key + ' docs',
            repo: '<%= pkg.homepage %>'
          }
        }
      };
    }
    return topdoc;
  };

  config.topdoc = dynamicTopdocTasks();

  grunt.initConfig(config);

  /**
   * The above tasks are loaded here.
   */
  grunt.loadNpmTasks('grunt-autoprefixer');
  grunt.loadNpmTasks('grunt-banner');
  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-cfpb-internal');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-release');
  grunt.loadNpmTasks('grunt-string-replace');
  grunt.loadNpmTasks('grunt-topdoc');

  /**
   * Create custom task aliases and combinations
   */
  grunt.registerTask('vendor', ['bower:install', 'concat:cf-less']);
  grunt.registerTask('cssdev', ['less', 'autoprefixer', 'cssmin']);
  grunt.registerTask('jsdev', ['concat:bodyScripts', 'uglify', 'usebanner']);
  grunt.registerTask('default', ['cssdev', 'string-replace:vendor', 'jsdev', 'copy:vendor']);
  grunt.registerTask('test', ['jshint']);

};
