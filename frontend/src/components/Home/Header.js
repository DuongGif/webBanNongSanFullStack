// src/components/Home/Header.js
import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "../../contexts/UserContext";

function Header() {
  const { user, getCartCount, setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = (e) => {
    e.preventDefault();
    setUser(null);
    localStorage.removeItem("user");
    navigate("/"); // Chuyển về trang chủ sau logout
  };

  return (
    <header id="header">
      <div className="header-middle">
        <div className="container">
          <div className="row">
            <div className="col-sm-4">
              <div className="logo pull-left">
                <Link to="/">
                  <img src="/assets/images/home/xoaphonglogo.png" alt="Logo" />
                </Link>
              </div>
            </div>
            <div className="col-sm-8">
              <div className="shop-menu pull-right">
                <ul className="nav navbar-nav">
                  {user ? (
                    <>
                      <li>
                        <Link to="/account">
                          <i className="fa fa-user"></i> Account
                        </Link>
                      </li>
                     
                      <li style={{ position: "relative" }}>
                        <Link to="/cart" style={{ display: "inline-block" }}>
                          <i className="fa fa-shopping-cart"></i> Cart
                          {getCartCount() > 0 && (
                            <span
                              className="cart-count-badge"
                              style={{
                                position: "absolute",
                                top: "-4px",
                                right: "-8px",
                                background: "red",
                                color: "white",
                                borderRadius: "50%",
                                padding: "1px 4px",
                                fontSize: "10px",
                                fontWeight: "bold",
                                lineHeight: 1
                              }}
                            >
                              {getCartCount()}
                            </span>
                          )}
                        </Link>
                      </li>
                      <li>
                        <Link to="/contact">
                          <i className="fa fa-envelope"></i> Contact
                        </Link>
                      </li>
                      <li>
                        <button
                          onClick={handleLogout}
                          style={{
                            background: "none",
                            border: "none",
                            color: "inherit",
                            cursor: "pointer",
                            padding: 0,
                            font: "inherit"
                          }}
                        >
                          <i className="fa fa-lock"></i> Logout
                        </button>
                      </li>
                    </>
                  ) : (
                    <li>
                      <Link to="/login">
                        <i className="fa fa-lock"></i> Login/Signup
                      </Link>
                    </li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      
    </header>
  );
}

export default Header;
