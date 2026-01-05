import React, { useState } from 'react';  // Thêm useState vào đây
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet'; // Thêm các import cần thiết
import L from 'leaflet';
import axios from 'axios';  // Thêm axios vào đây
import 'leaflet/dist/leaflet.css';

// Fix icon mặc định không hiện
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const DEFAULT_POSITION = [21.0285, 105.8542]; // Hà Nội

function LocationSelector({ onSelect }) {
  useMapEvents({
    click(e) {
      onSelect([e.latlng.lat, e.latlng.lng]);
    },
  });
  return null;
}

function ShippingFeeCalculator({ onShippingFeeSelected }) {  // Thêm prop để truyền phí ship lên CartPage
  const [destination, setDestination] = useState(null);
  const [phiShip, setPhiShip] = useState(null);
  const [distance, setDistance] = useState(null);

  const handleSelect = async (latlng) => {
    setDestination(latlng);
    try {
      const res = await axios.get('http://127.0.0.1:5000/api/cart/tinh-phi-ship', {
        params: {
          lat1: 21.0285, // vị trí kho hàng cố định (Hà Nội)
          lng1: 105.8542,
          lat2: latlng[0],
          lng2: latlng[1]
        }
      });
      setPhiShip(res.data.phi_ship);
      setDistance(res.data.distance_km);
      if (onShippingFeeSelected) {
        onShippingFeeSelected(res.data.phi_ship);  // Truyền phí ship lên CartPage
      }
    } catch (err) {
      console.error(err);
      setPhiShip(null);
    }
  };

  return (
    <div>
      <h4>Chọn vị trí giao hàng trên bản đồ</h4>
      <MapContainer
        center={DEFAULT_POSITION}
        zoom={13}
        style={{ height: '300px', width: '100%', marginBottom: '1rem' }}
      >
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <LocationSelector onSelect={handleSelect} />
        {destination && <Marker position={destination} />}
      </MapContainer>

      {phiShip !== null && (
        <div>
          <p>Khoảng cách: <strong>{distance} km</strong></p>
          {/* <p>Phí giao hàng: <strong>{phiShip.toLocaleString()}đ</strong></p> */}
        </div>
      )}
    </div>
  );
}

export default ShippingFeeCalculator;
