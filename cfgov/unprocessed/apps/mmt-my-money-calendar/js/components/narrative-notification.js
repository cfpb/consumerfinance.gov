import Modal from 'react-modal';
import { useBEM } from '../lib/hooks';

export default function NarrativeModal({showModal, handleOkClick, copy, ...props}) {
    const bem = useBEM('modal-dialog');

    return (
        <Modal  isOpen={showModal}
                className={bem()}
                overlayClassName="modal-overlay"
                appElement={document.querySelector('#mmt-my-money-calendar')}
                style={
                    { content: {
                       textAlign: 'center',
                       padding: '15px'
                      }
                    }
                 }
      >
        <div className='narrative-modal'>
          <h4>{copy.headline}</h4>
          <p>{copy.body}</p>
          {/* <div style={{height: '20px'}} dangerouslySetInnerHTML={{__html: downArrow}}></div> */}
          <button style={{float: 'right'}} onClick={(e) => handleOkClick(e)}>OK</button>
        </div>
        <div className='arrow-down'></div>
      </Modal>
    )
}
