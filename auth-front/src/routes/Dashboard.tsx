// auth-front/src/routes/Dashboard.tsx
import { useEffect, useState } from "react";
import PortalLayout from "../layout/PortalLayout";
import { useAuth } from "../auth/AuthProvider";
import { API_URL } from "../auth/authConstants";

interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
}

export default function Dashboard() {
  const auth = useAuth();
  const [products, setProducts] = useState<Product[]>([]);

  async function getProducts() {
    const accessToken = auth.getAccessToken();
    try {
      const response = await fetch(`${API_URL}/products`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (response.ok) {
        const json = await response.json();
        setProducts(json);
      } else {
        console.error("Failed to fetch products", response.statusText);
      }
    } catch (error) {
      console.error("An error occurred while fetching products", error);
    }
  }

  useEffect(() => {
    getProducts();
  }, []);

  return (
    <PortalLayout>
      <div className="dashboard">
        <h1>Dashboard de {auth.getUser()?.username ?? ""}</h1>
        <div className="products">
          {products.map((product: Product) => (
            <div key={product.id} className="product">
              <h3>{product.name}</h3>
              <p>{product.description}</p>
              <p>${product.price}</p>
            </div>
          ))}
        </div>
      </div>
    </PortalLayout>
  );
}