from flask import Blueprint, request, jsonify
from app import db
from app.models import review
from app.models.tai_khoan import TaiKhoan  # import model tài khoản

bp = Blueprint("review", __name__)

# GET /api/review/ -> tất cả đánh giá
@bp.route("/", methods=["GET"])
def get_all_reviews():
    data = review.query.all()
    return jsonify([{
        "MaReview": r.MaReview,
        "MaTaiKhoan": r.MaTaiKhoan,
        "Email": r.Email,
        "MaNongSan": r.MaNongSan,
        "NoiDung": r.NoiDung
    } for r in data])

# GET /api/review/<ma_ns> -> đánh giá theo sản phẩm
@bp.route("/<ma_ns>", methods=["GET"])
def get_by_product(ma_ns):
    data = review.query.filter_by(MaNongSan=ma_ns).all()
    return jsonify([{
        "MaReview": r.MaReview,
        "MaTaiKhoan": r.MaTaiKhoan,
        "Email": r.Email,
        "MaNongSan": r.MaNongSan,
        "NoiDung": r.NoiDung
    } for r in data])

# POST /api/review/ -> thêm đánh giá mới
@bp.route("/", methods=["POST"])
def create_review():
    data = request.get_json() or {}
    mk = data.get("MaTaiKhoan")
    mn = data.get("MaNongSan")
    nd = (data.get("NoiDung") or "").strip()
    if not (mk and mn and nd):
        return jsonify({"error": "Missing MaTaiKhoan, MaNongSan or NoiDung"}), 400

    # Lấy email từ request hoặc từ DB
    email = data.get("Email")
    if not email:
        user = TaiKhoan.query.filter_by(MaTaiKhoan=mk).first()
        email = user.Email if user else None

    rv = review(MaTaiKhoan=mk, Email=email, MaNongSan=mn, NoiDung=nd)
    db.session.add(rv)
    db.session.commit()

    return jsonify({
        "MaReview": rv.MaReview,
        "MaTaiKhoan": rv.MaTaiKhoan,
        "Email": rv.Email,
        "MaNongSan": rv.MaNongSan,
        "NoiDung": rv.NoiDung
    }), 200

# PUT /api/review/<review_id> -> cập nhật nội dung đánh giá
@bp.route("/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    data = request.get_json() or {}
    nd = (data.get("NoiDung") or "").strip()
    if not nd:
        return jsonify({"error": "Thiếu nội dung"}), 400
    rv = review.query.get(review_id)
    if not rv:
        return jsonify({"error": "Không tìm thấy đánh giá"}), 404
    rv.NoiDung = nd
    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})


# DELETE /api/review/<review_id> -> xóa đánh giá
@bp.route("/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    rv = review.query.get(review_id)
    if not rv:
        return jsonify({"error": "Không tìm thấy đánh giá"}), 404
    db.session.delete(rv)
    db.session.commit()
    return jsonify({"message": "Xóa thành công"})
