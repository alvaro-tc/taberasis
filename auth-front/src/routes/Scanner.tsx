// auth-front/src/routes/Scanner.tsx
import { useEffect, useState } from "react";
import PortalLayout from "../layout/PortalLayout";
import { Html5QrcodeScanner } from "html5-qrcode";

export default function Scanner() {
  const [scanner, setScanner] = useState<Html5QrcodeScanner | null>(null);

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
    if (scanner) {
      scanner.render(
        (decodedText, decodedResult) => {
          // Handle the result here.
          console.log(`Scan result: ${decodedText}`, decodedResult);
        },
        (errorMessage) => {
          // parse error, ignore it.
          console.log(`Scan error: ${errorMessage}`);
        }
      );
    }
  }, [scanner]);

  return (
    <PortalLayout>
      <div className="scanner">
        <h1>QR Code Scanner</h1>
        <div id="qr-reader" style={{ width: "500px", margin: "0 auto" }}></div>
      </div>
    </PortalLayout>
  );
}