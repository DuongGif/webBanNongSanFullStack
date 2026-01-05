from flask import Blueprint, request, jsonify
from app import db
# from app.models import AnhNongSan
from flask_cors import cross_origin
from app.models import db, AnhNongSan, NongSan

bp = Blueprint("anh_nong_san", __name__)

# Lấy tất cả ảnh
@bp.route("/", methods=["GET"])
def get_all_anhnongsan_paginated():
    # Lấy danh sách ID nếu có
    ids = request.args.get("ids", default=None, type=str)
    ma_nongsan = request.args.get("ma_nongsan", default=None, type=str)

    # Nếu có tham số ids, bỏ qua phân trang
    if ids:
        id_list = ids.split(",")
        query = AnhNongSan.query.filter(AnhNongSan.MaNongSan.in_(id_list))

        # Sắp xếp đúng theo thứ tự truyền vào nếu cần
        items = query.all()

        result = []
        for item in items:
            result.append({
                "MaNongSan": item.MaNongSan,
                "DuongDanAnh": item.DuongDanAnh
            })

        return jsonify({
            "items": result
        })

    # Trường hợp không có ids: xử lý phân trang + lọc
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=6, type=int)

    query = AnhNongSan.query

    if ma_nongsan:
        query = query.filter(AnhNongSan.MaNongSan == ma_nongsan)

    query = query.order_by(AnhNongSan.MaNongSan)
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()

    result = []
    for item in items:
        result.append({
            "MaNongSan": item.MaNongSan,
            "DuongDanAnh": item.DuongDanAnh
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
    })


# Lấy ảnh theo mã nông sản
@bp.route("/<ma>", methods=["GET"])
def get_by_ma(ma):
    data = AnhNongSan.query.filter_by(MaNongSan=ma).all()
    result = [{
        "MaNongSan": item.MaNongSan,
        "DuongDanAnh": item.DuongDanAnh
    } for item in data]
    return jsonify(result)
  # Đảm bảo import đúng


@bp.route("", methods=["POST", "OPTIONS"])  # 👈 Không có "/"
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def create_anh_nong_san():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    ma_nong_san = data.get("MaNongSan")

    # Kiểm tra nếu mã nông sản không tồn tại trong bảng NongSan
    if not NongSan.query.filter_by(MaNongSan=ma_nong_san).first():
        return jsonify({"error": f"Mã nông sản '{ma_nong_san}' không tồn tại trong bảng nông sản"}), 400

    # Kiểm tra nếu mã nông sản đã tồn tại trong bảng AnhNongSan
    if AnhNongSan.query.filter_by(MaNongSan=ma_nong_san).first():
        return jsonify({"error": f"Mã nông sản '{ma_nong_san}' đã tồn tại trong bảng ảnh"}), 400

    item = AnhNongSan(
        MaNongSan=ma_nong_san,
        DuongDanAnh=data.get("DuongDanAnh")
    )

    try:
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Thêm ảnh thành công"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Lỗi khi thêm ảnh", "details": str(e)}), 500


# Xóa ảnh
@bp.route("/", methods=["DELETE"])
def delete():
    data = request.get_json()
    ma = data.get("MaNongSan")
    duong_dan = data.get("DuongDanAnh")
    item = AnhNongSan.query.get((ma, duong_dan))
    if not item:
        return jsonify({"error": "Không tìm thấy ảnh"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Xóa ảnh thành công"})
