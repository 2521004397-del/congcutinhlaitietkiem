import streamlit as st
st.image("logo.jpg.png")

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-top: 20px;
    }

    .result-label {
        font-size: 15px;
        color: #666;
    }

    .result-value {
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_currency(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<div class="main-title">💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM_Thảo Tiên</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Nhập thông tin tiền gửi để tính tiền lãi và số tiền nhận được</div>',
    unsafe_allow_html=True
)


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

so_tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.01,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Chuyển lãi suất % sang số thập phân
    lai_suat_nam = lai_suat / 100

    # Tổng tiền lãi theo kỳ hạn
    tong_tien_lai = (
        so_tien_gui
        * lai_suat_nam
        * ky_han
        / 12
    )

    # =========================
    # TÍNH THEO HÌNH THỨC NHẬN LÃI
    # =========================

    if hinh_thuc == "Cuối kỳ":

        tien_lai_dinh_ky = tong_tien_lai
        so_ky = 1
        so_thang_moi_ky = ky_han

        # Bảng chi tiết
        data = [{
            "Kỳ nhận lãi": f"Kỳ hạn {ky_han} tháng",
            "Số tháng": ky_han,
            "Tiền lãi": tien_lai_dinh_ky
        }]

    elif hinh_thuc == "Hàng tháng":

        so_ky = ky_han
        so_thang_moi_ky = 1

        tien_lai_dinh_ky = (
            so_tien_gui
            * lai_suat_nam
            / 12
        )

        data = []

        for i in range(1, ky_han + 1):
            data.append({
                "Kỳ nhận lãi": f"Tháng {i}",
                "Số tháng": 1,
                "Tiền lãi": tien_lai_dinh_ky
            })

    else:  # Hàng quý

        so_ky = ky_han // 3
        so_thang_con_lai = ky_han % 3

        tien_lai_dinh_ky = (
            so_tien_gui
            * lai_suat_nam
            * 3
            / 12
        )

        data = []

        # Các kỳ quý đầy đủ
        for i in range(1, so_ky + 1):
            data.append({
                "Kỳ nhận lãi": f"Quý {i}",
                "Số tháng": 3,
                "Tiền lãi": tien_lai_dinh_ky
            })

        # Nếu kỳ hạn còn dư 1 hoặc 2 tháng
        if so_thang_con_lai > 0:
            tien_lai_ky_cuoi = (
                so_tien_gui
                * lai_suat_nam
                * so_thang_con_lai
                / 12
            )

            data.append({
                "Kỳ nhận lãi": "Kỳ cuối",
                "Số tháng": so_thang_con_lai,
                "Tiền lãi": tien_lai_ky_cuoi
            })


    # =========================
    # TỔNG TIỀN
    # =========================
    tong_tien_nhan = so_tien_gui + tong_tien_lai


    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Đã tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            format_currency(tien_lai_dinh_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_currency(tong_tien_lai)
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Tiền gốc",
            format_currency(so_tien_gui)
        )

    with col4:
        st.metric(
            "Tổng tiền nhận",
            format_currency(tong_tien_nhan)
        )


    # =========================
    # TÓM TẮT
    # =========================
    st.markdown("---")

    st.subheader("📝 Thông tin chi tiết")

    st.write(f"**Số tiền gửi:** {format_currency(so_tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

    # =========================
    # BẢNG LỊCH NHẬN LÃI
    # =========================
    st.subheader("📅 Lịch nhận tiền lãi")

    df = pd.DataFrame(data)

    # Định dạng tiền
    df["Tiền lãi"] = df["Tiền lãi"].apply(format_currency)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # =========================
    # TỔNG KẾT
    # =========================
    st.markdown("---")

    st.subheader("💵 Tổng kết")

    st.write(
        f"**Tổng tiền lãi:** "
        f"{format_currency(tong_tien_lai)}"
    )

    st.write(
        f"**Tổng số tiền gốc + lãi:** "
        f"{format_currency(tong_tien_nhan)}"
    )

    # =========================
    # CÔNG THỨC
    # =========================
    with st.expander("ℹ️ Xem công thức tính"):

        st.write(
            "**Tiền lãi = Tiền gốc × Lãi suất (%/năm) × Số tháng / 12**"
        )

        st.write(
            "Ví dụ: Gửi 100.000.000 VNĐ, lãi suất 5%/năm "
            "trong 12 tháng:"
        )

        st.code(
            "100.000.000 × 5% × 12 / 12 = 5.000.000 VNĐ"
        )

        st.info(
            "Lưu ý: Đây là công cụ tính lãi tham khảo. "
            "Lãi suất và phương pháp tính thực tế có thể khác "
            "tùy theo ngân hàng, sản phẩm tiền gửi và quy định "
            "của từng ngân hàng."
        )
