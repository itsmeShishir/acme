import React from 'react'
import axios from 'axios'
import { useQuery } from '@tanstack/react-query'

const fetchProducts = async () => {
  const res = await axios.get('http://127.0.0.1:8000/product')
  return res.data.results
}

const AllProducts = () => {
  const { data } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
    staleTime: 1000 * 60,
    cacheTime: 5000 * 60,
  })
  console.log(data)
  return (
    <div>
      <h1>All Products</h1>
      {data.map((product) => (
        <div key={product.id}>
          <img src={product.product_img} alt={product.title} />
          <h1>{product.title}</h1>
          <h2>{product.description}</h2>
          <h3>{product.price}</h3>
          <h4>{product.category}</h4>
        </div>
      ))}
    </div>
  )
}

export default AllProducts
