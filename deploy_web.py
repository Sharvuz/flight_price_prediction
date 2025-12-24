import pandas as pd
import joblib
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display



def du_doan_gia_ve_chinh_xac(hang_bay, diem_di, diem_den, loai_ve, gio_di, gio_den):
    format_type = '%H:%M:%S %d/%m/%Y'

    try:
        t_di = pd.to_datetime(gio_di, format=format_type)
        t_den = pd.to_datetime(gio_den, format=format_type)

        if t_den <= t_di:
            return "Lỗi: Thời gian hạ cánh phải sau thời gian khởi hành!"

        duration = (t_den - t_di).total_seconds() / 60.0
    except ValueError:
        return "Lỗi: Định dạng ngày giờ không hợp lệ (đúng: HH:MM:SS dd/mm/yyyy)"

    # Tạo DataFrame đầu vào
    input_df = pd.DataFrame({
        'code_name': [hang_bay],
        'from': [diem_di],
        'to': [diem_den],
        'type': [loai_ve],
        'f_time_from': [t_di]
    })

    input_df['hour'] = input_df['f_time_from'].dt.hour
    input_df['day_of_week'] = input_df['f_time_from'].dt.day_of_week
    input_df['day'] = input_df['f_time_from'].dt.day
    input_df['month'] = input_df['f_time_from'].dt.month

    input_df['duration_minutes'] = duration

    input_encoded = pd.get_dummies(input_df, columns=['code_name', 'from', 'to', 'type'])

    final_input = input_encoded.reindex(columns=X_train.columns, fill_value=0)

    # Dự đoán giá
    predicted_price = float(model.predict(final_input)[0])

    return predicted_price



ds_hang_bay = ['Vietnam Airlines', 'Vietjet', 'Bamboo Airways', 'Pacific Airlines', 'Vietravel Airlines']
ds_diem_di = ['TP HCM', 'Hà Nội', 'Đà Nẵng', 'Hải Phòng', 'Thanh Hóa', 'Nha Trang', 'Phú Quốc', 'Vinh', 'Quy Nhơn',
              'Cần Thơ', 'Đà Lạt', 'Huế']
ds_diem_den = ds_diem_di
ds_loai_ve = ['Eco', 'Business', 'Economy (EL)-P', 'Eco Saver']

print("--- ỨNG DỤNG DỰ ĐOÁN GIÁ VÉ (NHẬP GIỜ HẠ CÁNH) ---")

w_hang = widgets.Dropdown(options=ds_hang_bay, description='Hãng bay:')
w_di = widgets.Dropdown(options=ds_diem_di, description='Điểm đi:', value='Hà Nội')
w_den = widgets.Dropdown(options=ds_diem_den, description='Điểm đến:', value='TP HCM')
w_loai = widgets.Dropdown(options=ds_loai_ve, description='Loại vé:', value='Eco')

default_time = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
w_gio_di = widgets.Text(description='Giờ đi:', value='08:00:00 01/05/2021', placeholder='HH:MM:SS dd/mm/yyyy')
w_gio_den = widgets.Text(description='Giờ đến:', value='10:15:00 01/05/2021', placeholder='HH:MM:SS dd/mm/yyyy')

btn = widgets.Button(description="Dự đoán", button_style='success', icon='plane')
output = widgets.Output()


def on_click_predict(b):
    with output:
        output.clear_output()
        result = du_doan_gia_ve_chinh_xac(
            hang_bay=w_hang.value,
            diem_di=w_di.value,
            diem_den=w_den.value,
            loai_ve=w_loai.value,
            gio_di=w_gio_di.value,
            gio_den=w_gio_den.value
        )

        if isinstance(result, str):
            print(result)
        else:
            t1 = pd.to_datetime(w_gio_di.value, format='%H:%M:%S %d/%m/%Y')
            t2 = pd.to_datetime(w_gio_den.value, format='%H:%M:%S %d/%m/%Y')
            dur = (t2 - t1).total_seconds() / 60
            print(f"Thời gian bay: {dur:.0f} phút")
            print(f"💰 Giá vé dự đoán: {result:,.0f} VNĐ")


btn.on_click(on_click_predict)

display(w_hang, w_di, w_den, w_loai, w_gio_di, w_gio_den, btn, output)