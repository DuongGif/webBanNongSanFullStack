import React, { useState, useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../contexts/UserContext'; // Đảm bảo đường dẫn đúng

const ContactPage = () => {
  const { user } = useContext(UserContext);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user?.maTaiKhoan) {
      alert('Bạn cần đăng nhập trước khi gửi liên hệ.');
      return;
    }

    try {
      await axios.post('http://127.0.0.1:5000/api/contact', {
        ...formData,
        maTaiKhoan: user.maTaiKhoan,
      });
      alert('Gửi liên hệ thành công! Chúng tôi sẽ phản hồi bạn sớm nhất có thể.');
      setFormData({ name: '', email: '', subject: '', message: '' });
    } catch (error) {
      console.error('Lỗi khi gửi liên hệ:', error);
      alert('Đã xảy ra lỗi khi gửi liên hệ.');
    }
  };

  return (
    <div>
      <div id="contact-page" className="container">
        <div className="bg">
          <div className="row">
            <div className="col-sm-12">
              <h2 className="title text-center">Contact <strong>Us</strong></h2>
              {/* Nhúng Google Map vào trang */}
              <div className="map-container">
                <iframe 
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3724.1131159425695!2d105.80084557352365!3d21.028159487802547!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3135ab424a50fff9%3A0xbe3a7f3670c0a45f!2zVHLGsOG7nW5nIMSQ4bqhaSBI4buNYyBHaWFvIFRow7RuZyBW4bqtbiBU4bqjaQ!5e0!3m2!1svi!2s!4v1745136694453!5m2!1svi!2s"
                  width="100%" height="450" style={{ border: '0' }} allowFullScreen="" loading="lazy" referrerPolicy="no-referrer-when-downgrade">
                </iframe>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-sm-8">
              <div className="contact-form">
                <h2 className="title text-center">Get In Touch</h2>
                <div className="status alert alert-success" style={{ display: 'none' }}></div>
                <form className="contact-form row" onSubmit={handleSubmit}>
                  <div className="form-group col-md-6">
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      className="form-control"
                      required
                      placeholder="Name"
                    />
                  </div>
                  <div className="form-group col-md-6">
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      className="form-control"
                      required
                      placeholder="Email"
                    />
                  </div>
                  <div className="form-group col-md-12">
                    <input
                      type="text"
                      name="subject"
                      value={formData.subject}
                      onChange={handleChange}
                      className="form-control"
                      required
                      placeholder="Subject"
                    />
                  </div>
                  <div className="form-group col-md-12">
                    <textarea
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      className="form-control"
                      rows="8"
                      required
                      placeholder="Your Message Here"
                    ></textarea>
                  </div>
                  <div className="form-group col-md-12">
                    <input
                      type="submit"
                      className="btn btn-primary pull-right"
                      value="Submit"
                    />
                  </div>
                </form>
              </div>
            </div>
            <div className="col-sm-4">
              <div className="contact-info">
                <h2 className="title text-center">Contact Info</h2>
                <address>
                  <h4>E-Shopper - NÔNG SẢN XANH </h4>
                  <h4>Đại học Giao thông vận tải</h4>
                  <h4>Hà Nội </h4>
                  <h4>Mobile:012345678</h4>
                  <h4>Email: admin@nongsan.com</h4>
                </address>
                <div className="social-networks">
                  <h2 className="title text-center">Social Networking</h2>
                  <ul>
                    <li><a href="#"><i className="fa fa-facebook"></i></a></li>
                    <li><a href="#"><i className="fa fa-twitter"></i></a></li>
                    <li><a href="#"><i className="fa fa-google-plus"></i></a></li>
                    <li><a href="#"><i className="fa fa-youtube"></i></a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> 
    </div>
  );
};

export default ContactPage;
