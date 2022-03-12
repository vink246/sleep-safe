import React, {useContext, useRef, useEffect} from 'react';
import ContactContext from '../../context/contact/contactContext';
import { FILTER_CONTACTS } from '../../context/types';

const ContactFilter = () => {
  const contactContext = useContext(ContactContext);
  const text = useRef('');

  const { filterContacts, clearFilter, filtered } = contactContext;

  useEffect(() => {
    if(filtered === null) {
      text.current.value = '';
    }
  })

  const onChange = e => {
    if(text.current.value !== '') {
      filterContacts(e.target.value);
    } else {
      clearFilter();
    }
  }


  return (
    <form>
      <input ref={text} type="text" placeholder='Filter Diagnoses...' onChange={onChange}/>
    </form>
  );
};

export default ContactFilter;