import clsx from 'clsx';

export const ButtonGroup = ({ children }) => (
  <div className="m-btn-group">
    {children}
  </div>
);

export function Button({ as = 'button', fullWidth = false, className = '', variant = 'primary', disabled = false, link = false, children, ...btnProps }) {
  const TagName = as;
  const classes = clsx(className, 'a-btn', {
    'a-btn__secondary': variant === 'secondary',
    'a-btn__warning': variant === 'warning',
    'a-btn__disabled': disabled,
    'a-btn__super': variant === 'super',
    'a-btn__full-on-xs': fullWidth,
    'a-btn__link': link,
  });

  return (
    <TagName {...btnProps} className={classes} disabled={disabled}>
      {children}
    </TagName>
  )
};

export default Button;
