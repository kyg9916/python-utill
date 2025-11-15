import random
import time
from collections import Counter  # 빈도수를 세기 위한 Counter 도구 임포트

# 등수별 상금 (현실 기준)
PRIZES = {
    1: 2000000000,
    2: 100000000,
    3: 1800000,
    4: 50000,
    5: 5000
}

# ------------------------------------------------------
# 💾 과거 당첨 번호 데이터 (통계 분석의 기반)
# ⚠️ 주의: 실제 데이터를 넣어서 사용해 주세요! 현재는 100회차 더미 데이터입니다.
# ------------------------------------------------------
INITIAL_PAST_WINNING_NUMBERS = [
    [1, 10, 15, 23, 30, 40], [2, 11, 16, 24, 31, 41], [3, 12, 17, 25, 32, 42], [4, 13, 18, 26, 33, 43],
    [5, 14, 19, 27, 34, 44],
    [6, 15, 20, 28, 35, 45], [7, 16, 21, 29, 36, 1], [8, 17, 22, 30, 37, 2], [9, 18, 23, 31, 38, 3],
    [10, 19, 24, 32, 39, 4],
    [11, 20, 25, 33, 40, 5], [12, 21, 26, 34, 41, 6], [13, 22, 27, 35, 42, 7], [14, 23, 28, 36, 43, 8],
    [15, 24, 29, 37, 44, 9],
    [16, 25, 30, 38, 45, 10], [17, 26, 31, 39, 1, 11], [18, 27, 32, 40, 2, 12], [19, 28, 33, 41, 3, 13],
    [20, 29, 34, 42, 4, 14],
    [21, 30, 35, 43, 5, 15], [22, 31, 36, 44, 6, 16], [23, 32, 37, 45, 7, 17], [24, 33, 38, 1, 8, 18],
    [25, 34, 39, 2, 9, 19],
    [26, 35, 40, 3, 10, 20], [27, 36, 41, 4, 11, 21], [28, 37, 42, 5, 12, 22], [29, 38, 43, 6, 13, 23],
    [30, 39, 44, 7, 14, 24],
    [31, 40, 45, 8, 15, 25], [32, 41, 1, 9, 16, 26], [33, 42, 2, 10, 17, 27], [34, 43, 3, 11, 18, 28],
    [35, 44, 4, 12, 19, 29],
    [36, 45, 5, 13, 20, 30], [37, 1, 6, 14, 21, 31], [38, 2, 7, 15, 22, 32], [39, 3, 8, 16, 23, 33],
    [40, 4, 9, 17, 24, 34],
    [41, 5, 10, 18, 25, 35], [42, 6, 11, 19, 26, 36], [43, 7, 12, 20, 27, 37], [44, 8, 13, 21, 28, 38],
    [45, 9, 14, 22, 29, 39],
    [1, 11, 15, 23, 33, 40], [2, 12, 16, 24, 34, 41], [3, 13, 17, 25, 35, 42], [4, 14, 18, 26, 36, 43],
    [5, 15, 19, 27, 37, 44],
    [6, 16, 20, 28, 38, 45], [7, 17, 21, 29, 39, 1], [8, 18, 22, 30, 40, 2], [9, 19, 23, 31, 41, 3],
    [10, 20, 24, 32, 42, 4],
    [11, 21, 25, 33, 43, 5], [12, 22, 26, 34, 44, 6], [13, 23, 27, 35, 45, 7], [14, 24, 28, 36, 1, 8],
    [15, 25, 29, 37, 2, 9],
    [16, 26, 30, 38, 3, 10], [17, 27, 31, 39, 4, 11], [18, 28, 32, 40, 5, 12], [19, 29, 33, 41, 6, 13],
    [20, 30, 34, 42, 7, 14],
    [21, 31, 35, 43, 8, 15], [22, 32, 36, 44, 9, 16], [23, 33, 37, 45, 10, 17], [24, 34, 38, 1, 11, 18],
    [25, 35, 39, 2, 12, 19],
    [26, 36, 40, 3, 13, 20], [27, 37, 41, 4, 14, 21], [28, 38, 42, 5, 15, 22], [29, 39, 43, 6, 16, 23],
    [30, 40, 44, 7, 17, 24],
    [31, 41, 45, 8, 18, 25], [32, 42, 1, 9, 19, 26], [33, 43, 2, 10, 20, 27], [34, 44, 3, 11, 21, 28],
    [35, 45, 4, 12, 22, 29],
    [36, 1, 5, 13, 23, 30], [37, 2, 6, 14, 24, 31], [38, 3, 7, 15, 25, 32], [39, 4, 8, 16, 26, 33],
    [40, 5, 9, 17, 27, 34],
    [41, 6, 10, 18, 28, 35], [42, 7, 11, 19, 29, 36], [43, 8, 12, 20, 30, 37], [44, 9, 13, 21, 31, 38],
    [45, 10, 14, 22, 32, 39]
]

