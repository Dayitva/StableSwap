import React, {useContext} from 'react'
import { XIcon } from '@heroicons/react/solid';
import {ErrorContext} from '../../contexts/ErrorContext';

function Error() {
  const {show, setShow, message} = useContext(ErrorContext);
  return (
    <div 
      className={`
        flex items-center justify-center space-x-2
        bg-gray-900 absolute bottom-2 right-2 
        text-sm p-4 rounded-sm ${show ? 'block' : 'hidden'}
        transition ease-in-out`}
    >
      <button className="
        hover:bg-gray-300 hover:bg-opacity-5 p-2 
        focus:outline-none focus:bg-opacity-20 
        rounded-md"
        onClick={() => {setShow(false);}}
      >
        <XIcon className="w-4 h-4" />
      </button>
      <p className="flex-1">
        {message}
      </p>
    </div>
  )
}

export default Error
