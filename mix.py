import random
import tkinter as tk
from tkinter import messagebox
from functools import partial

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
        self.operations = []
        self.num_min = 0
        self.num_max = 10
        self.operators = {'+': '加法', '-': '减法', '×': '乘法', '÷': '除法'}

    def _create_widgets(self):
        self.main_frame = tk.Frame(self.window, padx=self.styles['padding'], 
                                 pady=self.styles['padding'])
        self.main_frame.pack(expand=True)
        self._create_settings_panel()
        self._create_quiz_interface()

    def _create_settings_panel(self):
        self.settings_frame = tk.Frame(self.main_frame)
        self.settings_frame.pack(pady=10)
        
        # 数字范围设置
        tk.Label(self.settings_frame, text="数字范围：", font=self.styles['font_medium']).grid(row=0, column=0)
        self.min_entry = tk.Entry(self.settings_frame, width=5, font=self.styles['font_medium'])
        self.min_entry.insert(0, "0")
        self.min_entry.grid(row=0, column=1)
        tk.Label(self.settings_frame, text="-", font=self.styles['font_medium']).grid(row=0, column=2)
        self.max_entry = tk.Entry(self.settings_frame, width=5, font=self.styles['font_medium'])
        self.max_entry.insert(0, "10")
        self.max_entry.grid(row=0, column=3)

        # 运算类型选择
        self.ops_frame = tk.LabelFrame(self.settings_frame, text="运算类型", font=self.styles['font_medium'])
        self.ops_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.ops_vars = {}
        for i, (op, name) in enumerate(self.operators.items()):
            var = tk.BooleanVar(value=(op in ['+', '-']))
            self.ops_vars[op] = var
            cb = tk.Checkbutton(self.ops_frame, text=name, variable=var, 
                              font=self.styles['font_medium'])
            cb.grid(row=0, column=i, padx=5)

        # 题目数量设置
        tk.Label(self.settings_frame, text="题目数量：", font=self.styles['font_medium']).grid(row=2, column=0)
        self.num_entry = tk.Entry(self.settings_frame, width=5, font=self.styles['font_medium'])
        self.num_entry.grid(row=2, column=1)
        tk.Button(self.settings_frame, text="开始练习", command=self.start_quiz, 
                font=self.styles['font_medium']).grid(row=2, column=3, padx=10)

    def _create_quiz_interface(self):
        self.quiz_frame = tk.Frame(self.main_frame)
        self.question_label = tk.Label(self.quiz_frame, font=self.styles['font_large'])
        self.answer_entry = tk.Entry(self.quiz_frame, font=self.styles['font_large'], width=10)
        self.answer_entry.bind('<Return>', self.check_answer)
        self.submit_btn = tk.Button(self.quiz_frame, text="提交答案", 
                                  command=self.check_answer, font=self.styles['font_medium'])
        self.status_label = tk.Label(self.quiz_frame, font=self.styles['font_medium'])

    def start_quiz(self):
        # 验证运算类型选择
        self.operations = [op for op, var in self.ops_vars.items() if var.get()]
        if not self.operations:
            messagebox.showerror("错误", "请至少选择一种运算类型")
            return

        # 验证数字范围
        try:
            self.num_min = int(self.min_entry.get())
            self.num_max = int(self.max_entry.get())
            if self.num_min < 0 or self.num_max <= self.num_min:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字范围")
            return

        # 验证题目数量
        input_val = self.num_entry.get()
        if not input_val.isdigit() or (total := int(input_val)) <= 0:
            messagebox.showerror("输入错误", "请输入有效的正整数")
            return
            
        self.total_questions = int(input_val)
        self.current_question = 0
        self.correct_count = 0
        self.wrong_count = 0
        
        self.settings_frame.pack_forget()
        self._show_quiz_interface()

    def _show_quiz_interface(self):
        self.quiz_frame.pack(expand=True)
        self.question_label.pack(pady=10)
        self.answer_entry.pack(pady=5)
        self.submit_btn.pack(pady=5)
        self.status_label.pack(pady=10)
        self.answer_entry.focus_set()
        self.next_question()

    def next_question(self):
        if self.current_question >= self.total_questions:
            self.show_results()
            return
            
        self.current_question += 1
        question, self.correct_answer = self.generate_question()
        self.question_label.config(text=f"第 {self.current_question} 题：{question}")
        self.answer_entry.delete(0, tk.END)
        self._update_status()

    def generate_question(self):
        operator = random.choice(self.operations)
        
        if operator == '+':
            num1 = random.randint(self.num_min, self.num_max)
            num2 = random.randint(self.num_min, self.num_max - num1)
            return f"{num1} + {num2} = ", num1 + num2
        elif operator == '-':
            num1 = random.randint(self.num_min, self.num_max)
            num2 = random.randint(self.num_min, num1)
            return f"{num1} - {num2} = ", num1 - num2
        elif operator == '×':
            num1 = random.randint(self.num_min, self.num_max)
            num2 = random.randint(self.num_min, self.num_max)
            return f"{num1} × {num2} = ", num1 * num2
        else:  # 除法
            divisor = random.randint(1, self.num_max)
            dividend = divisor * random.randint(0, self.num_max // max(1, divisor))
            return f"{dividend} ÷ {divisor} = ", dividend // divisor

    def check_answer(self, event=None):
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
        status_text = (
            f"进度：{self.current_question}/{self.total_questions} | "
            f"正确：{self.correct_count} | "
            f"错误：{self.wrong_count}"
        )
        self.status_label.config(text=status_text)

    def show_results(self):
        messagebox.showinfo(
            "练习结束",
            f"完成总数：{self.total_questions}\n"
            f"正确题目：{self.correct_count}\n"
            f"错误题目：{self.wrong_count}"
        )
        self.window.destroy()

    def _on_close(self):
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            self.window.destroy()

if __name__ == "__main__":
    MathQuizApp()
