class TableDefinition extends window.wagtailStreamField.blocks
  .StructBlockDefinition {
  render(placeholder, prefix, initialState, initialError) {
    const block = super.render(placeholder, prefix, initialState, initialError);
    const table = block.childBlocks.data;

    // Create a new element with paste buttons.
    const html = `
        <div>
            <label class="w-field__label">
                Paste from clipboard
            </label>
            <div class="w-field__wrapper data-field-wrapper">
                <button class="button button-small button-secondary paste-as-text">
                    Create as text
                </button>
                <button class="button button-small button-secondary paste-as-rich-text">
                    Create as rich text
                </button>
            </div>
        </div>
    `.trim();

    const elem = document.createElement('template');
    elem.innerHTML = html;

    // Add the new buttons below the options block.
    const optionsField = document.getElementById(prefix + '-options');
    const optionsWrapper = optionsField.closest(
      'div[data-contentpath="options"]',
    );

    const inserted = optionsWrapper.parentNode.insertBefore(
      elem.content.firstChild,
      optionsWrapper.nextSibling,
    );

    // Add click handlers to the buttons.
    const buttonText = inserted.querySelector('.paste-as-text');
    buttonText.addEventListener('click', this.getClickHandler(table, 'text'));

    const buttonRichText = inserted.querySelector('.paste-as-rich-text');
    buttonRichText.addEventListener(
      'click',
      this.getClickHandler(table, 'rich_text'),
    );

    return block;
  }

  getClickHandler(table, cellType) {
    const that = this;

    return function (event) {
      navigator.clipboard.readText().then((clipText) => {
        that.pasteFromClipboard(clipText, table, cellType);
      });
      event.preventDefault();
    };
  }

  pasteFromClipboard(clipText, table, cellType) {
    const rows = (clipText || '')
      .replace(/^\n+|\n+$/g, '')
      .split('\n')
      .map((line) => line.split('\t'));

    const numColumns = rows[0].length;

    // There needs to be at least 2 rows and 2 columns.
    if (rows.length < 2 || numColumns < 2) {
      return;
    }

    if (!rows.every((row) => row.length == numColumns)) {
      return;
    }

    table.clear();

    // First add headings, then add data.
    const newColumn = table.childBlockDefsByName[cellType];

    const converters = {
      text: function (text) {
        return text;
      },
      rich_text: this.convertTextToDraftail,
    };

    const converter = converters[cellType];

    for (let i = 0; i < numColumns; i++) {
      table.insertColumn(i, newColumn);
      table.columns[i].headingInput.value = rows[0][i];
    }

    for (let i = 1; i < rows.length; i++) {
      table.insertRow(i - 1);
      for (let j = 0; j < numColumns; j++) {
        table.rows[i - 1].blocks[j].setState(converter(rows[i][j]));
      }
    }
  }

  convertTextToDraftail(text) {
    return window.Draftail.createEditorStateFromRaw({
      blocks: [
        {
          type: 'unstyled',
          depth: 0,
          text: text,
          inlineStyleRanges: [],
          entityRanges: [],
        },
      ],
      entityMap: {},
    });
  }
}

window.telepath.register('v1.atomic_elements.tables.Table', TableDefinition);
