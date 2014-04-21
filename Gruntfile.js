module.exports = function(grunt) {

  'use strict';

  var path = require('path');

  grunt.initConfig({

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
          targetDir: './src/vendor/',
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
     * Concatenate cf-* LESS files prior to compiling them.
     */
    concat: {
      'cf-less': {
        src: ['src/vendor/cf-*/*.less'],
        dest: 'src/vendor/cf-concat/cf.less',
      },
      bodyScripts: {
        src: [
          'src/vendor/jquery/jquery.js',
          'src/vendor/cf-*/*.js',
          'src/static/js/app.js'
        ],
        dest: 'src/static/js/main.js'
      }
    },

    /**
     * LESS: https://github.com/gruntjs/grunt-contrib-less
     * 
     * Compile LESS files to CSS.
     */
    less: {
      main: {
        options: {
          paths: grunt.file.expand('src/vendor/**/'),
        },
        files: {
          'src/static/css/main.css': ['src/static/css/main.less']
        }
      },
      ie8: {
        options: {
          banner: '<%= banner.cfpb %>',
          paths: ['src/static'],
        },
        files: {
          'dist/static/css/ie8.css': ['src/static/css/ie/ie8.less']
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
          'src/static/css/': ['src/static/css/main.css']
        },
        options: {
          replacements: [{
            pattern: /url\((.*?)\)/ig,
            replacement: function (match, p1, offset, string) {
              var path, pathParts, pathLength, filename, newPath;
              path = p1.replace(/["']/g,''); // Removes quotation marks if there are any
              pathParts = path.split('/'); // Splits the path so we can find the filename
              pathLength = pathParts.length;
              filename = pathParts[pathLength-1]; // The filename is the last item in pathParts

              grunt.verbose.writeln('');
              grunt.verbose.writeln('--------------');
              grunt.verbose.writeln('Original path:');
              grunt.verbose.writeln(match);
              grunt.verbose.writeln('--------------');

              // Rewrite the path based on the file type
              // Note that .svg can be a font or a graphic, not sure what to do about this.
              if (filename.indexOf('.eot') !== -1 ||
                  filename.indexOf('.woff') !== -1 ||
                  filename.indexOf('.ttf') !== -1 ||
                  filename.indexOf('.svg') !== -1)
              {
                newPath = 'url("../fonts/'+filename+'")';
                grunt.verbose.writeln('New path:');
                grunt.verbose.writeln(newPath);
                grunt.verbose.writeln('--------------');
                return newPath;
              } else if (filename.indexOf('.png') !== -1 ||
                  filename.indexOf('.gif') !== -1 ||
                  filename.indexOf('.jpg') !== -1)
              {
                newPath = 'url("../img/'+filename+'")';
                grunt.verbose.writeln('New path:');
                grunt.verbose.writeln(newPath);
                grunt.verbose.writeln('--------------');
                return newPath;
              } else {
                grunt.verbose.writeln('No new path.');
                grunt.verbose.writeln('--------------');
                return match;
              }

              grunt.verbose.writeln('--------------');
              return match;
            }
          }]
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
        // Prefix all CSS files found in `src/static/css` and overwrite.
        expand: true,
        src: 'src/static/css/*.css'
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
      //   src: 'src/vendor/html5shiv/html5shiv-printshiv.js',
      //   dest: 'src/static/js/html5shiv-printshiv.js'
      // },
      bodyScripts: {
        src: ['src/static/js/main.js'],
        dest: 'src/static/js/main.min.js'
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
          src: [ 'src/static/css/*.min.css', 'src/static/js/*.min.js' ]
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
          //root: '/src/'
        },
        files: {
          'src/static/css/main.min.css': ['src/static/css/main.css'],
        }
      }
    },

    /**
     * Clean: https://github.com/gruntjs/grunt-contrib-clean
     *
     * Clear files and folders.
     */
    clean: {
      bowerDir: ['bower_components'],
      dist: ['dist/**/*', '!dist/.git/']
    },

    /**
     * Copy: https://github.com/gruntjs/grunt-contrib-copy
     * 
     * Copy files and folders.
     */
    copy: {
      dist: {
        files:
        [
          {
            expand: true,
            cwd: 'src/',
            src: [

              // Bring over everything in src/
              '**',

              // Except...

              // Don't bring over everything in static/
              '!static/**',
              // Only include minified assets in css/ and js/
              'static/css/*.min.css',
              'static/js/*.min.js',
              'static/fonts/**',

              // Exclude all vendor files because a lot will get concatenated
              '!vendor/**',
              // Only include vendor files that we use independently
              'vendor/html5shiv/html5shiv-printshiv.js'

            ],
            dest: 'dist/'
          }
        ]
      }
    },

    /**
     * Compress: https://github.com/gruntjs/grunt-contrib-compress
     * 
     * Creates a ZIP file with the contents of the dist folder.
     */
    compress: {
      dist: {
        options: {
          archive: 'capital-framework-dist.zip'
        },
        files: [
          {src: ['dist/**'], dest: '/'}
        ]
      }
    },

    /**
     * grunt-gh-pages: https://github.com/tschaub/grunt-gh-pages
     * 
     * Use Grunt to push to your gh-pages branch hosted on GitHub or any other branch anywhere else
     */
    'gh-pages': {
      options: {
        base: 'dist'
      },
      src: ['**']
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
      all: ['src/static/js/main.js']
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
        files: ['Gruntfile.js', 'src/static/css/*.less', '<%= uglify.bodyScripts.src %>'],
        tasks: ['default']
      }
    }
  });

  /**
   * The above tasks are loaded here.
   */
  grunt.loadNpmTasks('grunt-autoprefixer');
  grunt.loadNpmTasks('grunt-banner');
  grunt.loadNpmTasks('grunt-bower-task');
  grunt.loadNpmTasks('grunt-cfpb-internal');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-compress');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-release');
  grunt.loadNpmTasks('grunt-string-replace');
  grunt.loadNpmTasks('grunt-gh-pages');

  /**
   * Create custom task aliases and combinations
   */
  grunt.registerTask('vendor', ['clean:bowerDir', 'bower:install', 'concat:cf-less']);
  grunt.registerTask('compile', ['less', 'string-replace:vendor', 'autoprefixer', 'concat:bodyScripts']);
  grunt.registerTask('default', ['compile']);
  grunt.registerTask('dist', ['cssmin', 'uglify', 'usebanner', 'clean:dist', 'copy:dist', 'compress:dist']);
  grunt.registerTask('test', ['jshint']);

};
