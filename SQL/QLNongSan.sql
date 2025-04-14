CREATE DATABASE QLNongSan_Api;
GO
USE QLNongSan_Api;

CREATE TABLE LoaiNongSan (
    MaLoai VARCHAR(10) PRIMARY KEY,
    TenLoai NVARCHAR(50)
);

CREATE TABLE NhaCungCap (
    MaNhaCungCap VARCHAR(10) PRIMARY KEY,
    TenNhaCungCap NVARCHAR(100),
    DiaChi NVARCHAR(255),
    SoDienThoai VARCHAR(15)
);
INSERT INTO NhaCungCap (MaNhaCungCap, TenNhaCungCap, DiaChi, SoDienThoai)
VALUES
    ('NCC01', 'Cong ty TNHH Nong san ABC', '123 Duong A, Quan 1', '0901234567'),
    ('NCC02', 'Hop tac xa Nong san XYZ', '456 Duong B, Quan 2', '0902345678'),
    ('NCC03', 'Công ty TNHH Thực phẩm Fresh', '789 Đường C, Quận 3', '0903456789'),
    ('NCC04', 'Hợp tác xã Rau quả An Toàn', '321 Đường D, Quận 4', '0904567890'),
	('NCC05', 'Công ty TNHH Thực phẩm XYZ', '789 Đường C, Quận 3', '0903456789');

-- Tạo bảng NongSan với cột DuongDanAnh
CREATE TABLE NongSan (
    MaNongSan VARCHAR(10) PRIMARY KEY,
    TenNongSan NVARCHAR(255) NOT NULL,
    MaLoai VARCHAR(10),
    GiaBan DECIMAL(18, 2),
    SoLuongTonKho INT,
    DonViTinh NVARCHAR(50),
    MaNhaCungCap VARCHAR(10),
    DuongDanAnh VARCHAR(255),
    FOREIGN KEY (MaLoai) REFERENCES LoaiNongSan(MaLoai),
    FOREIGN KEY (MaNhaCungCap) REFERENCES NhaCungCap(MaNhaCungCap)
);

CREATE TABLE AnhNongSan (
    MaNongSan VARCHAR(10) NOT NULL,
    DuongDanAnh VARCHAR(255) NOT NULL,
    PRIMARY KEY (MaNongSan, DuongDanAnh),
    FOREIGN KEY (MaNongSan) REFERENCES NongSan(MaNongSan) ON DELETE CASCADE
);

CREATE TABLE NguonGoc (
    MaNongSan VARCHAR(10),
    KhuVuc VARCHAR(100),
    PhuongPhap VARCHAR(100),
    PRIMARY KEY (MaNongSan),
    FOREIGN KEY (MaNongSan) REFERENCES NongSan(MaNongSan)
);

CREATE TABLE KhuyenMai (
    MaKhuyenMai VARCHAR(10),
    MaNongSan VARCHAR(10),
    MoTa VARCHAR(255),
    NgayBatDau DATE,
    NgayKetThuc DATE,
    PRIMARY KEY (MaKhuyenMai),
    FOREIGN KEY (MaNongSan) REFERENCES NongSan(MaNongSan)
);

CREATE TABLE Kho (
    MaNongSan VARCHAR(10),
    SoLuongTonKho INT,
    NgayCapNhat DATE,
    PRIMARY KEY (MaNongSan),
    FOREIGN KEY (MaNongSan) REFERENCES NongSan(MaNongSan)
);

CREATE TABLE TaiKhoan (
    MaTaiKhoan NVARCHAR(10) PRIMARY KEY,
    MatKhau NVARCHAR(50) NOT NULL,
    LoaiTaiKhoan NVARCHAR(10) NOT NULL CHECK (LoaiTaiKhoan IN ('Khach', 'Admin')),
    HoTen NVARCHAR(100) NOT NULL,
    DiaChi NVARCHAR(200),
    SoDienThoai NVARCHAR(20),
    Email NVARCHAR(100)
);

-- Bảng HoaDon tạo trước vì được tham chiếu bởi ChiTietHoaDon
CREATE TABLE HoaDon (
    MaHoaDon NVARCHAR(10) PRIMARY KEY,
    NgayXuat DATE NOT NULL,
    TongTien MONEY NOT NULL,
    MaTaiKhoan NVARCHAR(10) NOT NULL,
    FOREIGN KEY (MaTaiKhoan) REFERENCES TaiKhoan(MaTaiKhoan)
);

