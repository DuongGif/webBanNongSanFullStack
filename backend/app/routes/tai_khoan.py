from flask import Blueprint, jsonify, request
from app.models import TaiKhoan, Cart
from app import db
import traceback
from flask import current_app

bp = Blueprint("tai_khoan", __name__)

# Lấy danh sách tài khoản
@bp.route("/", methods=["GET"])
def get_all_taikhoan():
    users = TaiKhoan.query.all()
    result = []
    for user in users:
        result.append({
            "MaTaiKhoan": user.MaTaiKhoan,
            "HoTen": user.HoTen,
            "DiaChi": user.DiaChi,
            "SoDienThoai": user.SoDienThoai,
            "Email": user.Email,
            "LoaiTaiKhoan": user.LoaiTaiKhoan
        })
    return jsonify(result)

# Tạo tài khoản mới
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

@bp.route("/signup", methods=["POST"])
def create_taikhoan():
    try:
        data = request.get_json()

        # Kiểm tra xem email đã tồn tại chưa
        existing_user = TaiKhoan.query.filter_by(Email=data.get("Email")).first()
        if existing_user:
            return jsonify({"error": "Email đã tồn tại"}), 409

        hashed_password = generate_password_hash(data.get("MatKhau"))
        user = TaiKhoan(
            MaTaiKhoan=data.get("MaTaiKhoan"),
            MatKhau=hashed_password,
            LoaiTaiKhoan=data.get("LoaiTaiKhoan"),
            HoTen=data.get("HoTen"),
            DiaChi=data.get("DiaChi"),
            SoDienThoai=data.get("SoDienThoai"),
            Email=data.get("Email")
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Tạo tài khoản thành công"}), 201  
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Mã tài khoản hoặc email đã tồn tại"}), 409 

# Đăng nhập
from werkzeug.security import check_password_hash
@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Vui lòng nhập đầy đủ email và mật khẩu"}), 400

    user = TaiKhoan.query.filter_by(Email=email).first()

    if not user:
        return jsonify({"error": "Tài khoản không tồn tại"}), 401

    if not check_password_hash(user.MatKhau, password):
        return jsonify({"error": "Mật khẩu không đúng"}), 401

    return jsonify({
        "MaTaiKhoan": user.MaTaiKhoan,
        "LoaiTaiKhoan": user.LoaiTaiKhoan,
        "HoTen": user.HoTen,
        "Email": user.Email
    }), 200

# Lấy tài khoản theo ID
@bp.route("/<ma_tai_khoan>", methods=["GET"])
def get_taikhoan(ma_tai_khoan):
    user = TaiKhoan.query.get(ma_tai_khoan)
    if user:
        return jsonify({
            "MaTaiKhoan": user.MaTaiKhoan,
            "HoTen": user.HoTen,
            "DiaChi": user.DiaChi,
            "SoDienThoai": user.SoDienThoai,
            "Email": user.Email,
            "LoaiTaiKhoan": user.LoaiTaiKhoan
        })
    return jsonify({"error": "Không tìm thấy tài khoản"}), 404

# Cập nhật tài khoản
@bp.route("/<ma_tai_khoan>", methods=["PUT"])
def update_taikhoan(ma_tai_khoan):
    user = TaiKhoan.query.get(ma_tai_khoan)
    if not user:
        return jsonify({"error": "Không tìm thấy tài khoản"}), 404
    
    data = request.get_json()
    if "MatKhau" in data:
        user.MatKhau = generate_password_hash(data["MatKhau"])
    user.LoaiTaiKhoan = data.get("LoaiTaiKhoan", user.LoaiTaiKhoan)
    user.HoTen = data.get("HoTen", user.HoTen)
    user.DiaChi = data.get("DiaChi", user.DiaChi)
    user.SoDienThoai = data.get("SoDienThoai", user.SoDienThoai)
    user.Email = data.get("Email", user.Email)

    db.session.commit()
    return jsonify({"message": "Cập nhật tài khoản thành công"})

@bp.route("/<ma_tai_khoan>", methods=["DELETE"])
def delete_tai_khoan(ma_tai_khoan):
    try:
        # Xóa các bản ghi liên quan trong bảng Cart
        Cart.query.filter_by(MaTaiKhoan=ma_tai_khoan).delete()
        db.session.commit()

        # Sau đó, xóa tài khoản
        tai_khoan = TaiKhoan.query.get(ma_tai_khoan)
        if not tai_khoan:
            return jsonify({"message": "Không tìm thấy tài khoản"}), 404

        db.session.delete(tai_khoan)
        db.session.commit()

        return jsonify({"message": "Đã xóa tài khoản thành công"}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            "error": "Đã xảy ra lỗi khi xóa tài khoản",
            "details": str(e)
        }), 500
