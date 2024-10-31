// auth-front/src/routes/Scanner.tsx
import { useEffect, useState } from "react";
import PortalLayout from "../layout/PortalLayout";
import { Html5QrcodeScanner } from "html5-qrcode";
import { API_URL } from "../auth/authConstants";
import { useAuth } from "../auth/AuthProvider";

interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
}

export default function Scanner() {
  const auth = useAuth();
  const [scanner, setScanner] = useState<Html5QrcodeScanner | null>(null);
  const [product, setProduct] = useState<Product | null>(null);
  const [message, setMessage] = useState("");
  const [isScanning, setIsScanning] = useState(true);

  useEffect(() => {
    const newScanner = new Html5QrcodeScanner(
      "qr-reader",
      { fps: 10, qrbox: { width: 250, height: 250 } },
      /* verbose= */ false
    );
    setScanner(newScanner);

    return () => {
      if (newScanner) {
        newScanner.clear().catch((error) => {
          console.error("Failed to clear scanner", error);
        });
      }
    };
  }, []);

  useEffect(() => {
    if (scanner && isScanning) {
      scanner.render(
        async (decodedText, decodedResult) => {
          // Handle the result here.
          console.log(`Scan result: ${decodedText}`, decodedResult);
          try {
            const qrData = JSON.parse(decodedText);
            if (qrData.id) {
              const accessToken = auth.getAccessToken();
              const response = await fetch(`${API_URL}/products/${qrData.id}`, {
                method: "GET",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${accessToken}`,
                },
              });
              if (response.ok) {
                const productData = await response.json();
                setProduct(productData);
                setMessage("Producto escaneado");
              } else {
                console.error("Failed to fetch product", response.statusText);
                setMessage("Error al obtener el producto");
              }
            } else {
              setMessage("QR inválido");
            }
          } catch (error) {
            console.error("Failed to parse QR code", error);
            setMessage("Error al leer el QR");
          }
          setIsScanning(false);
          scanner.clear().catch((error) => {
            console.error("Failed to clear scanner", error);
          });
        },
        (errorMessage) => {
          // parse error, ignore it.
          console.log(`Scan error: ${errorMessage}`);
        }
      );
    }
  }, [scanner, isScanning, auth]);

  const handleRetry = () => {
    setProduct(null);
    setMessage("");
    setIsScanning(true);
  };

  return (
    <PortalLayout>
      <div className="scanner">
        <h1>QR Code Scanner</h1>
        {isScanning ? (
          <div id="qr-reader" style={{ width: "500px", margin: "0 auto" }}></div>
        ) : (
          <>
            {message && <p>{message}</p>}
            {product && (
              <div>
                <h2>Producto</h2>
                <p><strong>ID:</strong> {product.id}</p>
                <p><strong>Nombre:</strong> {product.name}</p>
                <p><strong>Descripción:</strong> {product.description}</p>
                <p><strong>Precio:</strong> ${product.price}</p>
              </div>
            )}
            <button onClick={handleRetry}>Volver a intentar</button>
          </>
        )}
      </div>
    </PortalLayout>
  );
}