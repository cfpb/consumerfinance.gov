import clsx from 'clsx';

export function CardGroup({ columns = 1, children }) {
  const groupClass = clsx('o-card-group', columns > 1 && `o-card-group__column-${columns}`);

  return (
    <div className={groupClass}>
      <div className="o-card-group_cards">{children}</div>
    </div>
  );
}

export const Card = ({ href = '#', title, type, icon, children, footer }) => (
  <article className="m-card">
    <div className="m-card_heading m-card_background">
        {type !== 'general'? (
          
            <a href={href}>
              <div className="header-alignment">
                <div className="m-card_icon" dangerouslySetInnerHTML={{ __html: icon }} />
                <div className="m-card_title">{title}</div>
            </div>
            </a>
         
          ):(
            
               <a href={href}>
                 <div className="header-alignment">
                    <div className="m-card_icon general" dangerouslySetInnerHTML={{ __html: icon }} />
                    <div className="m-card_title">{title}</div>
               </div>
               </a>
            
          )}
    </div>

    {children}

    {footer && <p className="m-card_footer">{footer}</p>}
  </article>
);
