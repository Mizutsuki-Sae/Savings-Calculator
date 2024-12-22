import tkinter as tk
from tkinter import messagebox

# 윤년 판별 함수
def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

# 복리 통장 계산 함수 (매일 복리)
def compound_interest(principal, annual_rate, months, start_year):
    daily_rate = annual_rate / 365  # 일일 이자율
    total_amount = principal  # 처음 원금은 그대로 시작
    total_days = 0
    
    # 월별 일수 (각각의 월에 대해 실제 일수를 계산)
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 기본 월별 일수 (2월은 나중에 윤년 고려)
    
    # 윤년인 경우 2월을 29일로 수정
    if is_leap_year(start_year):
        month_days[1] = 29  # 2월을 29일로 설정
    
    # 주어진 기간 동안 각 월의 일수를 합산
    for month in range(months):
        # 월별 일수를 더함
        total_days += month_days[month % 12]  # 월을 12로 나눈 나머지로 반복하여 일수 합산
    
    # 매일 복리 계산
    for day in range(total_days):
        total_amount += total_amount * daily_rate  # 매일 복리 적용
    
    return total_amount

# 적금 통장 계산 함수 (단리 이자)
def savings_interest(principal, annual_rate, months):
    monthly_rate = annual_rate / 12  # 월 이자율
    total_interest = principal * monthly_rate * months  # 단리 이자 계산
    total_amount = principal + total_interest  # 총 금액
    return total_amount, total_interest

# 예금 통장 계산 함수 (단리 이자)
def deposit_interest(principal, monthly_deposit, annual_rate, months):
    total_amount = principal
    total_interest = 0
    for month in range(months):
        # 매월 예치된 금액에 대해서 이자를 계산하고 더함
        monthly_interest = (total_amount + monthly_deposit) * annual_rate / 12  # 월별 이자
        total_interest += monthly_interest
        total_amount += monthly_deposit + monthly_interest  # 매월 예치된 금액 + 이자
    return total_amount, total_interest

# 계산 함수
def calculate():
    try:
        # 사용자 입력 값 받기
        initial_amount = float(entry_initial_amount.get())  # 처음 금액
        monthly_deposit = float(entry_monthly_deposit.get())  # 매월 예치금
        annual_rate_compound = float(entry_annual_rate_compound.get()) / 100
        annual_rate_savings = float(entry_annual_rate_savings.get()) / 100
        annual_rate_deposit = float(entry_annual_rate_deposit.get()) / 100  # 예금 통장 이자율
        months = int(entry_months.get())  # 저축 기간
        start_year = int(entry_start_year.get())  # 시작 연도를 입력받음
        tax_rate = float(entry_tax_rate.get()) / 100  # 사용자 입력 세율

        # 복리 통장 계산
        total_compound = 0
        total_compound_interest = 0  # 복리 통장 이자 합계
        for i in range(months):
            if i == 0:
                amount = compound_interest(initial_amount + monthly_deposit, annual_rate_compound, months - i, start_year)
            else:
                amount = compound_interest(monthly_deposit, annual_rate_compound, months - i, start_year)
            total_compound += amount
            total_compound_interest += amount - (monthly_deposit if i > 0 else initial_amount + monthly_deposit)  # 이자 부분만 합산

        # 적금 통장 계산
        total_savings = 0
        total_savings_interest = 0  # 적금 통장 이자 합계
        for i in range(months):
            if i == 0:
                amount, interest = savings_interest(initial_amount + monthly_deposit, annual_rate_savings, months - i)
            else:
                amount, interest = savings_interest(monthly_deposit, annual_rate_savings, months - i)
            total_savings += amount
            total_savings_interest += interest  # 이자 부분만 합산

        # 예금 통장 계산
        total_deposit, total_deposit_interest = deposit_interest(initial_amount, monthly_deposit, annual_rate_deposit, months)

        # 세금 계산 (사용자가 입력한 세율 적용)
        compound_after_tax = total_compound - (total_compound_interest * tax_rate)
        savings_after_tax = total_savings - (total_savings_interest * tax_rate)
        deposit_after_tax = total_deposit - (total_deposit_interest * tax_rate)

        # 세금 적용 후 이자 계산 (세금은 이자에만 적용)
        compound_interest_after_tax = total_compound_interest - (total_compound_interest * tax_rate)
        savings_interest_after_tax = total_savings_interest - (total_savings_interest * tax_rate)
        deposit_interest_after_tax = total_deposit_interest - (total_deposit_interest * tax_rate)

        # 결과 출력 (세금 적용 전과 후 각각 상자에 넣기)
        update_result_boxes(total_compound, total_savings, total_deposit, total_compound_interest, total_savings_interest, total_deposit_interest, compound_after_tax, savings_after_tax, deposit_after_tax, compound_interest_after_tax, savings_interest_after_tax, deposit_interest_after_tax)

    except ValueError:
        messagebox.showerror("입력 오류", "잘못된 값을 입력하셨습니다. 올바른 값을 입력해주세요.")

