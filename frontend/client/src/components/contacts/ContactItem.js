import React, {useContext} from 'react';
import PropTypes from 'prop-types';
import ContactContext from '../../context/contact/contactContext';

export const ContactItem = ({ contact }) => {
  const contactContext = useContext(ContactContext);
  const { deleteContact, setCurrent, clearCurrent } = contactContext;

  const { _id, name, email, phone, type } = contact;

  const onDelete = () => {
    deleteContact(_id);
    clearCurrent();
  }

  return (
  <div className='card bg-light'>
    <h3 className="text-primary text-left">
      {name}
    </h3>
    <ul className="list">
      {email && (<li>
        {email}
      </li>)}
      {phone && (<li>
       <img src={phone} alt="" />
      </li>)}
    </ul>
    <p>
      <button className="btn btn-dark btn-sm" onClick={() => setCurrent(contact)}>Edit</button>
      <button className="btn btn-danger btn-sm" onClick={onDelete}>Delete</button>
    </p>
  </div>
  );
};

ContactItem.propTypes = {
  contact: PropTypes.object.isRequired
}