# ------------------------------------------------------
# 🌟 시뮬레이션 데이터를 누적할 실제 리스트 🌟
# INITIAL_PAST_WINNING_NUMBERS의 내용을 복사하여 초기화합니다.
# 이 리스트에 매 시뮬레이션 당첨 번호가 추가됩니다.
# ------------------------------------------------------
PAST_WINNING_NUMBERS_ACCUMULATED = INITIAL_PAST_WINNING_NUMBERS[:]


# ------------------------------------------------------
# 🎨 터미널 디자인 요소 함수
# ------------------------------------------------------
def print_separator(char='=', length=60, title=None):
    """구분선 출력 함수"""
    if title:
        padding = (length - len(title) - 4) // 2
        korean_len = len(title.encode('utf-8')) - len(title)
        padding = (length - (len(title) + korean_len) - 4) // 2
        if padding < 0: padding = 0
        print(f"\n{char * padding} [ {title} ] {char * padding}")
    else:
        print(char * length)


def print_box(text_list, char='#'):
    """간단한 박스 형태 출력"""
    max_len = max(len(t.encode('utf-8')) for t in text_list)
    width = max_len + 4
    print(char * width)
    for text in text_list:
        encoded_len = len(text.encode('utf-8'))
        pad = max_len - encoded_len + len(text)
        print(f"{char} {text.ljust(pad)} {char}")
    print(char * width)


# ------------------------------------------------------
# 번호 생성 함수
# ------------------------------------------------------
def generate_lotto():
    """자동 번호 6개 생성 (순수 랜덤)"""
    return sorted(random.sample(range(1, 46), 6))


def generate_stat_lotto(top_n=15):
    """B 버튼 로직: 누적된 과거 데이터를 분석하여 상위 빈도수 N개 내에서 6개 추천"""
    # ⚠️ 누적된 PAST_WINNING_NUMBERS_ACCUMULATED를 사용합니다.
    current_data = PAST_WINNING_NUMBERS_ACCUMULATED

    if not current_data:
        # 안전 장치: 데이터가 없으면 순수 랜덤으로 대체
        print(" ⚠️ [경고] 누적 데이터가 없어 자동 번호로 대체합니다.")
        return generate_lotto()

    all_numbers = []
    # 모든 과거 당첨 번호를 하나의 리스트로 모읍니다.
    for nums in current_data:
        all_numbers.extend(nums)

    # 각 숫자가 몇 번 나왔는지 빈도수를 계산합니다.
    counts = Counter(all_numbers)

    # 1. 가장 많이 나온 상위 N개 (top_n=15)의 숫자 리스트를 만듭니다.
    # 만약 데이터가 너무 적어 15개 미만이면, 있는 숫자 모두를 풀로 사용
    most_frequent_pool = [item[0] for item in counts.most_common(top_n)]

    # 2. 풀의 크기가 6개 미만이면 나머지 숫자로 채워서 6개로 만듭니다. (안전 장치)
    if len(most_frequent_pool) < 6:
        print(" ⚠️ [경고] 분석된 고빈도 숫자가 6개 미만입니다. 랜덤으로 채웁니다.")
        return generate_lotto()  # 이 경우는 순수 랜덤으로 안전하게 대체

    # 3. 상위 빈도 풀(most_frequent_pool)에서 무작위로 6개 선택합니다.
    final_nums = sorted(random.sample(most_frequent_pool, 6))

    return final_nums


