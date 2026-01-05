function Login({
  loginData,
  handleLoginChange,
  handleLoginSubmit,
  signupData,
  handleSignupChange,
  handleSendOtp,
  handleSignupSubmit,
  otpSent,
  otpError,
  handleGoHome,
}) {
  return (
    <section id="form">
      <div className="container">
        <div className="row">
          {/* Login Form */}
          <div className="col-sm-4 col-sm-offset-1">
            <div className="login-form">
              <h2>Login to your account</h2>
              <form onSubmit={handleLoginSubmit}>
                <input
                  type="email"
                  name="email"
                  placeholder="Email Address"
                  value={loginData.email}
                  onChange={handleLoginChange}
                />
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={loginData.password}
                  onChange={handleLoginChange}
                />
                <span>
                  <input type="checkbox" className="checkbox" /> Keep me signed in
                </span>
                <button type="submit" className="btn btn-default">
                  Login
                </button>
              </form>
            </div>
          </div>

          <div className="col-sm-1">
            <h2 className="or">OR</h2>
          </div>

          {/* Signup Form */}
          <div className="col-sm-4">
            <div className="signup-form">
              <h2>New User Signup!</h2>
              <form onSubmit={handleSignupSubmit}>
                <input
                  type="text"
                  name="name"
                  placeholder="Name"
                  value={signupData.name}
                  onChange={handleSignupChange}
                />
                <input
                  type="email"
                  name="email"
                  placeholder="Email Address"
                  value={signupData.email}
                  onChange={handleSignupChange}
                />
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={signupData.password}
                  onChange={handleSignupChange}
                />
                <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
                  <input
                    type="text"
                    name="otp"
                    placeholder="Nhập mã OTP"
                    value={signupData.otp}
                    onChange={handleSignupChange}
                    style={{ flex: 1 }}
                  />
                  <button
                    type="button"
                    className="btn btn-default"
                    onClick={handleSendOtp}
                  >
                    {otpSent ? "OTP đã gửi" : "Nhận OTP"}
                  </button>
                </div>
                {otpError && <div style={{ color: "red" }}>{otpError}</div>}
                <button type="submit" className="btn btn-default">
                  Signup
                </button>
                <p>
                  
                </p>
                {/* Nút quay về trang chủ */}
                <div className="text-center mt-3">
                  <button
                    type="button"
                    className="btn btn-default"
                    onClick={handleGoHome}
                  >
                    Quay về Trang chủ
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Login;
