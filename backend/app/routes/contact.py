from flask import Blueprint, request, jsonify
from app import db
from app.models.contact import Contact
from flask_cors import cross_origin

contact_bp = Blueprint("contact", __name__)

# Route tạo liên hệ
@contact_bp.route("", methods=["POST", "OPTIONS"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def create_contact():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.get_json()

    try:
        contact = Contact(
            MaTaiKhoan=data.get("maTaiKhoan"),  # đúng với React
            Email=data.get("email"),
            TenNguoiGui=data.get("name"),
            TieuDe=data.get("subject"),
            TinNhan=data.get("message")
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({"message": "Liên hệ đã được gửi thành công."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Route lấy danh sách liên hệ theo tài khoản
@contact_bp.route("/<ma_tai_khoan>", methods=["GET"])
def get_contacts_by_account(ma_tai_khoan):
    try:
        contacts = Contact.query.filter_by(MaTaiKhoan=ma_tai_khoan).all()
        result = []
        for c in contacts:
            result.append({
                "MaContact": c.MaContact,
                "MaTaiKhoan": c.MaTaiKhoan,
                "Email": c.Email,
                "TenNguoiGui": c.TenNguoiGui,
                "TieuDe": c.TieuDe,
                "TinNhan": c.TinNhan
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route cập nhật liên hệ
@contact_bp.route("/<int:ma_contact>", methods=["PUT", "OPTIONS"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def update_contact(ma_contact):
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.get_json()

    try:
        contact = Contact.query.get(ma_contact)

        if not contact:
            return jsonify({"error": "Liên hệ không tồn tại."}), 404

        contact.Email = data.get("email", contact.Email)
        contact.TenNguoiGui = data.get("name", contact.TenNguoiGui)
        contact.TieuDe = data.get("subject", contact.TieuDe)
        contact.TinNhan = data.get("message", contact.TinNhan)

        db.session.commit()
        return jsonify({"message": "Liên hệ đã được cập nhật thành công."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Route xóa liên hệ
@contact_bp.route("/<int:ma_contact>", methods=["DELETE", "OPTIONS"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def delete_contact(ma_contact):
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    try:
        contact = Contact.query.get(ma_contact)

        if not contact:
            return jsonify({"error": "Liên hệ không tồn tại."}), 404

        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message": "Liên hệ đã được xóa thành công."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
# Route lấy tất cả liên hệ với phân trang
@contact_bp.route("/", methods=["GET"])
def get_all_contacts():
    # Lấy thông tin phân trang từ query params
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=6, type=int)

    # Tạo truy vấn cơ bản với mệnh đề ORDER BY
    query = Contact.query.order_by(Contact.MaContact.desc())  # Sắp xếp theo MaContact giảm dần

    # Tổng số bản ghi
    total = query.count()

    # Lấy dữ liệu phân trang
    contacts = query.offset((page - 1) * limit).limit(limit).all()

    # Chuẩn bị dữ liệu trả về
    result = [
        {
            "MaContact": c.MaContact,
            "MaTaiKhoan": c.MaTaiKhoan,
            "Email": c.Email,
            "TenNguoiGui": c.TenNguoiGui,
            "TieuDe": c.TieuDe,
            "TinNhan": c.TinNhan
        } for c in contacts
    ]

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