def get_manual_lotto(index):
    """사용자가 직접 6개를 입력 (수동 모드)"""
    print_separator('-', 40, f"🎟️ {index}번째 수동 번호 입력")
    nums = set()

    while len(nums) < 6:
        try:
            num = int(input(f" 👉 {len(nums) + 1}/6번째 숫자 입력 (1~45): "))
            if not (1 <= num <= 45):
                print(" ⚠️ [ERROR] 1~45 숫자만 입력 가능합니다.")
                continue
            if num in nums:
                print(" ⚠️ [ERROR] 중복 숫자입니다.")
                continue
            nums.add(num)
        except ValueError:
            print(" ⚠️ [ERROR] 숫자로 입력해주세요.")

    print(f" ✅ 수동 입력 완료! 번호: {sorted(nums)}")
    print('-' * 40)
    return sorted(nums)


def get_semi_auto_lotto(index):
    """반자동 기능: 일부는 수동 + 나머지는 자동"""
    print_separator('-', 40, f"🎟️ {index}번째 반자동 설정")

    while True:
        try:
            manual_count = int(input(" ✍️ 수동으로 입력할 개수 (0~5): "))
            if 0 <= manual_count <= 5:
                break
            print(" ⚠️ [ERROR] 0~5 사이 숫자만 입력해주세요.")
        except ValueError:
            print(" ⚠️ [ERROR] 숫자로 입력해주세요.")

    nums = set()

    # 수동 입력
    for i in range(manual_count):
        while True:
            try:
                n = int(input(f" ✏️ {i + 1}번째 수동 입력 숫자: "))
                if not (1 <= n <= 45):
                    print(" ⚠️ [ERROR] 1~45 숫자만 입력 가능합니다.")
                    continue
                if n in nums:
                    print(" ⚠️ [ERROR] 중복 숫자입니다.")
                    continue
                nums.add(n)
                break
            except ValueError:
                print(" ⚠️ [ERROR] 숫자로 입력해주세요.")

    # 자동 생성
    remain = 6 - len(nums)
    if remain > 0:
        auto_nums = random.sample([n for n in range(1, 46) if n not in nums], remain)
        nums.update(auto_nums)

    final = sorted(nums)
    print(f"\n 🎉 **최종 로또 번호** (수동 {manual_count}개 + 자동 {remain}개): {final}")
    print('-' * 40)
    return final


# ------------------------------------------------------
# 등수 체크
# ------------------------------------------------------
def check_rank(buy_nums, win_nums, bonus):
    """정확한 로또 규칙 적용"""
    match = len(set(buy_nums) & set(win_nums))

    if match == 6:
        return 1
    if match == 5 and bonus in buy_nums:
        return 2
    if match == 5:
        return 3
    if match == 4:
        return 4
    if match == 3:
        return 5

    return 0


# ------------------------------------------------------
# 메인 시작
# ------------------------------------------------------
# 🎨 시작 화면 디자인
print_box(["", "💰 로또 시뮬레이션 프로그램 💰", "  - 개발자 김윤겸 -  ", ""], char='=')
print("\n[프로그램 안내]")
print("로또 구매 -> 당첨 확인 -> 총 수익 계산 시뮬레이션입니다.\n")
username = input("사용자님의 이름을 입력해주세요: ")

print_separator('~', 30, f"{username}님 환영합니다!")

# 초기 자금 입력
while True:
    try:
        inp = input("💵 당신의 현재 가진 돈을 입력해주세요 (미입력 시 100,000원): ")
        if inp == "":
            money = 100000
            print("  ➡️ 금액이 입력되지 않아 기본값 100,000원으로 설정되었습니다.")
            break
        money = int(inp)
        if money >= 0:
            break
        print(" ⚠️ [ERROR] 0원 이상 입력해주세요.")
    except ValueError:
        print(" ⚠️ [ERROR] 숫자만 입력해주세요.")

# 누적 통계 변수 초기화
total_spent = 0
total_winnings = 0
total_rank_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 0: 0}

