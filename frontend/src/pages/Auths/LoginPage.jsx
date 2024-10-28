import React from 'react'
import axios from 'axios'

const LoginPage = () => {
    const [email, setEmial] = React.useState('')
    const [password, setPassword] = React.useState('')
    const [error, setError] = React.useState('')
    const HandleSubmit = (e) => {
        e.preventDefault()
         axios.post('http://127.0.0.1:8000/login', {
            email: email,
            password: password,
        })
        .then((res) => {
            // set data in cookie js
            // setCookie('sessionid', res.data.)
            // setCookie('role', res.data.role)
            // setCookie('email', res.data.email)
            console.log(res.data.success)
        }).then((err) => {
            console.log(err)
        })
    }
  return (
    <div>
      <h1>Login Page</h1>
      <form onSubmit={HandleSubmit}>
        <label htmlFor="email">Emial</label>
        <input type="email" name="email" placeholder='johndoe@hello.com' value={email} onChange={(e) => setEmial(e.target.value)}/>
        <label htmlFor="password">password</label>
        <input type="password" name="password" placeholder='1234567890' value={password} onChange={(e) => setPassword(e.target.value)}/>
        <button type="submit">Submit</button>
      </form>
    </div>
  )
}

export default LoginPage
