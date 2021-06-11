const Cookies = require( 'js-cookie' );

const assessments = {
  init: () => {
    const patt = /\/youth-financial-education\/assess\/([^/]+)\/results\//;
    const m = location.href.match(patt);
    if (!m) {
        return;
    }

    const resultUrl = Cookies.get('resultUrl');

    if (resultUrl) {
        alert('resultUrl:' + resultUrl);
    }
  }
};

module.exports = assessments;
