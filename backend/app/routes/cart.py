from flask import Blueprint, request, jsonify, current_app
from app.models import Cart, TaiKhoan
import traceback
from app import db
import requests
cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/", methods=["GET"])
def get_all_carts():
    try:
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=6, type=int)

        query = Cart.query.order_by(Cart.MaTaiKhoan, Cart.MaNongSan)
        total = query.count()
        carts = query.offset((page - 1) * limit).limit(limit).all()

        if not carts:
            return jsonify({"message": "Không có giỏ hàng nào trong hệ thống"}), 404

        result = []
        for item in carts:
            result.append({
                "MaTaiKhoan": item.MaTaiKhoan,
                "MaNongSan": item.MaNongSan,
                "SoLuong": item.SoLuong,
                "GiamGia": float(item.GiamGia) if item.GiamGia else None,
                "PhiShip": float(item.PhiShip) if item.PhiShip else None
            })

        return jsonify({
            "items": result,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "pages": (total + limit - 1) // limit,
                "has_next": page * limit < total,
                "has_prev": page > 1
            }
        }), 200
    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error(tb)
        return jsonify({
            "message": "Lỗi khi lấy danh sách giỏ hàng",
            "error": str(e),
            "trace": tb
        }), 500


# 1. Lấy giỏ hàng của 1 tài khoản
@cart_bp.route("/<ma_tai_khoan>", methods=["GET"])
def get_cart(ma_tai_khoan):
    try:
        account = TaiKhoan.query.filter_by(MaTaiKhoan=ma_tai_khoan).first()
        if not account:
            return jsonify({"message": "Tài khoản không tồn tại"}), 404
        
        items = Cart.query.filter_by(MaTaiKhoan=ma_tai_khoan).all()
        
        # ✅ Trả luôn mảng (rỗng nếu không có)
        result = [{
            "MaTaiKhoan": item.MaTaiKhoan,
            "MaNongSan": item.MaNongSan,
            "SoLuong": item.SoLuong,
            "GiamGia": item.GiamGia,
            "PhiShip": item.PhiShip
        } for item in items]

        return jsonify(result), 200
    except Exception as e:
        tb = traceback.format_exc()
        current_app.logger.error(tb)
        return jsonify({
            "message": "Lỗi khi lấy giỏ hàng",
            "error": str(e),
            "trace": tb
        }), 500



# 2. Thêm sản phẩm vào giỏ
@cart_bp.route("/", methods=["POST"])
def add_to_cart():
    try:
        data = request.json
        ma_tk = data.get("MaTaiKhoan")
        ma_ns = data.get("MaNongSan")
        so_luong = data.get("SoLuong", 1)
        giam_gia = data.get("GiamGia", 0)
        phi_ship = data.get("PhiShip", 0)

        if not ma_tk or not ma_ns:
            return jsonify({"message": "MaTaiKhoan và MaNongSan là bắt buộc"}), 400
        if so_luong <= 0:
            return jsonify({"message": "Số lượng phải lớn hơn 0"}), 400

        account = TaiKhoan.query.filter_by(MaTaiKhoan=ma_tk).first()
        if not account:
            return jsonify({"message": "Tài khoản không tồn tại"}), 404
        
        existing = Cart.query.filter_by(MaTaiKhoan=ma_tk, MaNongSan=ma_ns).first()
        if existing:
            existing.SoLuong += so_luong
        else:
            new_item = Cart(
                MaTaiKhoan=ma_tk,
                MaNongSan=ma_ns,
                SoLuong=so_luong,
                GiamGia=giam_gia,
                PhiShip=phi_ship
            )
            db.session.add(new_item)

        db.session.commit()
        return jsonify({"message": "Đã thêm vào giỏ hàng"}), 201
    except Exception as e:
        db.session.rollback()
        tb = traceback.format_exc()
        current_app.logger.error(tb)
        return jsonify({
            "message": "Lỗi khi thêm vào giỏ hàng",
            "error": str(e),
            "trace": tb
        }), 500


