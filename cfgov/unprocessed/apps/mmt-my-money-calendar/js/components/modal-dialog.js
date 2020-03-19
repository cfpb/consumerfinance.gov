import clsx from 'clsx';
import { useLockBodyScroll } from 'react-use';
import Modal from 'react-modal';
import { useBEM } from '../lib/hooks';

export default function ModalDialog({ prompt, showCancel, actions = [], ...props }) {
  const bem = useBEM('modal-dialog');
  const actionButtons = actions.map(({ key, onClick, label, className, condition = true }, index) => {
    if (!condition || (typeof condition === 'function' && !condition())) return null;

    return (
      <li className={bem('action')} key={key || `action-${index}`}>
        <button tabIndex={index} className={clsx(bem('action-button', className))} onClick={onClick}>
          {label}
        </button>
      </li>
    );
  });

  return (
    <Modal
      {...props}
      className={bem()}
      overlayClassName="modal-overlay"
      appElement={document.querySelector('#mmt-my-money-calendar')}
      closeTimeoutMS={150}
    >
      <p className={bem('prompt')}>{prompt}</p>
      <ul className={bem('actions')}>
        {[
          ...actionButtons,
          showCancel && (
            <li className={bem('action')} key="cancel-button">
              <button tabIndex={actionButtons.length} className={clsx(bem('action-button'), bem('action-button', 'cancel'))} onClick={props.onRequestClose}>
                Cancel
              </button>
            </li>
          )
        ]}
      </ul>
    </Modal>
  )
}