# ------------------------------------------------------
# 게임 루프
# ------------------------------------------------------
while True:
    print_separator('=', 60, "현재 상태")
    print(f"💰 현재 잔액: {money: >15,}원")
    print(f"💸 총 지출액: {total_spent: >15,}원")
    print_separator('=')

    # ---------------------- 💵 상시 충전 기능 ----------------------
    print_separator('~', 60, "잔액 충전")

    while True:
        ask = input("돈을 충전하시겠습니까? (Y/N): ").upper()
        if ask in ["Y", "N"]:
            break
        print(" ⚠️ [ERROR] Y 또는 N을 입력해주세요.")

    if ask == "Y":
        while True:
            try:
                add = int(input("➕ 충전 금액 입력: "))
                if add >= 0:
                    money += add
                    print(f"✅ 충전 완료! 현재 잔액: {money:,}원")
                    break
                print(" ⚠️ [ERROR] 0원 이상 입력해주세요.")
            except ValueError:
                print(" ⚠️ [ERROR] 숫자로 입력해주세요.")
    else:
        print("충전하지 않고 로또 구매를 진행합니다.")
    print_separator('-')
    # ---------------------- 💵 상시 충전 기능 끝 ----------------------

    # ---------------------- 구매 모드 선택 (종료 버튼 추가) ----------------------
    mode_type = None  # mode_type 초기화

    while True:
        # [X], [B] 옵션이 추가된 메뉴 출력
        mode = input("\n[🎟️ 로또 구매 모드 선택]\n"
                     "  숫자 : 자동 구매 수량\n"
                     "  P    : 수동 모드\n"
                     "  S    : 반자동 모드\n"
                     "  B    : 번호 예측 모드 (누적 빈도 기반)\n"  # <-- 예측 모드 추가
                     "  X    : 프로그램 종료\n"
                     "  입력 : ").upper()

        # [X] 종료 모드 처리
        if mode == "X":
            mode_type = "exit"
            break

        # [P], [S], [B] 모드 처리
        if mode in ["P", "S", "B"]:
            if mode == "P":
                mode_name = "수동"
                mode_key = "manual"
            elif mode == "S":
                mode_name = "반자동"
                mode_key = "semi"
            else:  # mode == "B"
                mode_name = "번호 예측"
                mode_key = "stat_rec"  # 새로운 예측 모드 키

            try:
                count = int(input(f"  ➡️ {mode_name} 로또 구매 장수 입력: "))
                if count > 0:
                    mode_type = mode_key
                    break
                print(" ⚠️ [ERROR] 1장 이상 입력해주세요.")
            except ValueError:
                print(" ⚠️ [ERROR] 숫자로 입력해주세요.")
            continue

        # 자동 모드
        try:
            count = int(mode)
            if count > 0:
                mode_type = "auto"
                break
            print(" ⚠️ [ERROR] 1장 이상 입력해주세요.")
        except ValueError:
            # 오류 메시지에 'X', 'B' 추가 안내
            print(" ⚠️ [ERROR] 잘못된 입력입니다. 1이상의 숫자/P/S/B/X 중 하나를 입력해주세요.")
            continue

    # [X] 종료 처리 확인 및 메인 루프 종료
    if mode_type == "exit":
        print("\n프로그램을 종료합니다. 감사합니다! 👋")
        time.sleep(1)
        break  # 메인 while True 루프를 빠져나감
    # ---------------------- 구매 모드 선택 끝 ----------------------

    # ---------------------- 구매 진행 ----------------------
    price = count * 1000

    if price > money:
        print(f"\n❌ **잔액 부족!** 현재 잔액: {money:,}원. 구매 장수를 줄이거나 충전해주세요.")
        continue

    money -= price
    total_spent += price

    print_separator('=', 40, "구매 결과")
    print(f" ✅ 로또 {count}장 구매 완료! (지출: {price:,}원)")
    print(f" ➡️ 남은 돈: {money:,}원")
    print_separator('=')

    # ---------------------- 번호 생성 ----------------------
    bought = []

    for i in range(1, count + 1):
        if mode_type == "auto":
            nums = generate_lotto()
            print(f" {i: >3}번째 로또 (자동): {nums}")
            bought.append(nums)
        elif mode_type == "manual":
            nums = get_manual_lotto(i)
            bought.append(nums)
        elif mode_type == "semi":
            nums = get_semi_auto_lotto(i)
            bought.append(nums)
        elif mode_type == "stat_rec":  # <-- B (번호 예측) 모드 처리
            nums = generate_stat_lotto()
            print(f" {i: >3}번째 로또 (통계 예측): {nums}")
            bought.append(nums)

    # ---------------------- 당첨 확인 ----------------------
    while True:
        yn = input("\n🏆 당첨 결과를 확인하시겠습니까? (Y/N): ").upper()
        if yn in ["Y", "N"]:
            break
        print(" ⚠️ [ERROR] Y 또는 N을 입력해주세요.")

    if yn == "N":
        print("당첨 결과를 확인하지 않고 다음 구매로 넘어갑니다.\n")
    else:
        # 당첨 번호 생성
        win_nums = generate_lotto()
        bonus = random.choice([n for n in range(1, 46) if n not in win_nums])

        # --------------------------------------------------
        # 🌟 데이터 누적 로직: 이번 회차 당첨 번호를 누적 리스트에 추가 🌟
        # --------------------------------------------------
        PAST_WINNING_NUMBERS_ACCUMULATED.append(win_nums)
        # --------------------------------------------------

        print_box([
            "                 ",
            "  🎉 이번 주 당첨 결과 🎉 ",
            f"  당첨 번호  : {win_nums} ",
            f"  보너스 번호: {bonus} ",
            "                 "
        ], char='*')

        for idx, nums in enumerate(bought, 1):
            rank = check_rank(nums, win_nums, bonus)
            total_rank_counts[rank] += 1

            rank_info = f" {idx: >3}번째 로또 {nums}: "
            if rank == 0:
                print(f"{rank_info} ❌ 꽝 (0원)")
            else:
                prize = PRIZES[rank]
                money += prize
                total_winnings += prize
                symbol = "🌟" if rank <= 2 else "✨"
                print(f"{rank_info} {symbol} **{rank}등 당첨!** {prize: >15,}원 획득!")

        print_separator('-')
        print(f"💰 현재 잔액 총합: {money:,}원")
        print_separator('-')

    # ---------------------- Q/Y/N 선택 ----------------------
    while True:
        again = input("\n[다음 행동 선택]   다시 구매(Y)   중간 정산(Q)   종료(N): ").upper()
        if again in ["Y", "N", "Q"]:
            break
        print(" ⚠️ [ERROR] Y, N, Q 중 하나를 입력해주세요.")

    if again == "Q":
        profit = total_winnings - total_spent
        print_separator('#', 60, "중간 정산 누적 결과")
        print(f" 💸 총 소비 금액   : {total_spent: >15,}원")
        print(f" 💰 총 당첨 금액   : {total_winnings: >15,}원")
        print(f" 🟢 현재 잔액     : {money: >15,}원")

        sign = "+" if profit >= 0 else ""
        print(f" 📊 **손익** : {sign}{profit: >15,}원")
        print_separator('#', 60)
        continue

    if again == "N":
        print("\n\n프로그램 종료를 준비합니다...")
        time.sleep(2)
        break

    continue

