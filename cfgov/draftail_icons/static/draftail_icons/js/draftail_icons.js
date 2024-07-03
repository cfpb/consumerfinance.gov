class EntityIconSource extends window.React.Component {
  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props;
    const icon_name = window.prompt(
      'Canonical icon name (refer to the Iconography page in the CFPB Design System):',
    );

    if (icon_name) {
      const content = editorState.getCurrentContent();
      const selection = editorState.getSelection();

      const contentWithEntity = content.createEntity(
        entityType.type,
        'SEGMENTED',
        {
          'icon-name': icon_name,
        },
      );
      const entityKey = contentWithEntity.getLastCreatedEntityKey();

      // Attach the new entity to a space, since it has to have a range of
      // some length > 0. This will get rendered out in the decorator below
      // and in the frontend after storage in the database.
      const newContent = window.DraftJS.Modifier.replaceText(
        content,
        selection,
        ' ',
        null,
        entityKey,
      );
      const nextState = window.DraftJS.EditorState.push(
        editorState,
        newContent,
        'insert-characters',
      );

      onComplete(nextState);
    } else {
      onComplete(editorState);
    }
  }

  render() {
    return null;
  }
}

const Icon = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();

  // Get the icon name, then add an img tag that loads the icon from our
  // static files path. This will render the ICON "entity" with the svg in
  // the editor.
  var icon_name = data['icon-name'];
  var icon_url = `/static/icons/${icon_name}.svg`;
  return window.React.createElement('img', {
    src: icon_url,
    'data-icon-name': icon_name,
  });
};

window.draftail.registerPlugin({
  type: 'ICON',
  source: EntityIconSource,
  decorator: Icon,
});