# 3. Cập nhật sản phẩm trong giỏ
@cart_bp.route("/<ma_tai_khoan>/<ma_nong_san>", methods=["PUT"])
def update_cart_item(ma_tai_khoan, ma_nong_san):
    try:
        data = request.json

        # Không cần lấy lại ma_tk, ma_ns từ data nữa vì đã có trong URL
        account = TaiKhoan.query.filter_by(MaTaiKhoan=ma_tai_khoan).first()
        if not account:
            return jsonify({"message": "Tài khoản không tồn tại"}), 404

        item = Cart.query.filter_by(MaTaiKhoan=ma_tai_khoan, MaNongSan=ma_nong_san).first()
        if not item:
            return jsonify({"message": "Không tìm thấy sản phẩm trong giỏ"}), 404

        # Cập nhật số lượng và kiểm tra giá trị hợp lệ
        new_so_luong = data.get("SoLuong", item.SoLuong)
        if new_so_luong <= 0:
            return jsonify({"message": "Số lượng phải lớn hơn 0"}), 400

        item.SoLuong = new_so_luong
        item.GiamGia = data.get("GiamGia", item.GiamGia)
        item.PhiShip = data.get("PhiShip", item.PhiShip)

        db.session.commit()
        return jsonify({"message": "Cập nhật thành công"}), 200
    except Exception as e:
        db.session.rollback()
        tb = traceback.format_exc()
        current_app.logger.error(tb)
        return jsonify({
            "message": "Lỗi khi cập nhật giỏ hàng",
            "error": str(e),
            "trace": tb
        }), 500


@cart_bp.route("/<ma_tai_khoan>/<ma_nong_san>", methods=["DELETE"])
def delete_cart_item(ma_tai_khoan, ma_nong_san):
    try:
        item = Cart.query.filter_by(
            MaTaiKhoan=ma_tai_khoan,
            MaNongSan=ma_nong_san
        ).first()

        if not item:
            return jsonify({"error": "Không tìm thấy sản phẩm"}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "Đã xóa sản phẩm khỏi giỏ thành công"}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error("Lỗi khi xóa sản phẩm khỏi giỏ hàng: %s", traceback.format_exc())
        return jsonify({
            "error": "Đã xảy ra lỗi khi xóa sản phẩm",
            "details": str(e)
        }), 500



@cart_bp.route("/tinh-phi-ship", methods=["GET"])
def tinh_phi_ship():
    try:
        lat1 = request.args.get("lat1", type=float)
        lng1 = request.args.get("lng1", type=float)
        lat2 = request.args.get("lat2", type=float)
        lng2 = request.args.get("lng2", type=float)

        if None in [lat1, lng1, lat2, lng2]:
            return jsonify({"message": "Thiếu tọa độ"}), 400

        # Gọi GraphHopper API
        api_key = "2e9caa5a-434b-4b5e-a93c-dac2fbbeea9e"
        url = (
            f"https://graphhopper.com/api/1/route?"
            f"point={lat1},{lng1}&point={lat2},{lng2}"
            f"&vehicle=car&locale=vi&calc_points=false&key={api_key}"
        )
        res = requests.get(url)
        data = res.json()

        if "paths" not in data:
            return jsonify({"message": "Không thể tính khoảng cách", "api_response": data}), 500

        distance_m = data['paths'][0]['distance']
        distance_km = distance_m / 1000

        # Tính phí ship theo khoảng cách
        if distance_km <= 5:
            phi_ship = 0
        elif distance_km <= 10:
            phi_ship = distance_km * 3000
        else:
            phi_ship = distance_km * 2000

        return jsonify({
            "distance_km": round(distance_km, 2),
            "phi_ship": round(phi_ship)
        }), 200
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            "message": "Lỗi khi tính phí ship",
            "error": str(e)
        }), 500
