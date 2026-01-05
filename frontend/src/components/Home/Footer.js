import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";


function Footer() {
  return (
    <footer id="footer">
      <div className="footer-top">
        <div className="container">
          <div className="row">
            <div className="col-sm-2">
              <div className="companyinfo">
                <h2><span>Nông sản</span> Xanh</h2>
                <p>Kính chào quý khách!</p>
              </div>
            </div>
            <div className="col-sm-7">
              <div className="col-sm-3">
                <div className="video-gallery text-center">
                  <a href="#">
                    <div className="iframe-img">
                      <img src="/assets/images/home/iframe1.png" alt="" />
                    </div>
                    <div className="overlay-icon">
                      <i className="fa fa-play-circle-o"></i>
                    </div>
                  </a>
                  <p>VietGap</p>
                  <h2>Chứng nhận VietGap</h2>
                </div>
              </div>

              <div className="col-sm-3">
                <div className="video-gallery text-center">
                  <a href="https://www.facebook.com/dtd1801/">
                    <div className="iframe-img">
                      <img src="/assets/images/home/iframe2.png" alt="" />
                    </div>
                    <div className="overlay-icon">
                      <i className="fa fa-play-circle-o"></i>
                    </div>
                  </a>
                  <p>Facebook</p>
                  <h2>Trang chủ chính thức</h2>
                </div>
              </div>

              <div className="col-sm-3">
                <div className="video-gallery text-center">
                  <a href="https://www.facebook.com/people/Anime-Kh%C3%B4ng-ph%E1%BA%A3i-%C4%91%E1%BB%9Di-th%E1%BB%B1c/61569448989531/">
                    <div className="iframe-img">
                      <img src="/assets/images/home/iframe3.png" alt="" />
                    </div>
                    <div className="overlay-icon">
                      <i className="fa fa-play-circle-o"></i>
                    </div>
                  </a>
                  <p>Messenger</p>
                  <h2>Liên hệ với chúng tôi</h2>
                </div>
              </div>

              <div className="col-sm-3">
                <div className="video-gallery text-center">
                  <a href="https://maps.app.goo.gl/smPzdZj8h4wBq6mA9">
                    <div className="iframe-img">
                      <img src="/assets/images/home/iframe4.png" alt="" />
                    </div>
                    <div className="overlay-icon">
                      <i className="fa fa-play-circle-o"></i>
                    </div>
                  </a>
                  <p>Delivery</p>
                  <h2>Ship hàng 24/24</h2>
                </div>
              </div>
            </div>
            <div className="col-sm-3">
              <div className="address">
               <a href='https://www.facebook.com/dhgtvtcaugiay'> <img src="/assets/images/home/UTC.png" alt="" /></a>
                
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="footer-widget">
        <div className="container">
          <div className="row">
            <div className="col-sm-2">
              <div className="single-widget">
                <h2>Nhóm 3</h2>
                <ul className="nav nav-pills nav-stacked">
                  <li><a href="https://www.facebook.com/dtd1801/">Đào Thế Dương</a></li>
                  <li><a href="https://www.facebook.com/trung.hieu.020104">Phạm Trung Hiếu</a></li>
                  <li><a href="https://www.facebook.com/thanh.trinh.813373">Trịnh Xuân Thành</a></li>
                  <li><a href="https://www.youtube.com/watch?v=KgayxOF4Y7E">Xin chân thành cảm ơn !</a></li>
                  
                </ul>
              </div>
            </div>
            
           
           
            <div className="col-sm-2 col-sm-offset-5">
              <div className="single-widget">
                <h2>Liên hệ với chúng tôi</h2>
                <form action="#" className="searchform">
                  <button type="submit" ><Link to="/contact"> <i className="fa fa-envelope"></i> Contact</Link></button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="container">
          <div className="row">
            <p className="pull-left">Đây chỉ là sản phẩm demo không có giá trị thương mại (nhưng mà mua thì vẫn bán =))</p>
            <p className="pull-right">Designed by <span><a target="_blank" rel="noreferrer" href="https://www.facebook.com/dtd1801/">Nhóm 3</a></span></p>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