CREATE TABLE ChiTietHoaDon (
    MaHoaDon NVARCHAR(10),
    MaNongSan NVARCHAR(10),
    SoLuong INT NOT NULL CHECK (SoLuong > 0),
    DonGia MONEY NOT NULL CHECK (DonGia >= 0),
    GiamGia INT DEFAULT 0 CHECK (GiamGia >= 0 AND GiamGia <= 100),
    PRIMARY KEY (MaHoaDon, MaNongSan),
    FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
    FOREIGN KEY (MaNongSan) REFERENCES NongSan(MaNongSan)
);

INSERT INTO Kho (MaNongSan, SoLuongTonKho, NgayCapNhat) VALUES
('1', 100, '2024-10-11'),
('2', 50, '2024-10-11'),
('3', 80, '2024-10-11'),
('4', 75, '2024-10-11'),
('5', 60, '2024-10-11'),
('6', 90, '2024-10-11'),
('7', 45, '2024-10-11'),
('8', 50, '2024-10-11'),
('9', 30, '2024-10-11'),
('10', 85, '2024-10-11'),
('11', 100, '2024-10-11'),
('12', 70, '2024-10-11'),
('13', 40, '2024-10-11'),
('14', 65, '2024-10-11'),
('15', 25, '2024-10-11'),
('16', 80, '2024-10-11'),
('17', 55, '2024-10-11'),
('18', 65, '2024-10-11'),
('19', 100, '2024-10-11'),
('20', 90, '2024-10-11');



INSERT INTO KhuyenMai (MaKhuyenMai, MaNongSan, MoTa, NgayBatDau, NgayKetThuc) VALUES
    ('KM01', '1', 'Giam gia 10%', '2024-10-01', '2024-10-15'),
    ('KM02', '2', 'Mua 1 tang 1', '2024-10-05', '2024-10-20'),
    ('KM03', '3', 'Giam gia 15%', '2024-10-10', '2024-10-25'),
    ('KM04', '4', 'Giam gia 5% cho khach hang than thiet', '2024-10-01', '2024-10-30'),
    ('KM05', '5', 'Giam gia 20% cho don hang tren 500000 VND', '2024-10-01', '2024-10-31'),
    ('KM06', '6', 'Giam gia 10% cho khach hang moi', '2024-10-01', '2024-10-10'),
    ('KM07', '7', 'Giam gia 30% cho mua he', '2024-10-01', '2024-10-31'),
    ('KM08', '8', 'Giam gia 5% cho don hang online', '2024-10-05', '2024-10-15'),
    ('KM09', '9', 'Mua 2 tang 1', '2024-10-10', '2024-10-20'),
    ('KM10', '10', 'Giam gia 15% cho sinh vien', '2024-10-01', '2024-10-30'),
    ('KM11', '11', 'Giam gia 20% vao cuoi tuan', '2024-10-01', '2024-10-15'),
    ('KM12', '12', 'Khach hang mua hang dau tien duoc giam gia 10%', '2024-10-01', '2024-10-15'),
    ('KM13', '13', 'Giam gia 25% cho cac san pham chon loc', '2024-10-05', '2024-10-25'),
    ('KM14', '14', 'Giam gia 10% cho khach hang dat hang truoc', '2024-10-01', '2024-10-31'),
    ('KM15', '15', 'Giam gia 5% cho don hang tu 300000 VND', '2024-10-01', '2024-10-20'),
    ('KM16', '16', 'Giam gia 15% cho khach hang mua theo nhom', '2024-10-01', '2024-10-15'),
    ('KM17', '17', 'Mua 3 tang 1', '2024-10-10', '2024-10-20'),
    ('KM18', '18', 'Giam gia 10% cho don hang tu 500000 VND', '2024-10-01', '2024-10-30'),
    ('KM19', '19', 'Giam gia 20% cho lan mua thu 2', '2024-10-01', '2024-10-31'),
    ('KM20', '20', 'Giam gia 15% cho cac san pham tuoi song', '2024-10-01', '2024-10-15');

	INSERT INTO NguonGoc (MaNongSan, KhuVuc, PhuongPhap) VALUES
    ('1', 'Dong Nai', 'Canh tac huu co'),
    ('2', 'Lam Dong', 'Canh tac truyen thong'),
    ('3', 'Tien Giang', 'Canh tac hon hop'),
    ('4', 'Ha Noi', 'Canh tac huu co'),
    ('5', 'Ninh Thuan', 'Canh tac tu nhien'),
    ('6', 'Bac Ninh', 'Canh tac thong minh'),
    ('7', 'Hai Duong', 'Canh tac truyen thong'),
    ('8', 'An Giang', 'Canh tac huu co'),
    ('9', 'Vinh Long', 'Canh tac tu nhien'),
    ('10', 'Binh Thuan', 'Canh tac hon hop'),
    ('11', 'Long An', 'Canh tac thong minh'),
    ('12', 'Ha Giang', 'Canh tac huu co'),
    ('13', 'Dak Lak', 'Canh tac truyen thong'),
    ('14', 'Quang Nam', 'Canh tac tu nhien'),
    ('15', 'Nghe An', 'Canh tac hon hop'),
    ('16', 'Thua Thien Hue', 'Canh tac thong minh'),
    ('17', 'Kien Giang', 'Canh tac huu co'),
    ('18', 'Ca Mau', 'Canh tac truyen thong'),
    ('19', 'Soc Trang', 'Canh tac hon hop'),
    ('20', 'Ben Tre', 'Canh tac tu nhien');
	
	INSERT INTO AnhNongSan (MaNongSan, DuongDanAnh) VALUES
