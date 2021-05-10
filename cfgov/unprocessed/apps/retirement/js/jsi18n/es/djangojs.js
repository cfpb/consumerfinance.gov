  "use strict";
  (function (globals) {

      var django = window.django = globals.django || (globals.django = {});

      django.pluralidx = function (count) {
          return (count === 1) ? 0 : 1;
      };

      django.catalog = {
          "is your full benefit claiming age.": "de edad es su plena edad de jubilación.",
          "is past your full benefit claiming age.": "años de edad es después de haber cumplido su plena edad de jubilación.",
          "is your maximum benefit claiming age.": "es la edad máxima para solicitar.",
          "62": "62 años",
          "63": "63 años",
          "64": "64 años",
          "65": "65 años",
          "66": "66 años",
          "66 and 2 months": "66 años y 2 meses ",
          "66 and 4 months": "66 años y 4 meses ",
          "66 and 6 months": "66 años y 6 meses ",
          "66 and 8 months": "66 años y 8 meses ",
          "66 and 10 months": "66 años y 10 meses ",
          "67": "67 años",
          "68": "68 años",
          "69": "69 años",
          "70": "70 años",
          "Age": "",
          "<strong>reduces</strong> your monthly benefit by&nbsp;<strong>": "años de edad, su beneficio se <strong>reducirá</strong> un&nbsp;<strong>",
          "Compared to claiming at your full benefit claiming age.": "en comparación con su plena edad de jubilación.",
          "Compared to claiming at": "en comparación con su beneficio a los XXX años.",
          "(in today's dollars) (sin ajustes por inflación)": "(sin ajustes por inflación)",
          "Claiming at age": "A los",
          "<strong>increases</strong> your benefit by&nbsp;<strong>": "años de edad, su beneficio <strong>aumentará</strong> un&nbsp;<strong>",
          "Age 70 is your maximum benefit claiming age.": "70 años es la edad máxima para solicitar."
      };

      django.gettext = function (msgid) {
          var value = django.catalog[msgid];
          if (typeof(value) == 'undefined') {
              return msgid;
          } else {
              return (typeof(value) == 'string') ? value : value[0];
        }};

      /* gettext identity library */

      django.ngettext = function (singular, plural, count) { return (count == 1) ? singular : plural; };
      django.gettext_noop = function (msgid) { return msgid; };
      django.pgettext = function (context, msgid) { return msgid; };
      django.npgettext = function (context, singular, plural, count) { return (count == 1) ? singular : plural; };

      django.interpolate = function (fmt, obj, named) {
        if (named) {
          return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)]);});
        } else {
          return fmt.replace(/%s/g, function(match){return String(obj.shift());});
        }
      };

      /* formatting library */

      django.formats = {
        "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i",
        "DATETIME_INPUT_FORMATS": [
          "%d/%m/%Y %H:%M:%S",
          "%d/%m/%Y %H:%M:%S.%f",
          "%d/%m/%Y %H:%M",
          "%d/%m/%y %H:%M:%S",
          "%d/%m/%y %H:%M:%S.%f",
          "%d/%m/%y %H:%M",
          "%Y-%m-%d %H:%M:%S",
          "%Y-%m-%d %H:%M:%S.%f",
          "%Y-%m-%d %H:%M",
          "%Y-%m-%d"
        ],
        "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
        "DATE_INPUT_FORMATS": [
          "%d/%m/%Y",
          "%d/%m/%y",
          "%Y-%m-%d"
        ],
        "DECIMAL_SEPARATOR": ",",
        "FIRST_DAY_OF_WEEK": "1",
        "MONTH_DAY_FORMAT": "j \\d\\e F",
        "NUMBER_GROUPING": "3",
        "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
        "SHORT_DATE_FORMAT": "d/m/Y",
        "THOUSAND_SEPARATOR": ".",
        "TIME_FORMAT": "H:i:s",
        "TIME_INPUT_FORMATS": [
          "%H:%M:%S",
          "%H:%M:%S.%f",
          "%H:%M"
        ],
        "YEAR_MONTH_FORMAT": "F \\d\\e Y"
      };

      django.get_format = function (format_type) {
        var value = django.formats[format_type];
        if (typeof(value) == 'undefined') {
          return format_type;
          } else {
              return value;
          }
      };

      /* add to global namespace */
      globals.pluralidx = django.pluralidx;
      globals.gettext = django.gettext;
      globals.ngettext = django.ngettext;
      globals.gettext_noop = django.gettext_noop;
      globals.pgettext = django.pgettext;
      globals.npgettext = django.npgettext;
      globals.interpolate = django.interpolate;
      globals.get_format = django.get_format;

  }(this));
