# MIT License

# Copyright (c) 2024 Mizutsuki-Sae

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas, Frame, ttk
import webbrowser

# 윤년 판별 함수
def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

# 복리 통장 계산 함수 (매일 복리)
def compound_interest_daily(principal, annual_rate, months, start_year):
    daily_rate = annual_rate / 365  # 일일 이자율
    total_amount = principal
    total_days = 0

    # 월별 일수 (각각의 월에 대해 실제 일수를 계산)
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 기본 월별 일수 (2월은 나중에 윤년 고려)
    
    if is_leap_year(start_year):
        month_days[1] = 29  # 2월을 29일로 설정
    
    for month in range(months):
        total_days += month_days[month % 12]  # 월을 12로 나눈 나머지로 반복하여 일수 합산
    
    for day in range(total_days):
        total_amount += total_amount * daily_rate  # 매일 복리 적용
    
    return total_amount

# 복리 통장 계산 함수 (월 복리)
def compound_interest_monthly(principal, annual_rate, months):
    monthly_rate = annual_rate / 12  # 월 이자율
    total_amount = principal
    for month in range(months):
        total_amount += total_amount * monthly_rate  # 월 복리 적용
    return total_amount

# 복리 통장 계산 함수 (연 복리)
def compound_interest_yearly(principal, annual_rate, months):
    yearly_rate = annual_rate  # 연 이자율
    total_amount = principal
    total_years = months / 12
    for _ in range(int(total_years)):
        total_amount += total_amount * yearly_rate  # 연 복리 적용
    return total_amount

# 적금 통장 계산 함수 (단리 이자)
def savings_interest(principal, annual_rate, months):
    monthly_rate = annual_rate / 12  # 월 이자율
    total_interest = principal * monthly_rate * months  # 단리 이자 계산
    total_amount = principal + total_interest  # 총 금액
    return total_amount, total_interest

# 예금 통장 계산 함수 (단리 이자)
def deposit_interest(principal, annual_rate, months):
    # 단리 이자 계산
    total_interest = principal * annual_rate * months / 12  # 총 이자 = 원금 * 이자율 * 기간 (개월) / 12
    total_amount = principal + total_interest  # 총 금액 = 원금 + 이자
    return total_amount, total_interest

