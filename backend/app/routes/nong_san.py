from flask import Blueprint, jsonify, request
from app.models.nong_san import NongSan
from app import db

bp = Blueprint("nong_san", __name__)

# ✅ Lấy danh sách nông sản với phân trang
@bp.route("/", methods=["GET"])
def get_all_nongsan_paginated():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=6, type=int)

    query = NongSan.query.order_by(NongSan.MaNongSan)
    total = query.count()

    nongsan = query.offset((page - 1) * limit).limit(limit).all()
    result = []
    for ns in nongsan:
        result.append({
            "MaNongSan": ns.MaNongSan,
            "TenNongSan": ns.TenNongSan,
            "MaLoai": ns.MaLoai,
            "GiaBan": float(ns.GiaBan) if ns.GiaBan else None,
            "SoLuongTonKho": ns.SoLuongTonKho,
            "DonViTinh": ns.DonViTinh,
            "MaNhaCungCap": ns.MaNhaCungCap,
            "DuongDanAnh": ns.DuongDanAnh
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

# ✅ Tạo nông sản mới
@bp.route("/", methods=["POST"])
def create_nong_san():
    data = request.get_json()
    ns = NongSan(
        MaNongSan=data.get("MaNongSan"),
        TenNongSan=data.get("TenNongSan"),
        MaLoai=data.get("MaLoai"),
        GiaBan=data.get("GiaBan"),
        SoLuongTonKho=data.get("SoLuongTonKho"),
        DonViTinh=data.get("DonViTinh"),
        MaNhaCungCap=data.get("MaNhaCungCap"),
        DuongDanAnh=data.get("DuongDanAnh")
    )
    db.session.add(ns)
    db.session.commit()
    return jsonify({"message": "Tạo nông sản thành công"}), 201

# ✅ Cập nhật nông sản
@bp.route("/<id>", methods=["PUT"])
def update_nong_san(id):
    ns = NongSan.query.get(id)
    if not ns:
        return jsonify({"error": "Không tìm thấy nông sản"}), 404

    data = request.get_json()
    ns.TenNongSan = data.get("TenNongSan", ns.TenNongSan)
    ns.MaLoai = data.get("MaLoai", ns.MaLoai)
    ns.GiaBan = data.get("GiaBan", ns.GiaBan)
    ns.SoLuongTonKho = data.get("SoLuongTonKho", ns.SoLuongTonKho)
    ns.DonViTinh = data.get("DonViTinh", ns.DonViTinh)
    ns.MaNhaCungCap = data.get("MaNhaCungCap", ns.MaNhaCungCap)
    ns.DuongDanAnh = data.get("DuongDanAnh", ns.DuongDanAnh)

    db.session.commit()
    return jsonify({"message": "Cập nhật nông sản thành công"})

# ✅ Xóa nông sản
@bp.route("/<id>", methods=["DELETE"])
def delete_nong_san(id):
    ns = NongSan.query.get(id)
    if not ns:
        return jsonify({"error": "Không tìm thấy nông sản"}), 404

    db.session.delete(ns)
    db.session.commit()
    return jsonify({"message": "Xóa nông sản thành công"})
