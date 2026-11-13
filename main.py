import json
import os
import sys

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    def __init__(self):
        self.filepath = 'state.json'
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def setup_default_quizzes(self):
        default_data = [
            Quiz("모나리자를 그린 르네상스 시대의 화가는?", ["미켈란젤로", "레오나르도 다빈치", "라파엘로", "도나텔로"], 2),
            Quiz("빛의 변화를 포착하려 했던 '인상주의'를 대표하며 '인상, 해돋이'를 그린 화가는?", ["클로드 모네", "빈센트 반 고흐", "에두아르 마네", "폴 세잔"], 1),
            Quiz("달걀 노른자를 안료와 섞어 그리는 고전적인 회화 기법은?", ["유화", "수채화", "템페라", "프레스코"], 3),
            Quiz("우리나라 전통 목조 건축물에 단청을 칠할 때 뼈대가 되는 밑그림을 뜻하는 용어는?", ["초빛", "출초", "가칠", "타초"], 2),
            Quiz("종이나 비단에 그려진 오래된 동양 회화를 복원할 때, 오염물을 제거하고 결손부를 메우는 과정은?", ["배첩", "제본", "장황", "포수"], 3)
        ]
        self.quizzes.extend(default_data)
        self.save_data()

    def load_data(self):
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quizzes = [Quiz.from_dict(q) for q in data.get('quizzes', [])]
                    self.best_score = data.get('best_score', 0)
            if not self.quizzes:
                self.setup_default_quizzes()
        except (json.JSONDecodeError, Exception) as e:
            print(f"데이터 파일을 읽는 중 오류가 발생했습니다. 기본 퀴즈로 초기화합니다. ({e})")
            self.setup_default_quizzes()

    def save_data(self):
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score
            }
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"데이터 저장 중 오류가 발생했습니다: {e}")

    def get_valid_input(self, prompt, min_val, max_val):
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                print("입력값이 비어있습니다. 다시 입력해주세요.")
                continue
            try:
                choice = int(user_input)
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f"{min_val}에서 {max_val} 사이의 숫자를 입력하세요.")
            except ValueError:
                print("잘못된 입력입니다. 숫자를 입력하세요.")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
            return

        print(f"\n퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        print("-" * 40)
        current_score = 0

        for i, q in enumerate(self.quizzes, 1):
            print(f"[{i}번 문제] {q.question}")
            for idx, choice in enumerate(q.choices, 1):
                print(f"  {idx}. {choice}")
            
            user_answer = self.get_valid_input("정답 입력 (1-4): ", 1, 4)
            if user_answer == q.answer:
                print("정답입니다!\n")
                current_score += 1
            else:
                print(f"오답입니다. 정답은 {q.answer}번입니다.\n")

        print("=" * 40)
        print(f"결과: {len(self.quizzes)}문제 중 {current_score}문제 정답!")
        
        if current_score > self.best_score:
            print("새로운 최고 점수입니다!")
            self.best_score = current_score
            self.save_data()
        print("=" * 40)

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("문제가 비어있어 취소되었습니다.")
            return

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if choice:
                    choices.append(choice)
                    break
                print("선택지 내용은 비어있을 수 없습니다.")

        answer = self.get_valid_input("정답 번호 (1-4): ", 1, 4)
        
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_data()
        print("퀴즈가 추가되었습니다!")

    def show_list(self):
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, q in enumerate(self.quizzes, 1):
            print(f"[{i}] {q.question}")
        print("-" * 40)

    def show_best_score(self):
        print(f"\n역대 최고 점수: {self.best_score}점")

    def run(self):
        while True:
            print("\n========================================")
            print("          미술사 & 복원 퀴즈 게임          ")
            print("========================================")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 점수 확인")
            print("5. 종료")
            print("========================================")
            
            try:
                choice = self.get_valid_input("선택: ", 1, 5)
                
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_list()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    print("게임을 종료합니다. 감사합니다!")
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n\n비정상 종료가 감지되었습니다. 데이터를 안전하게 저장하고 게임을 종료합니다.")
                self.save_data()
                sys.exit(0)

if __name__ == "__main__":
    game = QuizGame()
    game.run()