# 계산 함수
def calculate():
    try:
        # 사용자 입력 값 받기
        deposit_initial_amount = float(entry_deposit_initial_amount.get())  # 예금 통장 저축 금액
        savings_initial_amount = float(entry_savings_initial_amount.get())  # 적금 통장 처음 금액
        compound_initial_amount = float(entry_compound_initial_amount.get())  # 복리 통장 처음 금액

        # 월 저축 금액 받기 (체크박스에 따라 선택적으로 반영)
        monthly_deposit = 0  # 기본값은 0으로 설정
        if var_savings_account.get():  # 적금 통장 체크박스가 선택되었으면
            monthly_deposit = float(entry_monthly_deposit.get())
        elif var_compound_account.get():  # 복리 통장 체크박스가 선택되었으면
            monthly_deposit = float(entry_monthly_deposit.get())

        annual_rate_compound = float(entry_annual_rate_compound.get()) / 100
        annual_rate_savings = float(entry_annual_rate_savings.get()) / 100
        annual_rate_deposit = float(entry_annual_rate_deposit.get()) / 100  # 예금 통장 이자율
        months = int(entry_months.get())  # 저축 기간
        start_year = int(entry_start_year.get())  # 시작 연도를 입력받음
        tax_rate = float(entry_tax_rate.get()) / 100  # 사용자 입력 세율

        # 복리 형식에 따른 함수 선택
        compound_format = compound_format_var.get()
        if compound_format == "매일 복리":
            compound_interest_function = compound_interest_daily
        elif compound_format == "월 복리":
            compound_interest_function = compound_interest_monthly
        elif compound_format == "연 복리":
            compound_interest_function = compound_interest_yearly

        # 복리 통장 계산
        total_compound = 0
        total_compound_interest = 0  # 복리 통장 이자 합계
        if var_compound_account.get():  # 복리 통장 체크박스가 선택되었으면
            for i in range(months):
                if compound_format == "매일 복리":
                    if i == 0:
                        amount = compound_interest_function(compound_initial_amount + monthly_deposit, annual_rate_compound, months - i, start_year)
                    else:
                        amount = compound_interest_function(monthly_deposit, annual_rate_compound, months - i, start_year)
                else:
                    if i == 0:
                        amount = compound_interest_function(compound_initial_amount + monthly_deposit, annual_rate_compound, months - i)
                    else:
                        amount = compound_interest_function(monthly_deposit, annual_rate_compound, months - i)

                total_compound += amount
                total_compound_interest += amount - (monthly_deposit if i > 0 else compound_initial_amount + monthly_deposit)  # 이자 부분만 합산

        # 적금 통장 계산
        total_savings = 0
        total_savings_interest = 0  # 적금 통장 이자 합계
        if var_savings_account.get():  # 적금 통장 체크박스가 선택되었으면
            for i in range(months):
                if i == 0:
                    amount, interest = savings_interest(savings_initial_amount + monthly_deposit, annual_rate_savings, months - i)
                else:
                    amount, interest = savings_interest(monthly_deposit, annual_rate_savings, months - i)
                total_savings += amount
                total_savings_interest += interest  # 이자 부분만 합산

        # 예금 통장 계산 (체크박스와 관계없이 항상 계산)
        total_deposit, total_deposit_interest = deposit_interest(deposit_initial_amount, annual_rate_deposit, months)

        # 세금 계산 (사용자가 입력한 세율 적용)
        compound_after_tax = total_compound - (total_compound_interest * tax_rate) if var_compound_account.get() else 0
        savings_after_tax = total_savings - (total_savings_interest * tax_rate) if var_savings_account.get() else 0
        deposit_after_tax = total_deposit - (total_deposit_interest * tax_rate)

        # 세금 적용 후 이자 계산 (세금은 이자에만 적용)
        compound_interest_after_tax = total_compound_interest - (total_compound_interest * tax_rate) if var_compound_account.get() else 0
        savings_interest_after_tax = total_savings_interest - (total_savings_interest * tax_rate) if var_savings_account.get() else 0
        deposit_interest_after_tax = total_deposit_interest - (total_deposit_interest * tax_rate)

        # 결과 출력 (세금 적용 전과 후 각각 상자에 넣기)
        update_result_boxes(total_compound, total_savings, total_deposit, total_compound_interest, total_savings_interest, total_deposit_interest, compound_after_tax, savings_after_tax, deposit_after_tax, compound_interest_after_tax, savings_interest_after_tax, deposit_interest_after_tax)

    except ValueError:
        messagebox.showerror("입력 오류", "잘못된 값을 입력하셨습니다. 올바른 값을 입력해주세요.")


# 결과 업데이트 함수 (세금 전후 금액 상자 업데이트)
def update_result_boxes(compound_before, savings_before, deposit_before, compound_interest, savings_interest, deposit_interest, compound_after_tax, savings_after_tax, deposit_after_tax, compound_interest_after_tax, savings_interest_after_tax, deposit_interest_after_tax):
    result_before_text = (
        f"예금 통장: {deposit_before:,.0f} 원\n"
        f"적금 통장: {savings_before:,.0f} 원\n"
        f"복리 통장: {compound_before:,.0f} 원\n\n"
        f"예금 통장 이자: {deposit_interest:,.0f} 원\n"
        f"적금 통장 이자: {savings_interest:,.0f} 원\n"
        f"복리 통장 이자: {compound_interest:,.0f} 원"
    )
    result_after_text = (
        f"예금 통장: {deposit_after_tax:,.0f} 원\n"
        f"적금 통장: {savings_after_tax:,.0f} 원\n"
        f"복리 통장: {compound_after_tax:,.0f} 원\n\n"
        f"예금 통장 이자: {deposit_interest_after_tax:,.0f} 원\n"
        f"적금 통장 이자: {savings_interest_after_tax:,.0f} 원\n"
        f"복리 통장 이자: {compound_interest_after_tax:,.0f} 원"
    )

    tax_before_label.config(text=result_before_text)
    tax_after_label.config(text=result_after_text)

# GUI 설정
root = tk.Tk()
root.title("저축 통장 계산기")
root.geometry("600x600")

# 저작권 문구 추가
copyright_label = tk.Label(root, text="Copyright (c) 2024 Mizutsuki-Sae", font=("Arial", 10), fg="#777", bg="#f9f9f9", cursor="hand2")
copyright_label.pack(side="bottom", pady=10)

