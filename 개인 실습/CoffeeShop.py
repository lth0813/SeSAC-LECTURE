import random

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
                break
            elif drink_choice.isdigit() and 1 <= int(drink_choice) <= 6:
                self.selected_drink = menu_list[int(drink_choice) - 1][1]
                self.select_option()
            else:
                print("잘못 선택하셨습니다. 다시 선택해주세요.")

    def select_option(self):
        print(f"선택하신 메뉴는 {self.selected_drink}입니다.")
        print(f'가격은 {self.menu[self.selected_drink][0]}원 입니다.')
        select_size = input("사이즈를 선택해주세요.")
        print("1. SMALL")
        print("2. MEDIUM")
        print("3. LARGE")
        print("4. 음료 다시 선택하기")
        select_temperature = input("옵션을 선택해주세요.")
        print("1. ICED")
        print("2. HOT")
        print("3. 사이즈 다시 선택하기")
        select_pay = input("다음 행동을 선택해주세요.")
        print("1. 결제하기")
        print("2. 장바구니 담기")
        print("3. 주문 취소")

    def start(self):
        while True:
            print("\n======== SeSAC Coffee Shop ========")
            print("1. 주문하기")
            print("2. 종료")
            choice = input("메뉴를 선택해주세요.")
            
            if choice == "1":
                self.display_menu()
            elif choice == "2":
                print("키오스크를 종료합니다. 감사합니다!")
                break
            else:
                print("잘못 선택하셨습니다. 다시 선택해주세요.")

coffee_shop = CoffeeShop()
coffee_shop.start()
