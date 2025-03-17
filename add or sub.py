import random
import tkinter as tk
from tkinter import messagebox

class MathQuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("数学小练习")
        self._init_styles()
        self._init_vars()
        self._create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self.window.mainloop()

    def _init_styles(self):
        self.styles = {
            'font_large': ('Microsoft YaHei', 14),
            'font_medium': ('Microsoft YaHei', 12),
            'color_correct': '#4CAF50',
            'color_wrong': '#F44336',
            'padding': 20
        }

    def _init_vars(self):
        self.total_questions = 0
        self.current_question = 0
        self.correct_count = 0
        self.wrong_count = 0

    def _create_widgets(self):
        self.main_frame = tk.Frame(self.window, padx=self.styles['padding'], 
                                 pady=self.styles['padding'])
        self.main_frame.pack(expand=True)
        self._create_question_input()
        self._create_quiz_interface()

    def _create_question_input(self):
        self.input_frame = tk.Frame(self.main_frame)  # 改为实例变量
        self.input_frame.pack(pady=10)
        
        tk.Label(self.input_frame, text="题目数量：", font=self.styles['font_medium']).pack(side=tk.LEFT)
        self.num_entry = tk.Entry(self.input_frame, width=5, font=self.styles['font_medium'])
        self.num_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.input_frame, text="开始练习", command=self.start_quiz, 
                font=self.styles['font_medium']).pack(side=tk.LEFT)

    def _create_quiz_interface(self):
        self.question_label = tk.Label(self.main_frame, font=self.styles['font_large'])
        self.answer_entry = tk.Entry(self.main_frame, font=self.styles['font_large'], width=10)
        self.answer_entry.bind('<Return>', self.check_answer)
        self.submit_btn = tk.Button(self.main_frame, text="提交答案", 
                                  command=self.check_answer, font=self.styles['font_medium'])
        self.status_label = tk.Label(self.main_frame, font=self.styles['font_medium'])

    def start_quiz(self):
        input_val = self.num_entry.get()
        if not input_val.isdigit() or (total := int(input_val)) <= 0:
            messagebox.showerror("输入错误", "请输入有效的正整数")
            return
            
        self.total_questions = int(input_val)
        self.input_frame.pack_forget()  # 隐藏输入组件
        self._show_quiz_interface()
        self.next_question()

    def _show_quiz_interface(self):
        self.question_label.pack(pady=10)
        self.answer_entry.pack(pady=5)
        self.submit_btn.pack(pady=5)
        self.status_label.pack(pady=10)
        self.answer_entry.focus_set()

    def next_question(self):
        """生成下一题"""
        if self.current_question >= self.total_questions:
            self.show_results()
            return
            
        self.current_question += 1
        question, self.correct_answer = generate_question()
        self.question_label.config(text=f"第 {self.current_question} 题：{question}")
        self.answer_entry.delete(0, tk.END)
        self._update_status()

    def check_answer(self, event=None):
        """检查答案"""
        answer = self.answer_entry.get()
        if not answer.isdigit():
            messagebox.showerror("输入错误", "请输入有效数字")
            return
            
        user_answer = int(answer)
        if user_answer == self.correct_answer:
            self.correct_count += 1
            self.status_label.config(fg=self.styles['color_correct'])
        else:
            self.wrong_count += 1
            self.status_label.config(fg=self.styles['color_wrong'])
            
        self._update_status()
        self.next_question()

    def _update_status(self):
        """更新状态显示"""
        status_text = (
            f"进度：{self.current_question-1}/{self.total_questions} | "
            f"正确：{self.correct_count} | "
            f"错误：{self.wrong_count}"
        )
        self.status_label.config(text=status_text)

    def show_results(self):
        """显示最终结果"""
        messagebox.showinfo(
            "练习结束",
            f"完成总数：{self.total_questions}\n"
            f"正确题目：{self.correct_count}\n"
            f"错误题目：{self.wrong_count}"
        )
        self.window.destroy()

    def _on_close(self):
        """关闭窗口确认"""
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            self.window.destroy()

def generate_question():
    operator = random.choice(['+', '-'])
    if operator == '+':
        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10 - num1)
        return f"{num1} + {num2} = ", num1 + num2
    else:
        num1 = random.randint(0, 10)
        num2 = random.randint(0, num1)
        return f"{num1} - {num2} = ", num1 - num2

if __name__ == "__main__":
    MathQuizApp()