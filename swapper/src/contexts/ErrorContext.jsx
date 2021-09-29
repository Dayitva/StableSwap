import {useState, createContext} from 'react';


const ErrorContext = createContext(false);

function ErrorProvider(props) {
  const [show, setShow] = useState(false);
  const [message, setMessage] = useState('');

  function showMessage(message, duration=5) {
    // Show the message for 5 sec.
    setShow(true);
    setMessage(message);
    setTimeout(() => {
      setShow(false);
      setMessage('');
    }, duration * 1000);
  }

  const providerValues = {
    show, setShow, showMessage, message
  }

  return (
    <ErrorContext.Provider value={providerValues}>
      {props.children}
    </ErrorContext.Provider>
  );
}

export {ErrorContext, ErrorProvider};