('1', 'cachua.jpeg'),
('2', 'carot.jpeg'),
('3', 'duahau.jpeg'),
('4', 'bido.jpeg'),
('5', 'carotvang.jpeg'),
('6', 'xoakeo.jpeg'),
('7', 'raungot.jpeg'),
('8', 'khoaitaytim.jpeg'),
('9', 'nhoxanh.jpeg'),
('10', 'muopdang.jpeg'),
('11', 'cucaitrang.jpeg'),
('12', 'dudud.jpeg'),
('13', 'rauden.jpeg'),
('14', 'khoailangvang.jpeg'),
('15', 'vaithieu.jpeg'),
('16', 'cachuabi.jpeg'),
('17', 'hanhtim.jpeg'),
('18', 'quabuoi.jpeg'),
('19', 'raumuong.jpeg'),
('20', 'rauxalach.jpeg'),
('21', 'bixanh.jpeg'),
('22', 'quat ao.jpeg'),
('23', 'bapcai.jpeg'),
('24', 'cuahanh.jpeg'),
('25', 'catim.jpeg'),
('26', 'raumuongxao.jpeg'),
('27', 'rauxanh.jpeg'),
('28', 'raungot.jpeg'),
('29', 'raudiep.jpeg'),
('30', 'rauxalach.jpeg'),
('31', 'dudu.jpeg'),
('32', 'buoi.jpeg'),
('33', 'dua.jpeg'),
('34', 'nho.jpeg'),
('35', 'quyt.jpeg'),
('36', 'gung.jpeg'),
('37', 'toi.jpeg'),
('38', 'tieu.jpeg'),
('39', 'hanh.jpeg'),
('40', 'muoi.jpeg'),
('41', 'gao.jpeg'),
('42', 'ngo.jpeg'),
('43', 'khoaimi.jpeg'),
('44', 'botmi.jpeg'),
('45', 'banhmi.jpeg'),
('46', 'thitheo.jpeg'),
('47', 'thitbo.jpeg'),
('48', 'thitga.jpeg'),
('49', 'tom.jpeg'),
('50', 'cahoi.jpeg'),
('51', 'thitvit.jpeg'),
('52', 'banhchung.jpeg'),
('53', 'dauxanh.jpeg'),
('54', 'dauden.jpeg'),
('55', 'bapngo.jpeg'),
('56', 'thitcuu.jpeg'),
('57', 'chaluat.jpeg'),
('58', 'thitgacongnghiep.jpeg'),
('59', 'thitbotuoi.jpeg'),
('60', 'sodiep.jpeg');



