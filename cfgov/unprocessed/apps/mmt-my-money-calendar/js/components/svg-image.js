export const SvgImage = ({ src, ...props }) => (
  <img src={`data:image/svg+xml;base64,${btoa(src)}`} {...props} />
);

export const SvgSpan = ({ src, ...props }) => (
  <span {...props} dangerouslySetInnerHTML={{ __html: src }} />
);

export default SvgImage;
