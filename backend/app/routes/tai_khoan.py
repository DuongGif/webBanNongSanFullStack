from flask import Blueprint, jsonify, request
from app.models import TaiKhoan
from app import db

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
@bp.route("/", methods=["POST"])
def create_taikhoan():
    data = request.get_json()
    user = TaiKhoan(
        MaTaiKhoan=data.get("MaTaiKhoan"),
        MatKhau=data.get("MatKhau"),
        LoaiTaiKhoan=data.get("LoaiTaiKhoan"),
        HoTen=data.get("HoTen"),
        DiaChi=data.get("DiaChi"),
        SoDienThoai=data.get("SoDienThoai"),
        Email=data.get("Email")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Tạo tài khoản thành công"}), 201
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
    user.MatKhau = data.get("MatKhau", user.MatKhau)
    user.LoaiTaiKhoan = data.get("LoaiTaiKhoan", user.LoaiTaiKhoan)
    user.HoTen = data.get("HoTen", user.HoTen)
    user.DiaChi = data.get("DiaChi", user.DiaChi)
    user.SoDienThoai = data.get("SoDienThoai", user.SoDienThoai)
    user.Email = data.get("Email", user.Email)

    db.session.commit()
    return jsonify({"message": "Cập nhật tài khoản thành công"})

# Xóa tài khoản
@bp.route("/<ma_tai_khoan>", methods=["DELETE"])
def delete_taikhoan(ma_tai_khoan):
    user = TaiKhoan.query.get(ma_tai_khoan)
    if not user:
        return jsonify({"error": "Không tìm thấy tài khoản"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Xóa tài khoản thành công"})