INSERT INTO NongSan (MaNongSan, TenNongSan, MaLoai, GiaBan, SoLuongTonKho, DonViTinh, MaNhaCungCap, DuongDanAnh)
VALUES
    ('1', 'Ca chua', '01', 20000, 100, 'kg', 'NCC01', 'cachua.jpeg'), 
    ('2', 'Ca rot', '02', 15000, 50, 'kg', 'NCC01', 'carot.jpeg'),
    ('3', 'Dua hau', '03', 30000, 80, 'kg', 'NCC02', 'duahau.jpeg'),
    ('4', 'Bi do', '01', 26000, 75, 'kg', 'NCC01', 'bido.jpeg'),
    ('5', 'Ca rot vang', '02', 15000, 60, 'kg', 'NCC01', 'carotvang.jpeg'),
    ('6', 'Xoai keo', '03', 30000, 90, 'kg', 'NCC02', 'xoaikeo.jpeg'),
    ('7', 'Rau ngot', '01', 22000, 45, 'kg', 'NCC01', 'raungot.jpeg'),
    ('8', 'Khoai tay tim', '02', 28000, 50, 'kg', 'NCC01', 'khoaitaytim.jpeg'),
    ('9', 'Nho xanh', '03', 55000, 30, 'kg', 'NCC02', 'nhoxanh.jpeg'),
    ('10', 'Muop dang', '01', 15000, 85, 'kg', 'NCC01', 'muopdang.jpeg'),
    ('11', 'Cu cai trang', '02', 12000, 100, 'kg', 'NCC01', 'cucaitrang.jpeg'),
    ('12', 'Du du', '03', 20000, 70, 'kg', 'NCC02', 'dudu.jpeg'),
    ('13', 'Rau den', '01', 17000, 40, 'kg', 'NCC01', 'rauden.jpeg'),
    ('14', 'Khoai lang vang', '02', 18000, 65, 'kg', 'NCC01', 'khoailangvang.jpeg'),
    ('15', 'Vai thieu', '03', 60000, 25, 'kg', 'NCC02', 'vaithieu.jpeg'),
    ('16', 'Ca chua bi', '01', 30000, 80, 'kg', 'NCC01', 'cachuabi.jpeg'),
    ('17', 'Hanh tim', '02', 25000, 55, 'kg', 'NCC01', 'hanhtim.jpeg'),
    ('18', 'Qua buoi', '03', 35000, 65, 'kg', 'NCC02', 'quabuoi.jpeg'),
    ('19', 'Rau muong', '01', 12000, 100, 'kg', 'NCC01', 'raumuong.jpeg'),
    ('20', 'Rau xa lach', '01', 18000, 90, 'kg', 'NCC01', 'rauxalach.jpeg'),
    ('21', 'Bi xanh', '01', 20000, 75, 'kg', 'NCC01', 'bixanh.jpeg'),
    ('22', 'Qua tao', '03', 45000, 60, 'kg', 'NCC02', 'quatao.jpeg'),
    ('23', 'Bap cai', '01', 22000, 85, 'kg', 'NCC01', 'bapcai.jpeg'),
    ('24', 'Cu hanh', '02', 15000, 95, 'kg', 'NCC01', 'cuhanh.jpeg'),
    ('25', 'Ca tim', '01', 17000, 55, 'kg', 'NCC01', 'catim.jpeg'),
    ('26', 'Rau muong xao', '01', 12000, 80, 'kg', 'NCC01', 'raumuongxao.jpeg'),
    ('27', 'Rau xanh', '01', 15000, 90, 'kg', 'NCC01', 'rauxanh.jpeg'),
    ('28', 'Rau ngot', '01', 22000, 70, 'kg', 'NCC01', 'raungot.jpeg'),
    ('29', 'Rau diep', '01', 18000, 100, 'kg', 'NCC01', 'raudiep.jpeg'),
    ('30', 'Rau xa lach', '01', 16000, 50, 'kg', 'NCC01', 'rauxalach.jpeg'),
    ('31', 'Du du', '02', 25000, 60, 'kg', 'NCC02', 'dudu.jpeg'),
    ('32', 'Buoi', '02', 30000, 40, 'kg', 'NCC02', 'buoi.jpeg'),
    ('33', 'Dua', '02', 20000, 80, 'kg', 'NCC02', 'dua.jpeg'),
    ('34', 'Nho', '02', 45000, 30, 'kg', 'NCC02', 'nho.jpeg'),
    ('35', 'Quyt', '02', 22000, 90, 'kg', 'NCC02', 'quyt.jpeg'),
    ('36', 'Gung', '03', 40000, 50, 'kg', 'NCC03', 'gung.jpeg'),
    ('37', 'Toi', '03', 60000, 25, 'kg', 'NCC03', 'toi.jpeg'),
    ('38', 'Tieu', '03', 70000, 15, 'kg', 'NCC03', 'tieu.jpeg'),
    ('39', 'Hanh', '03', 30000, 35, 'kg', 'NCC03', 'hanh.jpeg'),
    ('40', 'Muoi', '03', 10000, 100, 'kg', 'NCC03', 'muoi.jpeg'),
    ('41', 'Gao', '04', 20000, 200, 'kg', 'NCC04', 'gao.jpeg'),
    ('42', 'Ngo', '04', 18000, 150, 'kg', 'NCC04', 'ngo.jpeg'),
    ('43', 'Khoai mi', '04', 25000, 130, 'kg', 'NCC04', 'khoaimi.jpeg'),
    ('44', 'Bot mi', '04', 28000, 100, 'kg', 'NCC04', 'botmi.jpeg'),
    ('45', 'Banh mi', '04', 15000, 50, 'kg', 'NCC04', 'banhmi.jpeg'),
    ('46', 'Thit heo', '05', 80000, 40, 'kg', 'NCC04', 'thitheo.jpeg'),
    ('47', 'Thit bo', '05', 120000, 30, 'kg', 'NCC04', 'thitbo.jpeg'),
    ('48', 'Thit ga', '05', 60000, 70, 'kg', 'NCC04', 'thitga.jpeg'),
    ('49', 'Tom', '05', 150000, 20, 'kg', 'NCC04', 'tom.jpeg'),
    ('50', 'Ca hoi', '05', 250000, 15, 'kg', 'NCC04', 'cahoi.jpeg'),
    ('51', 'Thit vit', '05', 75000, 40, 'kg', 'NCC05', 'thitvit.jpeg'),
    ('52', 'Banh chung', '04', 30000, 50, 'kg', 'NCC05', 'banhchung.jpeg'),
    ('53', 'Dau xanh', '04', 22000, 75, 'kg', 'NCC05', 'dauxanh.jpeg'),
    ('54', 'Dau den', '04', 25000, 60, 'kg', 'NCC05', 'dauden.jpeg'),
    ('55', 'Bap ngo', '04', 18000, 90, 'kg', 'NCC05', 'bapngo.jpeg'),
    ('56', 'Thit cuu', '05', 140000, 30, 'kg', 'NCC05', 'thitcuu.jpeg'),
    ('57', 'Cha lua', '05', 70000, 45, 'kg', 'NCC05', 'chalua.jpeg'),
    ('58', 'Thit ga cong nghiep', '05', 55000, 50, 'kg', 'NCC05', 'thitgacongnghiep.jpeg'),
    ('59', 'Thit bo tuoi', '05', 120000, 35, 'kg', 'NCC05', 'thitbotuoi.jpeg'),
    ('60', 'So diep', '05', 200000, 20, 'kg', 'NCC05', 'xodiep.jpeg');


	-- Thêm dữ liệu vào bảng NhaCungCap


	-- Thêm dữ liệu vào bảng LoaiNongSan
