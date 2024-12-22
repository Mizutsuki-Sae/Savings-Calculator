# Savings Calculator

이 프로그램는 사용자가 제공한 정보를 바탕으로 **복리 통장**, **적금 통장**, **예금 통장**의 최종 금액을 계산하는 **저축 통장 계산기**입니다. 각 통장에 대한 계산을 통해 세금 전후의 금액을 비교할 수 있습니다.


---


## 소개

- **복리 통장**: **매일 복리** 방식으로 이자를 계산합니다. 연 이자율을 **365일로 나누어** 일일 이자율을 구하고, 매일 원금에 이자를 더하여 누적됩니다.

- **적금 통장**: 매월 일정 금액을 예치하면서 **단리 이자**를 계산하여 최종 금액을 구합니다. 적금 통장은 **매월 고정된 금액을 추가**하면서 이자가 계산되며 이자 계산은 **단리** 방식입니다.

- **예금 통장**: 매월 일정 금액을 예치하는 예금 통장에서는 **단리 이자** 방식으로 이자를 계산합니다. 예금 통장은 적금과 비슷하지만, 이자 계산 방식이 다릅니다.


## 주요 기능

- **이자 계산**: 사용자가 입력한 개월 수 만큼의 총 이자를 계산해 보여줍니다.
- **총 금액 계산**: 만기 시의 받게될 금액을 계산하여 보여줍니다.
- **윤년 계산**: 2월의 날짜가 28일인지 29일인지를 판단하여 복리 계산에 반영합니다.
- **세금 적용**: 이자에 대해 **사용자가 입력한 세율**을 적용하여 세금 전후의 금액을 계산합니다.
- **3가지 통장 비교**: 복리, 적금, 예금 통장의 금액을 세금 전후로 비교하여 결과를 제공합니다.


---


## 사용자 입력 항목

- **처음 금액 (원)**: 초기 투자 금액
- **매달 저축할 금액 (원)**: 매월 예치할 금액
     - 매달 저축하는 금액이 없다면 0으로 입력하시면 됩니다.
- **연 이자율 (%)**: 각 통장의 연 이자율
- **세율 (%)**: 사용자에게 적용되는 세율 (기본 15.4%, 비과세는 0%)
     - 무조건 숫자를 입력하셔야 합니다.
- **저축 기간 (개월)**: 저축할 기간 (개월 단위)
- **시작 연도**: 저축 시작 연도


## 계산 결과

- **세금 적용 전** 금액과 **세금 적용 후** 금액을 별도의 박스에 표시하여 사용자가 쉽게 비교할 수 있도록 합니다.


---


## 사용 방법

1. 프로그램을 실행합니다.
   - Savings Calculator.exe와 Savings Calculator_.exe는 아이콘만 다르고 그 외에는 모두 같습니다.
2. 각 입력 필드에 필요한 정보를 입력합니다:
   - 처음 금액, 매달 저축할 금액, 연 이자율, 저축 기간, 시작 연도를 입력합니다.
3. "계산" 버튼을 클릭하여 결과를 확인합니다.
4. 세금 적용 전과 후의 금액을 비교하여 확인할 수 있습니다.


## License

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.


---


# 마치면서...

이 프로젝트는 2024년도에 고등학교 2학년인 제가 저축 관련 상품들을 서로 비교하기 편하도록 만들었습니다. 부족한 부분이 많을 것이라 예상합니다. 적절한 피드백은 더 좋은 결과를 만들어 나갑니다 :)
