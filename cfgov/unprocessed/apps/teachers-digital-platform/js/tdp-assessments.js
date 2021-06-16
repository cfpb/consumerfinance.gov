const assessments = {
  init: () => {   
    const patt = /\/youth-financial-education\/assess\/results\//;
    const m = location.href.match(patt);
    if (!m) {
      return;
    }

    var input = document.querySelector('.share-input');
    var a = document.createElement('a');
    a.href = '../show/?r=' + encodeURIComponent(input.dataset.rparam);
    input.value = a.href;
    input.hidden = false;
  }
};

module.exports = assessments;
