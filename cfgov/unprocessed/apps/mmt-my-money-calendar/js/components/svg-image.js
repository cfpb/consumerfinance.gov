const SvgImage = ({ src, ...props }) => (
  <img src={`data:image/svg+xml;base64,${btoa(src)}`} {...props} />
);

export default SvgImage;
