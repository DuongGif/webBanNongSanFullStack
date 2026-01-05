import React from 'react';

function ProductDetails() {
	return (
		<div className="col-sm-9 padding-right">
			<div className="product-details">
				<div className="col-sm-5">
					<div className="view-product">
						<img src="/assets/images/product-details/1.jpg" alt="" />
						<h3>ZOOM</h3>
					</div>
					<div id="similar-product" className="carousel slide" data-ride="carousel">
						<div className="carousel-inner">
							<div className="item active">
								<a href=""><img src="/assets/images/product-details/similar1.jpg" alt="" /></a>
								<a href=""><img src="/assets/images/product-details/similar2.jpg" alt="" /></a>
								<a href=""><img src="/assets/images/product-details/similar3.jpg" alt="" /></a>
							</div>
							<div className="item">
								<a href=""><img src="/assets/images/product-details/similar1.jpg" alt="" /></a>
								<a href=""><img src="/assets/images/product-details/similar2.jpg" alt="" /></a>
								<a href=""><img src="/assets/images/product-details/similar3.jpg" alt="" /></a>
							</div>
							<div className="item">
								<a href=""><img src="/assets/images/product-details/similar1.jpg" alt="" /></a>
								<a href=""><img src="/assets/images/product-details/similar2.jpg" alt="" /></a>
								<a href=""><img src="/assets/images/product-details/similar3.jpg" alt="" /></a>
							</div>
						</div>
						<a className="left item-control" href="#similar-product" data-slide="prev">
							<i className="fa fa-angle-left"></i>
						</a>
						<a className="right item-control" href="#similar-product" data-slide="next">
							<i className="fa fa-angle-right"></i>
						</a>
					</div>
				</div>
				<div className="col-sm-7">
					<div className="product-information">
						<img src="/assets/images/product-details/new.jpg" className="newarrival" alt="" />
						<h2>Anne Klein Sleeveless Colorblock Scuba</h2>
						<p>Web ID: 1089772</p>
						<img src="/assets/images/product-details/rating.png" alt="" />
						<span>
							<span>US $59</span>
							<label>Quantity:</label>
							<input type="text" value="3" />
							<button type="button" className="btn btn-fefault cart">
								<i className="fa fa-shopping-cart"></i>
								Add to cart
							</button>
						</span>
						<p><b>Availability:</b> In Stock</p>
						<p><b>Condition:</b> New</p>
						<p><b>Brand:</b> E-SHOPPER</p>
						<a href="">
							<img src="/assets/images/product-details/share.png" className="share img-responsive" alt="" />
						</a>
					</div>
				</div>
			</div>
		</div>
	);
}

export default ProductDetails;
