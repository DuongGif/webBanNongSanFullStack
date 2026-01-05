from flask import Blueprint, request, jsonify, render_template_string
import paypalrestsdk
import logging
from app.models.cart import Cart
import uuid
from datetime import datetime
from app import db
from app.models.hoa_don import HoaDon
from app.models.chi_tiet_hoa_don import ChiTietHoaDon
from app.models.nong_san import NongSan

payment_bp = Blueprint('payment', __name__)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "AZxeaZAY_I0N79QOxIXOtPSoYTFKnoaO1AgX7VDqQRQoL-PqvKRcUsj7x8xABFHM45Z8F95jr-QeXeRO",
    "client_secret": "EEh4ptGwNJu3iqIkeCRBLPSdFVIeUNhkubgJmrptH9krlnnpimBaKzWLXxEapcDOEzH6gKAqKcL-o3P6"
})

# Sử dụng tỷ giá cố định
FIXED_USD_RATE = 1 / 23500  # 1 VND = ~0.00004255 USD

@payment_bp.route('/api/payment/create', methods=['POST'])
def create_payment():
    data = request.get_json() or {}
    try:
        amount_vnd = float(data.get('amount', 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Số tiền không hợp lệ"}), 400

    ma_tk = data.get('MaTaiKhoan')
    gio_hang = data.get('GioHang', [])
    if amount_vnd <= 0 or not ma_tk or not isinstance(gio_hang, list) or not gio_hang:
        return jsonify({"error": "Thiếu dữ liệu hoặc số tiền không hợp lệ"}), 400

    # Quy đổi sang USD với tỷ giá cố định
    amount_usd = round(amount_vnd * FIXED_USD_RATE, 2)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.host_url.rstrip('/') + "/api/payment/success_callback",
            "cancel_url": request.host_url.rstrip('/') + "/api/payment/cancel"
        },
        "transactions": [ {
            "amount": {
                "total": f"{amount_usd:.2f}",
                "currency": "USD"
            },
            "description": f"Thanh toán đơn hàng {amount_usd:.2f} USD"
        }]
    })

    if not payment.create():
        logging.error(f"PayPal error: {payment.error}")
        return jsonify({"error": "Tạo thanh toán thất bại", "details": payment.error}), 500

    approval_url = next((l.href for l in payment.links if l.rel == 'approval_url'), None)
    return jsonify({"approval_url": approval_url, "amount_usd": amount_usd})


@payment_bp.route('/api/payment/cancel', methods=['GET'])
def payment_cancel():
    return render_template_string("""
        <script>
            if(window.opener) {
                window.opener.postMessage({status:'cancel'}, '*');
                window.close();
            }
        </script>
    """)


@payment_bp.route('/api/payment/success_callback', methods=['GET'])
def payment_success_callback():
    payment_id = request.args.get('paymentId')
    payer_id   = request.args.get('PayerID')
    return render_template_string(f"""
        <script>
            if (window.opener) {{
                window.opener.postMessage({{
                    status: 'success',
                    paymentId: '{payment_id}',
                    PayerID: '{payer_id}'
                }}, '*');
                window.close();
            }}
        </script>
    """)

 
@payment_bp.route('/api/payment/execute', methods=['POST'])
def payment_execute():
    data       = request.get_json() or {}
    payment_id = data.get('paymentId')
    payer_id   = data.get('PayerID')
    ma_tk      = data.get('MaTaiKhoan')
    gio_hang   = data.get('GioHang', [])
    amount_usd = data.get('AmountUSD')

    if not all([payment_id, payer_id, ma_tk, isinstance(gio_hang, list), amount_usd]):
        return jsonify({"error": "Thiếu dữ liệu thanh toán"}), 400

    try:
        amount_usd = float(amount_usd)
    except (ValueError, TypeError):
        return jsonify({"error": "Số tiền không hợp lệ"}), 400

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
    except Exception as e:
        logging.error(f"Không thể tìm payment: {e}")
        return jsonify({"error": "Không tìm thấy giao dịch PayPal"}), 404

    if not payment.execute({"payer_id": payer_id}):
        name = payment.error.get("name", "")
        if name == "PAYMENT_ALREADY_DONE":
            return jsonify({"error": "Giao dịch đã được xử lý trước đó.", "details": payment.error}), 400
        logging.error(f"Execute error: {payment.error}")
        return jsonify({"error": "Thanh toán thất bại", "details": payment.error}), 400

    # Quy đổi lại sang VND với tỷ giá cố định
    amount_vnd = amount_usd

    inv_id = "HD" + uuid.uuid4().hex[:8]
    hd = HoaDon(
        MaHoaDon   = inv_id,
        MaTaiKhoan = ma_tk,
        NgayXuat   = datetime.now(),
        TongTien   = amount_vnd
    )
    db.session.add(hd)
    db.session.flush()

    for item in gio_hang:
        ns = NongSan.query.get(item['MaNongSan'])
        if not ns:
            db.session.rollback()
            return jsonify({"error": f"Nông sản {item['MaNongSan']} không tồn tại"}), 400

        ct = ChiTietHoaDon(
            MaHoaDon  = inv_id,
            MaNongSan = item['MaNongSan'],
            SoLuong   = item.get('SoLuong', 1),
            DonGia    = ns.GiaBan,
            GiamGia   = item.get('GiamGia', 0)
        )
        db.session.add(ct)

    db.session.commit()

    # Xóa giỏ hàng sau khi thanh toán thành công
    try:
        Cart.query.filter_by(MaTaiKhoan=ma_tk).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while clearing cart: {e}")
        return jsonify({"error": "Lỗi khi xóa giỏ hàng"}), 500

    return jsonify({
        "status":   "success",
        "maHoaDon": inv_id,
        "amount":   amount_vnd,
        "currency": "VND"
    })
