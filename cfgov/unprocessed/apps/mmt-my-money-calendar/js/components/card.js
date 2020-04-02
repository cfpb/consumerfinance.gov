import clsx from 'clsx';

export function CardGroup({ columns = 1, children }) {
  const groupClass = clsx('o-card-group', columns > 1 && `o-card-group__column-${columns}`);

  return (
    <div className={groupClass}>
      <div className="o-card-group_cards">{children}</div>
    </div>
  );
}

export const Card = ({ href = '#', title, icon, children, footer }) => (
  <article className="m-card">
    <h2 className="m-card_heading">
      <a href={href}>
        {icon && <div className="m-card_icon" dangerouslySetInnerHTML={{ __html: icon }} />}

        <span className="m-card_title">{title}</span>
      </a>
    </h2>

    {children}

    {footer && <p className="m-card_footer">{footer}</p>}
  </article>
);
