export function buildMobileTOC() {
    expandableTOCFrame = `<div class="o-expandable
    o-expandable__padded
    o-expandable__background
    o-expandable__border">
<button class="o-expandable_header o-expandable_target"
    title="Expand Table Of Contents">
<h3 class="h4 o-expandable_header-left o-expandable_label">
    Table of Contents
</h3>
<span class="o-expandable_header-right o-expandable_link">
    <span class="o-expandable_cue o-expandable_cue-open">
        <span class="u-visually-hidden-on-mobile">Show</span>
        {% include icons/plus-round.svg %}
    </span>
    <span class="o-expandable_cue o-expandable_cue-close">
        <span class="u-visually-hidden-on-mobile">Hide</span>
        {% include icons/minus-round.svg %}
    </span>
</span>
</button>
<div class="o-expandable_content toc-expandable_content">
</div>
</div>`

    let expandableTOCElement = document.createElement('div');
    expandableTOCElement.className = 'toc-div';
    expandableTOCElement.innerHTML = expandableTOCFrame;

    return expandableTOCElement;

}