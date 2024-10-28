import React from 'react'
import axios from 'axios'

const RegisterPage = () => {
    const [username, setUsername] = React.useState('')
    const [email, setEmial] = React.useState('')
    const [password, setPassword] = React.useState('')
    const [error, setError] = React.useState('')
    const HandleSubmit = (e) => {
        e.preventDefault()
        axios.post('http://127.0.0.1:8000/register', {
            username: username,
            email: email,
            password: password,
        })
        .then((res) => {
            console.log(res)
        }).then((err) => {
            console.log(err)
        })
    }
  return (
    <div>
      <h1>Register Page</h1>
      <form onSubmit={HandleSubmit}>
        <label htmlFor="firstName">Username</label>
        <input type="text" name="username" placeholder='john' value={username} onChange={(e) => setUsername(e.target.value)}/>
        <label htmlFor="email">Emial</label>
        <input type="email" name="email" placeholder='johndoe@hello.com' value={email} onChange={(e) => setEmial(e.target.value)}/>
        <label htmlFor="password">password</label>
        <input type="password" name="password" placeholder='1234567890' value={password} onChange={(e) => setPassword(e.target.value)}/>
        <button type="submit">Submit</button>
      </form>
    </div>
  )
}

export default RegisterPage
