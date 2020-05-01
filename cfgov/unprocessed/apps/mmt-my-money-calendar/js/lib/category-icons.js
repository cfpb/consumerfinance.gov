const requireCategoryIcons = require.context('img/category-icons', true, /\.svg$/);
const categoryIcons = requireCategoryIcons.keys().reduce((images, path) => {
  const name = path.replace(/(\.\/|\.svg)/g, '');
  images[name] = requireCategoryIcons(path);
  return images;
}, {});

export default categoryIcons;