# 클릭 이벤트 처리
copyright_label.bind("<Button-1>", lambda e: open_github())  # GitHub 링크로 이동

# GitHub 링크를 열기 위한 함수
def open_github():
    webbrowser.open("https://github.com/Mizutsuki-Sae/Savings-Calculator")

# 전체 배경 색상 설정
root.config(bg="#f9f9f9")

# 스크롤 가능한 영역 설정
canvas = tk.Canvas(root, bg="#f9f9f9", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# 내부 프레임을 캔버스에 추가
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

# 캔버스의 스크롤 범위 설정
def on_configure(event):
    # 내부 프레임 크기와 Canvas의 스크롤 영역 동기화
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(canvas_window, width=canvas.winfo_width())

def on_resize(event):
    # Canvas 크기 변경 시 스크롤 영역과 내부 프레임 크기 업데이트
    canvas_width = event.width
    canvas.itemconfig(canvas_window, width=canvas_width)
    canvas.configure(scrollregion=canvas.bbox("all"))

# 내부 프레임의 크기를 Canvas에 맞추기
scrollable_frame.bind("<Configure>", on_configure)

# 창 크기 조정 시 캔버스 크기 업데이트
canvas.bind("<Configure>", on_resize)

# 마우스 스크롤로 캔버스 스크롤 제어
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# 마우스 휠 이벤트 바인딩
root.bind_all("<MouseWheel>", on_mouse_wheel)

# 제목 프레임 설정
title_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
title_frame.pack(padx=20, pady=10)

# 제목 라벨 추가
title_label = tk.Label(title_frame, text="저축 통장 계산기", font=("Arial", 18, "bold"), bg="#f9f9f9", fg="#4CAF50")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# 기존 프레임 설정 (입력 필드와 계산 버튼을 포함)
frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
frame.pack(padx=20, pady=20)

# 각 입력 필드 및 라벨
label_deposit_initial_amount = tk.Label(frame, text="예금 통장 저축 금액 (원):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_deposit_initial_amount.grid(row=0, column=0, sticky="w", padx=5, pady=10)
entry_deposit_initial_amount = tk.Entry(frame, font=("Arial", 12))
entry_deposit_initial_amount.grid(row=0, column=1, padx=10, pady=10)

label_savings_initial_amount = tk.Label(frame, text="적금 통장 처음 금액 (원):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_savings_initial_amount.grid(row=1, column=0, sticky="w", padx=5, pady=10)
entry_savings_initial_amount = tk.Entry(frame, font=("Arial", 12))
entry_savings_initial_amount.grid(row=1, column=1, padx=10, pady=10)

label_compound_initial_amount = tk.Label(frame, text="복리 통장 처음 금액 (원):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_compound_initial_amount.grid(row=2, column=0, sticky="w", padx=5, pady=10)
entry_compound_initial_amount = tk.Entry(frame, font=("Arial", 12))
entry_compound_initial_amount.grid(row=2, column=1, padx=10, pady=10)

# '매달 저축할 금액 (원):' 필드와 복리 형식 선택 드롭다운 사이에 복리 형식 선택 메뉴 추가
label_monthly_deposit = tk.Label(frame, text="매달 저축할 금액 (원):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_monthly_deposit.grid(row=3, column=0, sticky="w", padx=5, pady=10)
entry_monthly_deposit = tk.Entry(frame, font=("Arial", 12))
entry_monthly_deposit.grid(row=3, column=1, padx=10, pady=10)

# '복리 통장', '적금 통장', '예금 통장'에 매달 저축할 금액을 넣을지 여부를 선택하는 체크박스들
var_savings_account = tk.BooleanVar()
checkbox_savings = tk.Checkbutton(frame, text="적금 통장에 넣기", variable=var_savings_account, font=("Arial", 12), bg="#f9f9f9", fg="#333")
checkbox_savings.grid(row=4, column=0, sticky="w", padx=5, pady=5)

var_compound_account = tk.BooleanVar()
checkbox_compound = tk.Checkbutton(frame, text="복리 통장에 넣기", variable=var_compound_account, font=("Arial", 12), bg="#f9f9f9", fg="#333")
checkbox_compound.grid(row=4, column=1, sticky="w", padx=5, pady=5)

# 복리 형식 선택 드롭다운 메뉴
label_compound_format = tk.Label(frame, text="복리 형식 선택:", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_compound_format.grid(row=5, column=0, sticky="w", padx=5, pady=10)

# 드롭다운 메뉴에 사용할 옵션들
compound_formats = ["매일 복리", "월 복리", "연 복리"]

# 드롭다운 메뉴 (스타일 수정)
compound_format_var = tk.StringVar()
compound_format_var.set(compound_formats[0])  # 기본값은 "일일 복리"

compound_format_menu = tk.OptionMenu(frame, compound_format_var, *compound_formats)
compound_format_menu.config(font=("Arial", 12), bg="#fff", fg="#333", relief="raised", width=15)
compound_format_menu.grid(row=5, column=1, padx=10, pady=10)

# '각 통장 연 이자율 (%):' 필드
label_annual_rate_deposit = tk.Label(frame, text="예금 통장 연 이자율 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_annual_rate_deposit.grid(row=6, column=0, sticky="w", padx=5, pady=10)
entry_annual_rate_deposit = tk.Entry(frame, font=("Arial", 12))
entry_annual_rate_deposit.grid(row=6, column=1, padx=10, pady=10)

label_annual_rate_savings = tk.Label(frame, text="적금 통장 연 이자율 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_annual_rate_savings.grid(row=7, column=0, sticky="w", padx=5, pady=10)
entry_annual_rate_savings = tk.Entry(frame, font=("Arial", 12))
entry_annual_rate_savings.grid(row=7, column=1, padx=10, pady=10)

label_annual_rate_compound = tk.Label(frame, text="복리 통장 연 이자율 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_annual_rate_compound.grid(row=8, column=0, sticky="w", padx=5, pady=10)
entry_annual_rate_compound = tk.Entry(frame, font=("Arial", 12))
entry_annual_rate_compound.grid(row=8, column=1, padx=10, pady=10)

label_tax_rate = tk.Label(frame, text="세금 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_tax_rate.grid(row=9, column=0, sticky="w", padx=5, pady=10)
entry_tax_rate = tk.Entry(frame, font=("Arial", 12))
entry_tax_rate.grid(row=9, column=1, padx=10, pady=10)

label_months = tk.Label(frame, text="저축 기간 (개월):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_months.grid(row=10, column=0, sticky="w", padx=5, pady=10)
entry_months = tk.Entry(frame, font=("Arial", 12))
entry_months.grid(row=10, column=1, padx=10, pady=10)

label_start_year = tk.Label(frame, text="시작 연도:", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_start_year.grid(row=11, column=0, sticky="w", padx=5, pady=10)
entry_start_year = tk.Entry(frame, font=("Arial", 12))
entry_start_year.grid(row=11, column=1, padx=10, pady=10)

# 계산 버튼 스타일
button_calculate = tk.Button(frame, text="계산", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", command=calculate)
button_calculate.grid(row=12, column=0, columnspan=2, pady=20)

# 결과 출력 프레임
result_frame = tk.Frame(scrollable_frame, bg="#f9f9f9")
result_frame.pack(padx=20, pady=10)

# 세금 적용 전 금액 상자
tax_before_box = tk.Frame(result_frame, bg="#f9f9f9", bd=2, relief="solid", padx=10, pady=10, width=250)
tax_before_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

tax_before_label = tk.Label(tax_before_box, text="세금 적용 전 금액", font=("Arial", 14, "bold"), bg="#f9f9f9", fg="#333")
tax_before_label.pack(fill="both", expand=True)

# 세금 적용 후 금액 상자
tax_after_box = tk.Frame(result_frame, bg="#f9f9f9", bd=2, relief="solid", padx=10, pady=10, width=250)
tax_after_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

tax_after_label = tk.Label(tax_after_box, text="세금 적용 후 금액", font=("Arial", 14, "bold"), bg="#f9f9f9", fg="#333")
tax_after_label.pack(fill="both", expand=True)

# 상자 설명 추가
tax_before_description = tk.Label(tax_before_box, text="세금이 적용되지 않은 총 금액입니다.", font=("Arial", 10), bg="#f9f9f9", fg="#777")
tax_before_description.pack(pady=5)

tax_after_description = tk.Label(tax_after_box, text="세금이 적용된 후의 총 금액입니다.", font=("Arial", 10), bg="#f9f9f9", fg="#777")
tax_after_description.pack(pady=5)

# GUI 실행
root.mainloop()