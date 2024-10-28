import React from 'react'
import axios from 'axios'
const ContactPage = () => {
    const [firstName, setFirstName] = React.useState('')
    const [lastName, setLastName] = React.useState('')
    const [email, setEmial] = React.useState('')
    const [phone, setPhone] = React.useState('')
    const [message, setMessage] = React.useState('')
    const [error, setError] = React.useState('')
    const HandleSubmit = (e) => {
        e.preventDefault()
        axios.post('http://127.0.0.1:8000/create/contactus', {
            first_name: firstName,
            last_name: lastName,
            email: email,
            phone: phone,
            message: message
        })
        .then((res) => {
            console.log(res)
        }).then((err) => {
            console.log(err)
        })
    }
  return (
    <div>
      <h1>Contact Page</h1>
      <form onSubmit={HandleSubmit}>
        <label htmlFor="firstName">First Name</label>
        <input type="text" name="firstName" placeholder='john' value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
        <label htmlFor="lastName">Last Name</label>
        <input type="text" name="lastName" placeholder='doe' value={lastName} onChange={(e) => setLastName(e.target.value)}/>
        <label htmlFor="email">Emial</label>
        <input type="email" name="email" placeholder='johndoe@hello.com' value={email} onChange={(e) => setEmial(e.target.value)}/>
        <label htmlFor="phone">Phone</label>
        <input type="number" name="phone" placeholder='1234567890' value={phone} onChange={(e) => setPhone(e.target.value)}/>
        <label htmlFor="message">Message</label>
        <textarea type="text" name="message" placeholder='Type your message here' value={message} onChange={(e) => setMessage(e.target.value)}/>
        <button type="submit">Submit</button>
      </form>
    </div>
  )
}

export default ContactPage