# ------------------------------------------------------
# 🏆 최종 결과 출력 및 당첨 통계 (수정된 부분)
# ------------------------------------------------------
profit = total_winnings - total_spent

print_box([
    "                                                 ",
    "       🚀 최종 로또 시뮬레이션 결과 🚀       ",
    "                                                 ",
    f"  총 소비 금액     : {total_spent: >15,}원  ",
    f"  총 당첨 금액     : {total_winnings: >15,}원  ",
    f"  최종 잔액        : {money: >15,}원  ",
    "  -----------------------------------------------  ",
    # 형식 지정자 수정: 콜론 뒤에 쉼표(,)를 제거하고, 마지막에 추가
    f"  ✨ 최종 손익 : {profit:>+15,}원  ",
    "                                                 "
], char='*')

print("\n")
print_separator('=', 60, "🏆 당첨 횟수 상세 통계")
total_tickets = sum(total_rank_counts.values())

for rank in sorted(total_rank_counts.keys(), reverse=True):
    count = total_rank_counts[rank]
    if count == 0:
        continue

    if rank == 0:
        spent_amount = count * 1000
        print(f"  ❌ 꽝 횟수 ({count / total_tickets * 100:.2f}%)  : {count: >5,}회 (총 {spent_amount: >12,}원 소모)")
    else:
        prize_per_ticket = PRIZES[rank]
        total_prize_for_rank = count * prize_per_ticket
        print(
            f"  🥇 {rank}등 당첨 횟수  ({count / total_tickets * 100:.2f}%) : {count: >5,}회 (총 {total_prize_for_rank: >12,}원 획득)")

print_separator('=', 60)
print(f"  총 구매 로또 장수: {total_tickets:,}장")
print_separator('=')

print("\n프로그램을 완전히 종료합니다. 굿바이! 👋")
time.sleep(5)