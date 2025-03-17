import random

def generate_question():
    # 随机选择加法或减法
    operator = random.choice(['+', '-'])
    
    if operator == '+':
        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10 - num1)  # 保证和不超过 10
        answer = num1 + num2
    else:
        num1 = random.randint(0, 10)
        num2 = random.randint(0, num1)       # 保证结果不为负数
        answer = num1 - num2
    
    return f"{num1} {operator} {num2} = ", answer

# 新增：获取题目数量
while True:
    try:
        total_questions = int(input("请输入要练习的题目数量："))
        if total_questions > 0:
            break
        print("请输入大于 0 的正整数！")
    except ValueError:
        print("请输入有效的数字！")

# 修改主循环为有限次数
correct_count = 0
wrong_count = 0

for _ in range(total_questions):
    question, correct_answer = generate_question()
    
    while True:
        try:
            user_input = input(f"题目：{question}")
            user_answer = int(user_input)
            break
        except ValueError:
            print("请输入数字！")
    
    if user_answer == correct_answer:
        correct_count += 1  # 新增计数
        print("✅ 答对了，真棒！")
    else:
        wrong_count += 1    # 新增计数
        print(f"❌ 答错了，正确答案是：{correct_answer}")
    
    print("---")

print(f"练习结束！共练习了{total_questions}道题，答对了{correct_count}道，答错了{wrong_count}道。继续加油！")