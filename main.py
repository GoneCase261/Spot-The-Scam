import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json

# Set dark theme and blue colors globally
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def load_quiz_data(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        messagebox.showerror("ERROR", "FILE NOT FOUND")
        exit(1)
    except json.JSONDecodeError:
        messagebox.showerror("ERROR", "INVALID JSON")
        exit(1)


quiz_data = load_quiz_data("data.json")


class SpotTheScam:
    def __init__(self, root):
        self.root = root
        self.root.title("Spot the Scam Quiz")
        self.root.geometry("900x900")
        self.root.resizable(True, True)

        self.score = 0
        self.q_no = 0
        self.main_frame = ctk.CTkFrame(root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.home_page()

    def screen_refresh(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def home_page(self):
        self.screen_refresh()

        # Title
        title = ctk.CTkLabel(self.main_frame, text="🚨 SPOT THE SCAM QUIZ 🚨",
                             font=ctk.CTkFont(size=36, weight="bold"))
        title.pack(pady=(50, 20))

        # Subtitle with cyber theme
        subtitle = ctk.CTkLabel(self.main_frame,
                                text="Read the message carefully and decide: SCAM or LEGIT?",
                                font=ctk.CTkFont(size=18), text_color="#ff6b6b")
        subtitle.pack(pady=10)

        # Start button with hover effects
        start_btn = ctk.CTkButton(self.main_frame, text="🚀 START QUIZ",
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  height=60, fg_color="#00d4aa", hover_color="#00b894",
                                  command=self.quiz_start)
        start_btn.pack(pady=50)

    def quiz_start(self):
        self.score = 0
        self.q_no = 0
        self.disp_q()

    def disp_q(self):
        self.screen_refresh()

        # Progress header
        prog_text = ctk.CTkLabel(self.main_frame, text=f"Question {self.q_no + 1}/{len(quiz_data)}",
                                 font=ctk.CTkFont(size=20, weight="bold"))
        prog_text.pack(pady=20)

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            self.main_frame, width=500, height=20)
        self.progress.set((self.q_no + 1) / len(quiz_data))
        self.progress.pack(pady=(0, 30))

        # Question label
        q_label = ctk.CTkLabel(self.main_frame, text="📱 Situation:",
                               font=ctk.CTkFont(size=24, weight="bold"))
        q_label.pack()

        # Message frame with scroll
        msg_frame = ctk.CTkScrollableFrame(self.main_frame, height=250, width=700,
                                           corner_radius=15)
        msg_frame.pack(pady=20, padx=20, fill="x")

        q = quiz_data[self.q_no]
        msg_text = ctk.CTkTextbox(msg_frame, width=650, height=220,
                                  font=ctk.CTkFont(size=16), fg_color="#2b2b2b")
        msg_text.insert("0.0", q["message"])
        msg_text.configure(state="disabled")
        msg_text.pack(pady=10, padx=10)

        # Button frame
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        # SCAM button (red theme)
        scam_btn = ctk.CTkButton(btn_frame, text="🚨 SCAM!", width=180, height=60,
                                 font=ctk.CTkFont(size=20, weight="bold"),
                                 fg_color="#ff4757", hover_color="#ff3838",
                                 command=lambda: self.check_ans("Scam"))
        scam_btn.grid(row=0, column=0, padx=10)

        # LEGIT button (green theme)
        legit_btn = ctk.CTkButton(btn_frame, text="✅ LEGIT", width=180, height=60,
                                  font=ctk.CTkFont(size=20, weight="bold"),
                                  fg_color="#00d4aa", hover_color="#00b894",
                                  command=lambda: self.check_ans("Legit"))
        legit_btn.grid(row=0, column=1, padx=10)

        # Tips button
        tips_btn = ctk.CTkButton(self.main_frame, text="💡 Scam Spotting Tips",
                                 width=200, height=40, font=ctk.CTkFont(size=16),
                                 fg_color="#ffa502", hover_color="#ff8c00",
                                 command=self.show_tips)
        tips_btn.pack(pady=10)

    def check_ans(self, ans):
        q = quiz_data[self.q_no]
        correct = q["answer"]
        expl = q["explanation"]

        if ans == correct:
            self.score += 1
            messagebox.showinfo("✅ CORRECT!", f"Correct!\n\n{expl}")
        else:
            messagebox.showwarning("❌ WRONG!", f"Oops! Wrong answer\n\n{expl}")

        self.q_no += 1
        if self.q_no < len(quiz_data):
            self.disp_q()
        else:
            self.disp_score()

    def disp_score(self):
        self.screen_refresh()

        # Score display
        score_text = f"🎯 You scored {self.score}/{len(quiz_data)}"
        score_label = ctk.CTkLabel(self.main_frame, text=score_text,
                                   font=ctk.CTkFont(size=40, weight="bold"))
        score_label.pack(pady=60)

        percent = (self.score / len(quiz_data)) * 100

        if percent == 100:
            msg = "🏆 Excellent! You're a scam-spotting PRO! 🏆"
            msg_color = "#00d4aa"
        elif percent >= 70:
            msg = "👍 Good job! Stay vigilant out there! 👍"
            msg_color = "#ffa502"
        else:
            msg = "📚 Keep learning - scammers are tricky! 📚"
            msg_color = "#ff6b6b"

        msg_label = ctk.CTkLabel(self.main_frame, text=msg,
                                 font=ctk.CTkFont(size=22), text_color=msg_color)
        msg_label.pack(pady=30)

        # Action buttons
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=50)

        restart_btn = ctk.CTkButton(btn_frame, text="🔄 Restart Quiz", width=200, height=50,
                                    font=ctk.CTkFont(size=18), fg_color="#667eea",
                                    command=self.home_page)
        restart_btn.grid(row=0, column=0, padx=20)

        exit_btn = ctk.CTkButton(btn_frame, text="🚪 Exit", width=200, height=50,
                                 font=ctk.CTkFont(size=18), fg_color="#ff6b6b",
                                 command=self.root.destroy)
        exit_btn.grid(row=0, column=1, padx=20)

    def show_tips(self):
        tips = ("💡 SCAM SPOTTING TIPS:\n\n"
                "1. Be wary of urgent requests\n"
                "2. Check sender's email/phone carefully\n"
                "3. Don't click suspicious links\n"
                "4. Look for spelling mistakes\n"
                "5. Never give personal info over email")
        messagebox.showinfo("💡 Scam Spotting Tips", tips)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = SpotTheScam(root)
    root.mainloop()
