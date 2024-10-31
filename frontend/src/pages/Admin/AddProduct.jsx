import React, { useState } from 'react'
import axios from 'axios'
const AddProduct = () => {
    const [title, setTitle] = useState('')
    const [description, setDescription] = useState('')
    const [price, setPrice] = useState('')
    const [category, setCategory] = useState('')
    const [stock, setStock] = useState('')
    const [product_img, setProduct_img] = useState('')

    const HandleSubmit = (e) => {
        e.preventDefault()
        axios.post('http://127.0.0.1:8000/create/product', {
            title: title,
            description: description,
            price: price,
            category: category,
            stock: stock,
            product_img: product_img
        }, { 
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}`},
          'Content-Type': 'application/json',
          }
    )
        .then((res) => {
            console.log(res)
        })
        .catch((err) => {
            console.log(err)
        })
    }
  return (
    <div>
      <h1>Add Product</h1>
      <form onSubmit={HandleSubmit} >
        <label htmlFor="title">Title</label>
        <input type="text" name="title" placeholder='title' value={title} onChange={(e) => setTitle(e.target.value)}/>
        <label htmlFor="description">Description</label>
        <input type="text" name="description" placeholder='description' value={description} onChange={(e) => setDescription(e.target.value)}/>
        <label htmlFor="price">Price</label>
        <input type="text" name="price" placeholder='price' value={price} onChange={(e) => setPrice(e.target.value)}/>
        <label htmlFor="category">Category</label>
        <input type="text" name="category" placeholder='category' value={category} onChange={(e) => setCategory(e.target.value)}/>
        <label htmlFor="stock">Stock</label>
        <input type="text" name="stock" placeholder='stock' value={stock} onChange={(e) => setStock(e.target.value)}/>
        <label htmlFor="product_img">Product_img</label>
        <input type="file" name="product_img" value={product_img} onChange={(e) => setProduct_img(e.target.value)}/>
        <button type="submit">Submit</button>
      </form>
    </div>
  )
}

export default AddProduct
