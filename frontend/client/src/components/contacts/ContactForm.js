import React, { useState, useContext, useEffect } from 'react';
import ContactContext from '../../context/contact/contactContext';

const ContactForm = () => {
  const contactContext = useContext(ContactContext);

  const { addContact, updateContact, clearCurrent, current } = contactContext;

  useEffect(() => {
    if(current !== null) {
      setContact(current);
    } else {
      setContact({
        name: '',
        email: '',
        phone: '',
        type: 'personal'
      });
    }
  }, [contactContext, current])

  const [contact, setContact] = useState({
    name: '',
    email: '',
    phone: '',
    type: 'personal'
  });

  const { name, email, phone, type  } = contact;

  const onChange = e => setContact({ ...contact, [e.target.name]: e.target.value });

  const onSubmit = e => {
    e.preventDefault();
    if(current === null) {
      addContact(contact);
    } else {
      updateContact(contact);
    }
    setContact({
      name: '',
      email: '',
      phone: '',
      type: 'personal'
    });
  }

  const clearAll = () => {
    clearCurrent();
  }

  return(
    <form onSubmit={onSubmit}>
      <h2 className="text-primary">{current ? 'Update data' : 'Add your own data'}</h2>
      <input type="text" placeholder='Checkup Recommendation' name='name' value={name} onChange={onChange} />
      <input type="text" placeholder='Date' name='email' value={email} onChange={onChange} />
      <input type="text" placeholder='Image URL' name='phone' value={phone} onChange={onChange} />
      <div>
        <input type="submit" value={current ? 'Update data' : 'Add Data'} className='btn btn-primary btn-block' />
      </div>
      {current && <div>
        <button className="btn btn-light btn-block" onClick={clearAll}>Clear</button>
      </div>}
    </form>
  )
}

export default ContactForm;