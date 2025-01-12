class CoffeeShop:
    def __init__(self):
        self.inventory = {
            "커피액": 300,
            "물": 300,
            "우유": 300,
            "얼음": 300,
            "초콜릿 시럽": 300,
            "오렌지 퓨레": 300,
            "딸기 퓨레": 300,
            "자몽 퓨레": 300,
            "시럽": 300,
            "설탕": 300,
            "사이다": 300
        }
        self.menu = {
            "아메리카노": [2500, "물", "커피액", "얼음"],
            "카페라떼": [3000, "우유", "커피액", "얼음"],
            "카페모카": [3500, "우유", "커피액", "초콜릿 시럽", "얼음"],
            "오렌지에이드": [4000, "오렌지 퓨레", "시럽", "설탕", "사이다", "얼음"],
            "딸기에이드": [4000, "딸기 퓨레", "시럽", "설탕", "사이다", "얼음"],
            "자몽에이드": [4000, "자몽 퓨레", "시럽", "설탕", "사이다", "얼음"]
        }
        self.order_queue = []
        self.waiting_number = 0
        self.cart = []  # 장바구니
        self.messages = [
            "감사합니다! 맛있게 드세요!",
            "오늘도 좋은 하루 되세요!",
            "항상 찾아주셔서 고맙습니다!",
            "최선을 다해 준비했습니다!",
            "행복한 시간이 되시길 바랍니다!"
        ]

    def display_menu(self):
        menu_list = list(enumerate(self.menu.keys()))
        while True:
            for drink in menu_list:
                print(f'{int(drink[0])+1}. {drink[1]}')
            print("7. 이전 메뉴로 돌아가기")
            drink_choice = input("음료를 선택해주세요.")
            if drink_choice == "7":
                return
            elif drink_choice.isdigit() and 1 <= int(drink_choice) <= 6:
                self.selected_drink = menu_list[int(drink_choice) - 1][1]
                if "에이드" in self.selected_drink:
                    self.select_size(is_aid=True)
                else:
                    self.select_size()
            else:
                print("잘못 선택하셨습니다. 다시 선택해주세요.")

    def select_size(self, is_aid=False):
        while True:
            print(f"선택하신 메뉴는 {self.selected_drink}입니다.")
            print(f'가격은 {self.menu[self.selected_drink][0]}원 입니다.')
            print("1. SMALL")
            print("2. MEDIUM")
            print("3. LARGE")
            print("4. 음료 다시 선택하기")
            select_size = input("사이즈를 선택해주세요.")
            if select_size == "4":
                return
            elif select_size in ["1", "2", "3"]:
                if is_aid:
                    self.cart.append(f"{self.selected_drink} (ICED)")
                    print(f"{self.selected_drink} (ICED)이(가) 장바구니에 담겼습니다.")
                    self.select_pay()
                else:
                    self.select_temperature()
                return
            else:
                print("잘못 선택하셨습니다. 다시 선택해주세요.")

    def select_temperature(self):
        while True:
            print("1. ICED")
            print("2. HOT")
            print("3. 사이즈 다시 선택하기")
            select_temperature = input("옵션을 선택해주세요.")

            if select_temperature == "3":
                return
            elif select_temperature == "1":
                self.cart.append(f"{self.selected_drink} (ICED)")
                print(f"{self.selected_drink} (ICED)이(가) 장바구니에 담겼습니다.")
                self.select_pay()
                return
            elif select_temperature == "2":
                self.cart.append(f"{self.selected_drink} (HOT)")
                print(f"{self.selected_drink} (HOT)이(가) 장바구니에 담겼습니다.")
                self.select_pay()
                return
            else:
                print("잘못 선택하셨습니다. 다시 선택해주세요.")

    def select_pay(self):
        while True:
            print("1. 결제하기")
            print("2. 주문 계속하기")
            print("3. 주문 취소")
            select_pay = input("다음 행동을 선택해주세요.")
            if select_pay == "3":
                self.cart.pop()
                print("주문이 취소되었습니다.")
                return
            elif select_pay == "1":
                self.process_payment()
                return
            elif select_pay == "2":
                print("다음 주문을 선택해주세요.")
                return
            else:
                print("잘못 선택하셨습니다. 다시 선택해주세요.")

    def process_payment(self):
        total_price = sum(self.menu[item.split(" (")[0]][0] for item in self.cart)
        print("\n결제 내역:")
        for item in self.cart:
            print(f"- {item}: {self.menu[item.split(' (')[0]][0]}원")
        print(f"총 금액: {total_price}원")

        # 재고 감소 처리
        for item in self.cart:
            base_item = item.split(" (")[0]
            is_hot = "HOT" in item
            for ingredient in self.menu[base_item][1:]:
                if ingredient == "얼음" and is_hot:
                    continue
                if self.inventory[ingredient] >= 50:  # 재료 소모량 가정: 각 50
                    self.inventory[ingredient] -= 50
                else:
                    print(f"재료 {ingredient}가 부족합니다. 주문이 취소됩니다.")
                    return

        self.waiting_number += 1
        print(f"대기번호 {self.waiting_number}번입니다. {self.messages[self.waiting_number % len(self.messages)]}")
        self.cart.clear()

    def start(self):
        while True:
            print("\n======== SeSAC Coffee Shop ========")
            print("1. 주문하기")
            print("2. 장바구니 확인")
            print("3. 재료 확인")
            print("4. 종료")
            choice = input("메뉴를 선택해주세요.")
            if choice == "1":
                self.display_menu()
            elif choice == "2":
                if self.cart:
                    print("\n장바구니:")
                    for item in self.cart:
                        print(f"- {item}: {self.menu[item.split(' (')[0]][0]}원")
                    if input("결제하시겠습니까? (y/n): ") == "y":
                        self.process_payment()
                else:
                    print("장바구니가 비어 있습니다.")
            elif choice == "3":
                print("\n남은 재료량:")
                for ingredient, amount in self.inventory.items():
                    unit = "ml" if ingredient in ["커피액", "물", "우유", "사이다"] else "g"
                    print(f"- {ingredient}: {amount}{unit}")
            elif choice == "4":
                print("키오스크를 종료합니다. 감사합니다!")
                break
            else:
                print("잘못 선택하셨습니다. 다시 선택해주세요.")

coffee_shop = CoffeeShop()
coffee_shop.start()