# 결과 업데이트 함수 (세금 전후 금액 상자 업데이트)
def update_result_boxes(compound_before, savings_before, deposit_before, compound_interest, savings_interest, deposit_interest, compound_after_tax, savings_after_tax, deposit_after_tax, compound_interest_after_tax, savings_interest_after_tax, deposit_interest_after_tax):
    result_before_text = (
        f"복리 통장: {compound_before:,.0f} 원\n"
        f"적금 통장: {savings_before:,.0f} 원\n"
        f"예금 통장: {deposit_before:,.0f} 원\n\n"
        f"복리 통장 이자: {compound_interest:,.0f} 원\n"
        f"적금 통장 이자: {savings_interest:,.0f} 원\n"
        f"예금 통장 이자: {deposit_interest:,.0f} 원"
    )
    result_after_text = (
        f"복리 통장: {compound_after_tax:,.0f} 원\n"
        f"적금 통장: {savings_after_tax:,.0f} 원\n"
        f"예금 통장: {deposit_after_tax:,.0f} 원\n\n"
        f"복리 통장 이자: {compound_interest_after_tax:,.0f} 원\n"
        f"적금 통장 이자: {savings_interest_after_tax:,.0f} 원\n"
        f"예금 통장 이자: {deposit_interest_after_tax:,.0f} 원"
    )

    tax_before_label.config(text=result_before_text)
    tax_after_label.config(text=result_after_text)

# GUI 설정
root = tk.Tk()
root.title("저축 통장 계산기")

# 전체 배경 색상 설정
root.config(bg="#f9f9f9")

# 프레임 설정 (입력 필드와 계산 버튼을 포함)
frame = tk.Frame(root, bg="#f9f9f9")
frame.pack(padx=20, pady=20)

# 제목 라벨 추가
title_label = tk.Label(frame, text="저축 통장 계산기", font=("Arial", 18, "bold"), bg="#f9f9f9", fg="#4CAF50")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# 각 입력 필드 및 라벨
label_initial_amount = tk.Label(frame, text="처음 금액 (원):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_initial_amount.grid(row=1, column=0, sticky="w", padx=5, pady=10)
entry_initial_amount = tk.Entry(frame, font=("Arial", 12))
entry_initial_amount.grid(row=1, column=1, padx=10, pady=10)

label_monthly_deposit = tk.Label(frame, text="매달 저축할 금액 (원):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_monthly_deposit.grid(row=2, column=0, sticky="w", padx=5, pady=10)
entry_monthly_deposit = tk.Entry(frame, font=("Arial", 12))
entry_monthly_deposit.grid(row=2, column=1, padx=10, pady=10)

label_annual_rate_compound = tk.Label(frame, text="복리 통장 연 이자율 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_annual_rate_compound.grid(row=3, column=0, sticky="w", padx=5, pady=10)
entry_annual_rate_compound = tk.Entry(frame, font=("Arial", 12))
entry_annual_rate_compound.grid(row=3, column=1, padx=10, pady=10)

label_annual_rate_savings = tk.Label(frame, text="적금 통장 연 이자율 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_annual_rate_savings.grid(row=4, column=0, sticky="w", padx=5, pady=10)
entry_annual_rate_savings = tk.Entry(frame, font=("Arial", 12))
entry_annual_rate_savings.grid(row=4, column=1, padx=10, pady=10)

label_annual_rate_deposit = tk.Label(frame, text="예금 통장 연 이자율 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_annual_rate_deposit.grid(row=5, column=0, sticky="w", padx=5, pady=10)
entry_annual_rate_deposit = tk.Entry(frame, font=("Arial", 12))
entry_annual_rate_deposit.grid(row=5, column=1, padx=10, pady=10)

label_tax_rate = tk.Label(frame, text="세금 (%):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_tax_rate.grid(row=6, column=0, sticky="w", padx=5, pady=10)
entry_tax_rate = tk.Entry(frame, font=("Arial", 12))
entry_tax_rate.grid(row=6, column=1, padx=10, pady=10)

label_months = tk.Label(frame, text="저축 기간 (개월):", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_months.grid(row=7, column=0, sticky="w", padx=5, pady=10)
entry_months = tk.Entry(frame, font=("Arial", 12))
entry_months.grid(row=7, column=1, padx=10, pady=10)

label_start_year = tk.Label(frame, text="시작 연도:", font=("Arial", 12), bg="#f9f9f9", fg="#333")
label_start_year.grid(row=8, column=0, sticky="w", padx=5, pady=10)
entry_start_year = tk.Entry(frame, font=("Arial", 12))
entry_start_year.grid(row=8, column=1, padx=10, pady=10)

# 계산 버튼 스타일
button_calculate = tk.Button(frame, text="계산", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", command=calculate)
button_calculate.grid(row=9, column=0, columnspan=2, pady=20)

# 결과 출력 프레임
result_frame = tk.Frame(root, bg="#f9f9f9")
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
