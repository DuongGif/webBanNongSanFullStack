from flask import Blueprint, request, jsonify
from flask_mail import Message
import random
from app import mail


bp = Blueprint('otp', __name__)
otp_store = {}

@bp.route("/sendotp", methods=["POST"])
def send_otp():
    email = request.json.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    otp = random.randint(100000, 999999)
    otp_store[email] = otp

    try:
        subject = "Mã OTP đăng ký tài khoản"
        sender_name = "Nông sản Xanh"
        sender_email = "phamtrunghieu201004@gmail.com"
        body = f"""
        Xin chào,

        Cảm ơn bạn đã đăng ký tài khoản tại Nông sản Xanh.

        Mã OTP của bạn là: {otp}

        Vui lòng không chia sẻ mã này với người khác. Mã OTP có hiệu lực trong 5 phút.

        Trân trọng,
        Đội ngũ hỗ trợ Nông sản Xanh
        """

        msg = Message(subject=subject,
                      sender=(sender_name, sender_email),
                      recipients=[email])
        msg.body = body
        mail.send(msg)

        return jsonify({"message": "OTP sent successfully to your email!"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send OTP: {str(e)}"}), 500

@bp.route("/verifyotp", methods=["POST"])
def verify_otp():
    email = request.json.get("email")
    otp_sent = otp_store.get(email)
    if not otp_sent:
        return jsonify({"error": "OTP not found or expired"}), 404

    otp_received = request.json.get("otp_received")
    if not otp_received or otp_sent != int(otp_received):
        return jsonify({"error": "Invalid OTP"}), 400

    del otp_store[email]
    return jsonify({"message": "OTP verified successfully!"}), 200
