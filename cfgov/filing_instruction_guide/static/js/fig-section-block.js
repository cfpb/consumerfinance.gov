class FigSectionDefinition extends window.wagtailStreamField.blocks
  .StructBlockDefinition {
  render(placeholder, prefix, initialState, initialError) {
    const block = super.render(placeholder, prefix, initialState, initialError);

    const sectionID = $(document).find('#' + prefix + '-section_id');
    sectionID.prop('disabled', true);

    return block;
  }
}

window.telepath.register(
  'filing_instruction_guide.blocks.FigSection',
  FigSectionDefinition,
);
