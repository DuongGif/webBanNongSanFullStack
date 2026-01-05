from flask import Blueprint, request, jsonify
from app import db
from app.models import NguonGoc,NongSan
from flask_cors import cross_origin

bp = Blueprint("nguon_goc", __name__)

# Lấy tất cả nguồn gốc
@bp.route("/", methods=["GET"])
def get_all():
    # Lấy danh sách ID nếu có
    ids = request.args.get("ids", default=None, type=str)
    ma_nongsan = request.args.get("ma_nongsan", default=None, type=str)

    # Nếu có tham số ids, bỏ qua phân trang
    if ids:
        id_list = ids.split(",")
        query = NguonGoc.query.filter(NguonGoc.MaNongSan.in_(id_list))
        items = query.all()

        result = []
        for item in items:
            result.append({
                "MaNongSan": item.MaNongSan,
                "KhuVuc": item.KhuVuc,
                "PhuongPhap": item.PhuongPhap
            })

        return jsonify({
            "items": result
        })

    # Trường hợp không có ids: xử lý phân trang + lọc
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=6, type=int)

    query = NguonGoc.query

    if ma_nongsan:
        query = query.filter(NguonGoc.MaNongSan == ma_nongsan)

    query = query.order_by(NguonGoc.MaNongSan)
    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()

    result = []
    for item in items:
        result.append({
            "MaNongSan": item.MaNongSan,
            "KhuVuc": item.KhuVuc,
            "PhuongPhap": item.PhuongPhap
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


# Lấy nguồn gốc theo mã nông sản
@bp.route("/<ma>", methods=["GET"])
def get_by_id(ma):
    item = NguonGoc.query.get(ma)
    if item:
        return jsonify({
            "MaNongSan": item.MaNongSan,
            "KhuVuc": item.KhuVuc,
            "PhuongPhap": item.PhuongPhap
        })
    return jsonify({"error": "Không tìm thấy"}), 404

@bp.route("", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def create():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    ma_nong_san = data.get("MaNongSan")

    # Kiểm tra nếu mã nông sản không tồn tại trong bảng NongSan
    if not NongSan.query.filter_by(MaNongSan=ma_nong_san).first():
        return jsonify({"error": f"Mã nông sản '{ma_nong_san}' không tồn tại trong bảng nông sản"}), 400

    # Kiểm tra nếu mã nông sản đã tồn tại trong bảng NguonGoc
    if NguonGoc.query.filter_by(MaNongSan=ma_nong_san).first():
        return jsonify({"error": f"Mã nông sản '{ma_nong_san}' đã tồn tại trong bảng nguồn gốc"}), 400

    item = NguonGoc(
        MaNongSan=ma_nong_san,
        KhuVuc=data.get("KhuVuc"),
        PhuongPhap=data.get("PhuongPhap")
    )

    try:
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Tạo nguồn gốc thành công"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Lỗi khi tạo nguồn gốc", "details": str(e)}), 500


# Cập nhật
@bp.route("/<ma>", methods=["PUT"])
def update(ma):
    item = NguonGoc.query.get(ma)
    if not item:
        return jsonify({"error": "Không tìm thấy"}), 404
    data = request.get_json()
    item.KhuVuc = data.get("KhuVuc", item.KhuVuc)
    item.PhuongPhap = data.get("PhuongPhap", item.PhuongPhap)
    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})

# Xóa
@bp.route("/<ma>", methods=["DELETE"])
def delete(ma):
    item = NguonGoc.query.get(ma)
    if not item:
        return jsonify({"error": "Không tìm thấy"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Xóa thành công"})
