import clsx from 'clsx';
import informationRound from '@cfpb/cfpb-icons/src/icons/information-round.svg';

export function Notification({ variant, message, icon = informationRound, visible = true, actionLink, children }) {
  const classes = clsx('m-notification', visible && 'm-notification__visible', variant && `m-notification__${variant}`);

  return (
    <div className={classes}>
      <span className="notification-icon" dangerouslySetInnerHTML={{ __html: icon }} />
      <div className="m-notification_content">
        <div className="h4 m-notification_message">{message}</div>
        {children}
      </div>
      {actionLink}
    </div>
  );
}
