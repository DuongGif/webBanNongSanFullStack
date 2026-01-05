from flask import Blueprint, jsonify, request
from app.models.nong_san import NongSan
from app import db
from flask_cors import cross_origin
from app.models import db, NongSan, LoaiNongSan, NhaCungCap, AnhNongSan, NguonGoc, KhuyenMai, Kho
from collections import OrderedDict
from unidecode import unidecode

bp = Blueprint("nong_san", __name__)

@bp.route("/", methods=["GET"])
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def get_all_nongsan_paginated():
    # Lấy tham số
    search = request.args.get("search", default=None, type=str)
    ids    = request.args.get("ids",     default=None, type=str)
    ma_loai= request.args.get("category",default=None, type=str)
    brand  = request.args.get("brand",   default=None, type=str)
    page   = request.args.get("page",    default=1,    type=int)
    limit  = request.args.get("limit",   default=6,    type=int)

    # 1) Nếu có ids thì bỏ qua phân trang, lọc khác
    if ids:
        id_list = ids.split(",")
        items = NongSan.query.filter(NongSan.MaNongSan.in_(id_list)).all()

        result = []
        for ns in items:
            result.append({
                "MaNongSan": ns.MaNongSan,
                "TenNongSan": ns.TenNongSan,
                "MaLoai": ns.MaLoai,
                "GiaBan": float(ns.GiaBan) if ns.GiaBan else None,
                "SoLuongTonKho": ns.SoLuongTonKho,
                "DonViTinh": ns.DonViTinh,
                "MaNhaCungCap": ns.MaNhaCungCap,
                "TenNhaCungCap": ns.nhacungcap.TenNhaCungCap if ns.nhacungcap else None,
                "DuongDanAnh": ns.DuongDanAnh
            })
        return jsonify({"items": result})

    # 2) Build query cơ bản
    query = NongSan.query
    if ma_loai:
        query = query.filter(NongSan.MaLoai == ma_loai)
    if brand:
        query = query.filter(NongSan.MaNhaCungCap == brand)

    # 3) Nếu có search: phải fetch all, normalize rồi lọc thủ công
    if search:
        # normalize từ khóa: bỏ khoảng trắng, chuyển không dấu, viết thường
        key = unidecode(search.strip().lower().replace(" ", ""))

        # fetch all đã lọc theo category & brand
        all_items = query.all()
        filtered = []
        for ns in all_items:
            name_norm = unidecode(ns.TenNongSan.lower().replace(" ", ""))
            if key in name_norm:
                filtered.append(ns)

        total = len(filtered)
        # phân trang trên list Python
        start = (page - 1) * limit
        end   = page * limit
        page_items = filtered[start:end]
    else:
        # nếu không search thì tận dụng SQL để phân trang
        query = query.order_by(NongSan.MaNongSan)
        total = query.count()
        page_items = query.offset((page - 1) * limit).limit(limit).all()

    # 4) Chuẩn bị kết quả
    result = []
    for ns in page_items:
        result.append(OrderedDict({
            "MaNongSan": ns.MaNongSan,
            "TenNongSan": ns.TenNongSan,
            "MaLoai": ns.MaLoai,
            "GiaBan": float(ns.GiaBan) if ns.GiaBan else None,
            "SoLuongTonKho": ns.SoLuongTonKho,
            "DonViTinh": ns.DonViTinh,
            "MaNhaCungCap": ns.MaNhaCungCap,
            "TenNhaCungCap": ns.nhacungcap.TenNhaCungCap if ns.nhacungcap else None,
            "DuongDanAnh": ns.DuongDanAnh
        }))

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


@bp.route("/<string:id>", methods=["GET"])
def get_nong_san_by_id(id):
    ns = NongSan.query.get(id)
    if not ns:
        return jsonify({"error": "Không tìm thấy nông sản"}), 404

    result = {
        "MaNongSan": ns.MaNongSan,
        "TenNongSan": ns.TenNongSan,
        "MaLoai": ns.MaLoai,
        "GiaBan": float(ns.GiaBan) if ns.GiaBan else None,
        "SoLuongTonKho": ns.SoLuongTonKho,
        "DonViTinh": ns.DonViTinh,
        "MaNhaCungCap": ns.MaNhaCungCap,
        "TenNhaCungCap": ns.nhacungcap.TenNhaCungCap if ns.nhacungcap else None,
        "DuongDanAnh": ns.DuongDanAnh
    }

    return jsonify(result)


@bp.route("", methods=["POST", "OPTIONS"])  # 👈 Không có "/"
@cross_origin(origins=["http://localhost:3000", "http://127.0.0.1:3000"], supports_credentials=True)
def create_nong_san():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    ma_nong_san = data.get("MaNongSan")
    ma_loai = data.get("MaLoai")
    ma_ncc = data.get("MaNhaCungCap")

    # 1. Kiểm tra mã nông sản đã tồn tại chưa
    if NongSan.query.filter_by(MaNongSan=ma_nong_san).first():
        return jsonify({"error": f"Mã nông sản '{ma_nong_san}' đã tồn tại"}), 400

    # 2. Kiểm tra mã loại nông sản
    loai_nong_san = LoaiNongSan.query.filter_by(MaLoai=ma_loai).first()
    if not loai_nong_san:
        return jsonify({"error": f"Loại nông sản với mã '{ma_loai}' không tồn tại"}), 400

    # 3. Kiểm tra mã nhà cung cấp
    nha_cung_cap = NhaCungCap.query.filter_by(MaNhaCungCap=ma_ncc).first()
    if not nha_cung_cap:
        return jsonify({"error": f"Nhà cung cấp với mã '{ma_ncc}' không tồn tại"}), 400

    try:
        ns = NongSan(
            MaNongSan=ma_nong_san,
            TenNongSan=data.get("TenNongSan"),
            MaLoai=ma_loai,
            GiaBan=data.get("GiaBan"),
            SoLuongTonKho=data.get("SoLuongTonKho"),
            DonViTinh=data.get("DonViTinh"),
            MaNhaCungCap=ma_ncc,
            DuongDanAnh=data.get("DuongDanAnh")
        )
        db.session.add(ns)
        db.session.commit()
        return jsonify({"message": "Tạo nông sản thành công"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Lỗi khi tạo nông sản", "details": str(e)}), 500



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
    try:
        # Tìm nông sản theo mã
        ns = NongSan.query.get(id)
        if not ns:
            return jsonify({"error": "Không tìm thấy nông sản"}), 404

        # Xóa các bản ghi liên quan
        AnhNongSan.query.filter_by(MaNongSan=id).delete()
        NguonGoc.query.filter_by(MaNongSan=id).delete()
        KhuyenMai.query.filter_by(MaNongSan=id).delete()
        Kho.query.filter_by(MaNongSan=id).delete()

        # Xóa nông sản
        db.session.delete(ns)
        db.session.commit()

        return jsonify({"message": "Xóa nông sản và các bản ghi liên quan thành công"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Đã xảy ra lỗi trong quá trình xóa",
            "details": str(e)
        }), 500

