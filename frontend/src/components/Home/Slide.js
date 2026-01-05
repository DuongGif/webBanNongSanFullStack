import React from 'react';

function Slide() {
  return (
    <section id="slider">
      <div className="container">
        <div className="row">
          <div className="col-sm-12">
            <div id="slider-carousel" className="carousel slide" data-ride="carousel">
              <ol className="carousel-indicators">
                <li data-target="#slider-carousel" data-slide-to="0" className="active"></li>
                <li data-target="#slider-carousel" data-slide-to="1"></li>
                <li data-target="#slider-carousel" data-slide-to="2"></li>
              </ol>

              <div className="carousel-inner">
                <div className="item active">
                  <div className="col-sm-6">
                  <h1><span>Nông sản</span> Xanh</h1>
                    <h2>Rau củ được trồng tự nhiên</h2>
                    <p>Trang web bán nông sản tươi , sạch , giá cả hợp lý nhất Việt Nam.</p>
                    {/* <button type="button" className="btn btn-default get">Get it now</button> */}
                  </div>
                  <div className="col-sm-6">
                    <img src="/assets/images/home/girl1.jpg" className="girl img-responsive" alt="" />
                    <img src="/assets/images/home/pricing.png" className="pricing" alt="" />
                  </div>
                </div>

                <div className="item">
                  <div className="col-sm-6">
                  <h1><span>Nông sản</span> Xanh</h1>
                    <h2>100% Thực phẩm sạch từ trang trại</h2>
                    <p>Từ nông trại đến bàn ăn - Nông sản sạch, an toàn cho sức khỏe gia đình bạn.</p>
                    {/* <button type="button" className="btn btn-default get">Get it now</button> */}
                  </div>
                  <div className="col-sm-6">
                    <img src="/assets/images/home/girl2.jpg" className="girl img-responsive" alt="" />
                    <img src="/assets/images/home/pricing.png" className="pricing" alt="" />
                  </div>
                </div>

                <div className="item">
                  <div className="col-sm-6">
                    <h1><span>Nông sản</span> Xanh</h1>
                    <h2>Vận chuyển nhanh khắp nẻo đất nước</h2>
                    <p>Đặt hàng hôm nay, giao tận nơi miễn phí trong bán kính 5km.</p>
                    {/* <button type="button" className="btn btn-default get">Get it now</button> */}
                  </div>
                  <div className="col-sm-6">
                    <img src="/assets/images/home/girl3.jpg" className="girl img-responsive" alt="" />
                    <img src="/assets/images/home/pricing.png" className="pricing" alt="" />
                  </div>
                </div>
              </div>

              <a href="#slider-carousel" className="left control-carousel hidden-xs" data-slide="prev">
                <i className="fa fa-angle-left"></i>
              </a>
              <a href="#slider-carousel" className="right control-carousel hidden-xs" data-slide="next">
                <i className="fa fa-angle-right"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Slide;
