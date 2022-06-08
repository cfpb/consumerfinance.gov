export function buildMobileTOC() {
    const expandableTOCFrame = `
    <div class="o-expandable o-expandable__padded o-expandable__background o-expandable__border">
        <button class="o-expandable_header o-expandable_target" title="Expand Table Of Contents">
            <h3 class="h4 o-expandable_header-left o-expandable_label">
                Table of Contents
            </h3>
            <span class="o-expandable_header-right o-expandable_link toc-expandable_link">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.416 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.916 7.917zm-2.958.01a.792.792 0 0 0-.792-.792H9.284V6.12a.792.792 0 1 0-1.583 0V9.5H4.32a.792.792 0 0 0 0 1.584H7.7v3.382a.792.792 0 0 0 1.583 0v-3.382h3.382a.792.792 0 0 0 .792-.791z"/></path></svg>
            </span>
        </button>
        <div id="toc-expand" class="o-expandable_content toc-expandable_content" style="display: none;">
        </div>
    </div>
    `

    let expandableTOCElement = document.createElement('div');
    expandableTOCElement.className = 'toc-div';
    expandableTOCElement.innerHTML = expandableTOCFrame;

    return expandableTOCElement;

}