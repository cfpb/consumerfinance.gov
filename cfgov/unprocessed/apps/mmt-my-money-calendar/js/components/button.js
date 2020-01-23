import clsx from 'clsx';

const ButtonIcon = ({ side = 'left', icon }) => (
  <span className={`a-btn_icon a-btn_icon__on-${side}`} dangerouslySetInnerHTML={{__html: icon}}></span>
);

export const ButtonGroup = ({ children }) => <div className="m-btn-group">{children}</div>;

export function Button({
  as = 'button',
  fullWidth = false,
  className = '',
  variant = 'primary',
  disabled = false,
  link = false,
  icon = null,
  iconSide = 'left',
  children,
  ...btnProps
}) {
  const TagName = as;
  const classes = clsx(className, 'a-btn', {
    'a-btn__secondary': variant === 'secondary',
    'a-btn__warning': variant === 'warning',
    'a-btn__disabled': disabled,
    'a-btn__super': variant === 'super',
    'a-btn__full-on-xs': fullWidth,
    'a-btn__link': link,
  });

  const btnIcon = icon ? <ButtonIcon icon={icon} side={iconSide} /> : null;

  return (
    <TagName {...btnProps} className={classes} disabled={disabled}>
      {icon && iconSide === 'left' && btnIcon}
      {children}
      {icon && iconSide === 'right' && btnIcon}
    </TagName>
  );
}

export default Button;
