import Modal from 'react-modal';
import { useBEM } from '../lib/hooks';

export default function NarrativeModal({showModal, handleOkClick, copy, step, ...props}) {
    const bem = useBEM('modal-dialog');
    
    return (
      <Modal isOpen={showModal}
              className={step === 'step1' ? 'narrative-step1' : bem()} 
              overlayClassName="modal-overlay"
              appElement={step === 'step1' ? document.querySelector('#add') : document.querySelector('#mmt-my-money-calendar')}
              style={
                { content: {
                    textAlign: 'center',
                    padding: '15px'
                  },
                  overlay: {
                    backgroundColor: localStorage.getItem('enteredData') ? '' : 'rgba(0,0,0,0)'
                  }
                }
              }
      >
        <div className='narrative-modal'>
          <h4>{copy.headline}</h4>
          <p>{copy.body}</p>
          <button style={{float: 'right'}} onClick={(e) => handleOkClick(e)}>OK</button>
        </div>
      </Modal>
    )
}