INSERT INTO LoaiNongSan (MaLoai, TenLoai)
VALUES
    ('01', 'Rau cu'),
    ('02', 'Hoa qua'),
    ('03', 'Gia vi'),
    ('04', 'Luong thuc'),
    ('05', 'Thit');


INSERT INTO TaiKhoan (MaTaiKhoan, MatKhau, LoaiTaiKhoan, HoTen, SoDienThoai, Email, DiaChi)
VALUES
('TK01', 'pw1', 'Khach', 'Nguyễn Văn A', '0901234567', 'vana@gmail.com', 'Hà Nội'),
('TK02', 'pw2', 'Khach', 'Trần Thị B', '0902345678', 'thib@gmail.com', 'Hồ Chí Minh'),
('TK03', 'pw3', 'Khach', 'Lê Văn C', '0903456789', 'vanc@gmail.com', 'Đà Nẵng'),
('TK04', 'pw4', 'Khach', 'Phạm Thị D', '0904567890', 'thid@gmail.com', 'Hải Phòng'),
('TK05', 'pw5', 'Khach', 'Hoàng Văn E', '0905678901', 'vane@gmail.com', 'Cần Thơ'),
('TK06', 'pw6', 'Khach', 'Nguyễn Thị F', '0906789012', 'thif@gmail.com', 'Huế'),
('TK07', 'pw7', 'Khach', 'Trần Văn G', '0907890123', 'vang@gmail.com', 'Vũng Tàu'),
('TK08', 'pw8', 'Khach', 'Lê Thị H', '0908901234', 'thih@gmail.com', 'Bình Dương'),
('TK09', 'pw9', 'Khach', 'Phạm Văn I', '0909012345', 'vani@gmail.com', 'Đắk Lắk'),
('TK10', 'pw10', 'Khach', 'Hoàng Thị J', '0910123456', 'thij@gmail.com', 'Nghệ An'),
('TK_ADMIN', '1', 'Admin', 'Admin', '0999999999', 'admin@nongsan.vn', 'Trụ sở chính');
