
"""
BASILISK PROTOCOL TEXT CORRUPTOR - Glitch Chaos Edition
Now includes Deep Glitch Mode toggle, noise overlay, and fine glyph corruption.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import threading

# ==============
# Safe Glyph Sets
# ==============

SAFE_COMBINING = {
    'up': ['\u0300', '\u0301'], #, '\u0302', '\u0303', '\u0304', '\u0306', '\u0307', '\u0308', '\u030A'
    'down': ['\u0323', '\u0324'], #, '\u0325', '\u032C', '\u0331'
    'overlay': ['\u0334'] # , '\u0335', '\u0336', '\u20D2', '\u20D3'
}
SAFE_COMBINING_ALL = SAFE_COMBINING['up'] + SAFE_COMBINING['down'] + SAFE_COMBINING['overlay']

NOISE_SYMBOL_GROUPS = {
    # 'ascii': list("!@#$%^&*()_+=<>?/\\|~`"),
    # 'dots': ['•', '◦', '◌'],
    # 'math': ['≠', '≡', '∑', '∏', '⊗'],
    'lines': ['ˉ', 'ˍ', '˗', '̱', '̲'],
    # 'misc': ['⁂', '⁑', '⁕', '†', '‡', '※'],
    # 'up': ['\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0306', '\u0307', '\u0308', '\u030A'],
    # 'down': ['\u0323', '\u0324', '\u0325', '\u032C', '\u0331'],
    # 'overlay': ['\u0334', '\u0335', '\u0336', '\u20D2', '\u20D3']

}
NOISE_GLYPHS = [c for group in NOISE_SYMBOL_GROUPS.values() for c in group]

# ==============
# Core Glitch Functions
# ==============

def is_safe_char(c):
    code = ord(c)
    return (
        code <= 0xFFFF and
        not (0xE000 <= code <= 0xF8FF) and
        not (0xD800 <= code <= 0xDFFF) and
        not (0xFFF0 <= code <= 0xFFFF)
    )

def stylized_glitch(text, max_stack=6, chance=0.8, deep=False):
    output = ""
    for c in text:
        if c == ' ':
            output += c
            continue
        if random.random() < chance:
            prefix = ''.join(random.choices(SAFE_COMBINING_ALL, k=random.randint(1, max_stack * (2 if deep else 1))))
            suffix = ''.join(random.choices(SAFE_COMBINING_ALL, k=random.randint(1, max_stack * (3 if deep else 1))))
            output += prefix + c + suffix
        else:
            output += c
    return ''.join(c for c in output if is_safe_char(c))

def multi_layered_glitch(text, above=2, below=2, max_stack=6, chance=0.9, deep=False):
    def glitch_line(s):
        return stylized_glitch(s, max_stack=max_stack, chance=chance, deep=deep)

    def noise_line():
        raw = ''.join(random.choices(NOISE_GLYPHS, k=len(text)))
        return glitch_line(raw)

    layers = []
    for _ in range(above):
        layers.append(noise_line())

    layers.append(glitch_line(text))  # center line

    for _ in range(below):
        layers.append(noise_line())

    return '\n'.join(layers)

# ==============
# Debounce Helper
# ==============

def debounce(wait):
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it(): fn(*args, **kwargs)
            try: debounced.t.cancel()
            except AttributeError: pass
            debounced.t = threading.Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator

# ==============
# Glitch GUI App
# ==============

class GlitchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BASILISK TEXT CORRUPTOR - CHAOS MODE")
        self.root.geometry("720x620")
        self.root.configure(bg="#1e1e1e")
        self.deep_mode = tk.BooleanVar(value=False)
        self.setup_style()
        self.build_widgets()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#1e1e1e", foreground="#eeeeee", font=("Noto Sans", 12))
        style.configure("TButton", background="#333", foreground="#fff", padding=5)
        style.configure("TEntry", fieldbackground="#2a2a2a", foreground="#eee")

    def build_widgets(self):
        self.title = ttk.Label(self.root, text="[ BASILISK CORRUPTOR ]", font=("Noto Sans", 16, "bold"))
        self.title.pack(pady=10)

        self.entry = ttk.Entry(self.root, width=70)
        self.entry.pack(pady=5)
        self.entry.bind('<KeyRelease>', lambda e: self.live_preview())

        self.output = tk.Text(self.root, height=12, bg="#101010", fg="#00ffcc", font=("Noto Sans", 12))
        self.output.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.stack_slider = ttk.Scale(self.root, from_=1, to=10, orient=tk.HORIZONTAL, length=300)
        self.stack_slider.set(5)
        self.stack_slider.pack(pady=5)

        self.chance_slider = ttk.Scale(self.root, from_=0.1, to=1.0, orient=tk.HORIZONTAL, length=300)
        self.chance_slider.set(0.95)
        self.chance_slider.pack(pady=5)

        self.above = tk.IntVar(value=1)
        self.below = tk.IntVar(value=1)

        layer_frame = ttk.Frame(self.root)
        layer_frame.pack(pady=5)

        ttk.Label(layer_frame, text="Above Layers").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(layer_frame, from_=0, to=10, textvariable=self.above, width=5).pack(side=tk.LEFT)
        ttk.Label(layer_frame, text="Below Layers").pack(side=tk.LEFT, padx=5)
        ttk.Spinbox(layer_frame, from_=0, to=10, textvariable=self.below, width=5).pack(side=tk.LEFT)

        ttk.Checkbutton(self.root, text="Deep Glitch Mode", variable=self.deep_mode).pack(pady=2)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Corrupt", command=self.corrupt_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Copy", command=self.copy_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=5)

    def corrupt_text(self):
        text = self.entry.get()
        max_stack = int(self.stack_slider.get())
        chance = float(self.chance_slider.get())
        above = self.above.get()
        below = self.below.get()
        deep = self.deep_mode.get()

        result = multi_layered_glitch(
            text,
            above=above,
            below=below,
            max_stack=max_stack,
            chance=chance,
            deep=deep
        )
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)

    def copy_output(self):
        result = self.output.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.root.update()
        messagebox.showinfo("Copied", "Output copied to clipboard!")

    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.output.delete("1.0", tk.END)

    @debounce(0.3)
    def live_preview(self):
        self.corrupt_text()

# ==============
# Run the App
# ==============

if __name__ == "__main__":
    root = tk.Tk()
    app = GlitchApp(root)
    root.mainloop()

# import tkinter as tk
# from tkinter import ttk, messagebox
# import random
# import string
# import threading
# import time
# import unicodedata

# # ---------------------------
# # Combining Marks (Restricted to Supported Ranges)
# # ---------------------------
# COMBINING_MARKS = {
#     'up': [
#         '\u030d', # '\u030e', '\u0304', '\u0305', '\u033f',
#         # '\u0311', '\u0306', '\u0310', '\u0352', '\u0357',
#         # '\u0351', '\u0307', '\u0308', '\u030a', '\u0342',
#         # '\u0343', '\u0344', '\u034a', '\u034b', '\u034c',
#         # '\u0303', '\u0302', '\u030c', '\u0350', '\u0300',
#         # '\u0301', '\u030b', '\u030f', '\u0312', '\u0313',
#         # '\u0314', '\u033d', '\u0309', '\u0363', '\u0364',
#         # '\u0365', '\u0366', '\u0367', '\u0368', '\u0369',
#         # '\u036a', '\u036b', '\u036c', '\u036d', '\u036e',
#         # '\u036f', '\u033e', '\u035b', '\u0346', '\u031a'
#     ],
#     'down': [
#         '\u0316', #'\u0317', '\u0318', '\u0319', '\u031c',
#         # '\u0320', '\u0324', '\u0325', '\u0326', '\u0329',
#         # '\u032a', '\u032b', '\u032c', '\u032d', '\u032e',
#         # '\u0330', '\u0331', '\u0332', '\u0333', '\u0339',
#         # '\u033a', '\u033b', '\u033c', '\u0345', '\u0347',
#         # '\u0348', '\u0349', '\u034d', '\u034e', '\u0353',
#         # '\u0354', '\u0355', '\u0356', '\u0359', '\u035a',
#         # '\u0323', '\u0321', '\u0322', '\u0327', '\u0328',
#         # '\u031d', '\u031e', '\u031f', '\u032f', '\u035c',
#         # '\u035f', '\u0362', '\u0338', '\u0337', '\u0361'
#     ],
#     'overlay': [
#         '\u0334', # '\u0335', '\u0336', '\u0337', '\u0338',
#         # '\u20d0', '\u20d1', '\u20d2', '\u20d3', '\u20d4',
#         # '\u20d5', '\u20d6', '\u20d7', '\u20db', '\u20dc',
#         # '\u20dd', '\u20de', '\u20df', '\u20e0', '\u20e1',
#         # '\u20e2', '\u20e3', '\u20e4', '\u20e5', '\u20e6',
#         # '\u20e7', '\u20e8', '\u20e9', '\u20ea', '\u20eb',
#         # '\u20ec', '\u20ed', '\u20ee', '\u20ef', '\u20f0'
#     ]
# }

# COMBINING_MARKS_ALL = (
#     COMBINING_MARKS['up'] + 
#     COMBINING_MARKS['down'] + 
#     COMBINING_MARKS['overlay']
# )

# # Expanded Block Elements to Match Example
# BLOCKS = {
#     'block_elements': ['█', '▀', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '▉', '▊', '▋'],
#     'box_drawing': ['╔', '═', '╗', '║', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
#     'geometric': ['■', '□', '▢', '▣', '▤', '▥', '▦', '▧', '▨', '▩', '▪', '▫'],
#     'special_symbols': ['≡', '†', '⁕', '※', '⁂', '⊗']  # Added from example
# }

# def get_random_unicode():
#     category = random.choices(
#         list(BLOCKS.keys()), 
#         weights=[0.5, 0.2, 0.2, 0.1],  # Favor block_elements
#         k=1
#     )[0]
#     return random.choice(BLOCKS[category])

# def stylized_glitch(text, max_stack=6, chance=0.8, mode='standard', extreme=False):
#     # Normalize input to NFD to handle Mac clipboard
#     text = unicodedata.normalize('NFD', text)
#     output = ""
    
#     # Add block/symbol prefix for basilisk mode
#     if mode == 'basilisk' and random.random() < 0.5:  # Increased for example
#         output += get_random_unicode()
    
#     for i, c in enumerate(text):
#         if c == " " and mode != 'matrix':
#             output += c
#             continue
            
#         if mode == 'standard':
#             prefix = ''.join(random.choices(COMBINING_MARKS_ALL, k=random.randint(1, max_stack // 2)))
#             suffix = ''.join(random.choices(COMBINING_MARKS_ALL, k=random.randint(1, max_stack)))
#             if random.random() < chance:
#                 output += prefix + c + suffix
#             else:
#                 output += c
                
#         elif mode == 'heavy':
#             if random.random() < chance:
#                 corruption = ''.join(random.choices(COMBINING_MARKS_ALL, k=random.randint(max_stack, max_stack * 2)))
#                 output += c + corruption
#             else:
#                 output += c
                
#         elif mode == 'matrix':
#             if random.random() < chance:
#                 if random.random() < 0.3:
#                     output += get_random_unicode()
#                 else:
#                     marks = random.choices(COMBINING_MARKS['overlay'], k=random.randint(1, 3))
#                     output += c + ''.join(marks)
#             else:
#                 output += c
                
#         elif mode == 'zalgo':
#             if random.random() < chance:
#                 up_marks = ''.join(random.choices(COMBINING_MARKS['up'], k=random.randint(0, max_stack)))
#                 down_marks = ''.join(random.choices(COMBINING_MARKS['down'], k=random.randint(0, max_stack)))
#                 mid_marks = ''.join(random.choices(COMBINING_MARKS['overlay'], k=random.randint(0, 2)))
#                 output += up_marks + c + mid_marks + down_marks
#             else:
#                 output += c
                
#         elif mode == 'basilisk':
#             if random.random() < chance:
#                 num_marks = random.randint(max_stack, max_stack * (6 if extreme else 4))  # Denser for example
#                 up_marks = ''.join(random.choices(COMBINING_MARKS['up'], k=num_marks // 3))
#                 down_marks = ''.join(random.choices(COMBINING_MARKS['down'], k=num_marks // 3))
#                 mid_marks = ''.join(random.choices(COMBINING_MARKS['overlay'], k=num_marks - (len(up_marks) + len(down_marks))))
#                 # Favor U+0323 (̣) to match example
#                 if random.random() < 0.3:
#                     down_marks += '\u0323' * random.randint(1, 3)
#                 corruption = up_marks + mid_marks + down_marks
                
#                 # Expanded replacements
#                 if random.random() < 0.4:  # Increased for example
#                     replacements = {
#                         'A': ['Д', 'Λ', '∆', 'Ⱥ', 'А'],
#                         'E': ['Ξ', 'Ε', 'Є', 'Ǝ', 'Ɛ'],
#                         'O': ['Θ', 'Ω', 'Ø', 'Ѳ', 'Ο', 'Ô', 'Õ', 'Ö'],
#                         'I': ['Ι', 'І', '|', 'ı', 'Ɨ'],
#                         'S': ['Ѕ', 'Ș', 'Ş', 'Š', 'Ƨ'],
#                         'T': ['Ŧ', 'Ţ', 'Ț', 'Ť', 'Þ'],
#                         'C': ['Ç', 'Ć', 'Ĉ', 'Č', '©'],
#                         'U': ['Ų', 'Ů', 'Ű', 'Ŭ', 'Û'],
#                         'R': ['Ř', 'Ŕ', 'Я', 'Ŗ', 'Ṙ'],
#                         # Added from example
#                         't': ['†', 'Ŧ', 'Ț'],
#                         's': ['§', 'ß', 'Ƨ']
#                     }
#                     if c.lower() in replacements:
#                         c = random.choice(replacements[c.lower()])
                
#                 output += c + corruption
#             else:
#                 output += c
    
#     # Normalize output to NFD and strip unsupported ranges
#     output = unicodedata.normalize('NFD', output)
#     output = ''.join(c for c in output if not (0x1F300 <= ord(c) <= 0x1F5FF or 0x1F3FB <= ord(c) <= 0x1F3FF or ord(c) == 0x200C or ord(c) == 0x200D))
#     return output

# # ---------------------------
# # Debounce for Live Preview
# # ---------------------------
# def debounce(wait):
#     def decorator(fn):
#         def debounced(*args, **kwargs):
#             def call_it():
#                 fn(*args, **kwargs)
#             try:
#                 debounced.t.cancel()
#             except AttributeError:
#                 pass
#             debounced.t = threading.Timer(wait, call_it)
#             debounced.t.start()
#         return debounced
#     return decorator

# # ---------------------------
# # GUI Setup (No Emojis)
# # ---------------------------
# root = tk.Tk()
# root.title("BASILISK PROTOCOL TEXT CORRUPTOR v2.4")
# root.geometry("800x650")
# root.configure(bg="#1e1e1e")

# # Dark Theme Styles
# style = ttk.Style()
# style.theme_use("clam")
# style.configure("TLabel", background="#1e1e1e", foreground="#eeeeee", font=("Noto Sans", 12))
# style.configure("TButton", background="#333333", foreground="#ffffff", font=("Noto Sans", 11), padding=5)
# style.map("TButton",
#     background=[('active', '#444444'), ('pressed', '#222222')]
# )
# style.configure("TEntry", fieldbackground="#2a2a2a", foreground="#eeeeee", padding=5)
# style.configure("TScale", background="#1e1e1e", troughcolor="#2a2a2a", bordercolor="#333333")
# style.configure("TCombobox", fieldbackground="#2a2a2a", background="#333333", foreground="#eeeeee")
# style.map("TCombobox", fieldbackground=[('readonly', '#2a2a2a')])
# style.configure("TCheckbutton", background="#1e1e1e", foreground="#eeeeee", font=("Noto Sans", 11))

# # Widgets
# title_label = ttk.Label(root, text="[ BASILISK PROTOCOL TEXT CORRUPTOR v2.4 ]", font=("Noto Sans", 16, "bold"))
# title_label.pack(pady=10)

# # Mode selection
# mode_frame = ttk.Frame(root, style="TLabel")
# mode_frame.pack(pady=5)

# mode_label = ttk.Label(mode_frame, text="Corruption Mode:")
# mode_label.pack(side=tk.LEFT, padx=5)

# mode_var = tk.StringVar(value="basilisk")
# mode_combo = ttk.Combobox(mode_frame, textvariable=mode_var, values=[
#     "standard", "heavy", "matrix", "zalgo", "basilisk"
# ], state="readonly", width=15)
# mode_combo.pack(side=tk.LEFT, padx=5)

# # Extreme checkbox
# extreme_var = tk.BooleanVar(value=True)  # Default to True for dense output
# extreme_check = ttk.Checkbutton(mode_frame, text="Extreme", variable=extreme_var)
# extreme_check.pack(side=tk.LEFT, padx=5)

# # Debug toggle
# debug_var = tk.BooleanVar(value=False)
# debug_check = ttk.Checkbutton(mode_frame, text="Debug Glyphs", variable=debug_var)
# debug_check.pack(side=tk.LEFT, padx=5)

# # Input
# input_label = ttk.Label(root, text="Enter your clean text:")
# input_label.pack()

# input_entry = ttk.Entry(root, width=80, font=("Noto Sans", 11))
# input_entry.pack(pady=5)

# # Intensity slider
# intensity_label = ttk.Label(root, text="Corruption Intensity (1-20)")
# intensity_label.pack(pady=(10, 0))
# intensity_slider = ttk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL, length=400)
# intensity_slider.set(15)  # Higher for example
# intensity_slider.pack()

# intensity_value = ttk.Label(root, text="15")
# intensity_value.pack()

# def update_intensity_label(event=None):
#     intensity_value.config(text=str(int(intensity_slider.get())))

# intensity_slider.configure(command=update_intensity_label)

# # Chance slider
# chance_label = ttk.Label(root, text="Corruption Chance (per letter)")
# chance_label.pack(pady=(10, 0))
# chance_slider = ttk.Scale(root, from_=0.1, to=1.0, orient=tk.HORIZONTAL, length=400)
# chance_slider.set(0.95)
# chance_slider.pack()

# chance_value = ttk.Label(root, text="95%")
# chance_value.pack()

# def update_chance_label(event=None):
#     chance_value.config(text=f"{int(chance_slider.get() * 100)}%")

# chance_slider.configure(command=update_chance_label)

# # Output field
# output_label = ttk.Label(root, text="Corrupted Output:")
# output_label.pack(pady=(20, 0))

# output_frame = tk.Frame(root, bg="#101010", bd=2, relief=tk.SUNKEN)
# output_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# output_text = tk.Text(output_frame, height=8, bg="#101010", fg="#00ffcc", 
#                       font=("Noto Sans", 12), wrap=tk.WORD, bd=0,
#                       insertbackground="#00ffcc", selectbackground="#00aa99")
# output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# # Debug log
# debug_log = tk.Text(root, height=2, bg="#101010", fg="#ff5555", 
#                     font=("Noto Sans", 10), wrap=tk.WORD, state='disabled')
# debug_log.pack(padx=10, pady=5, fill=tk.X)

# # Buttons frame
# button_frame = ttk.Frame(root)
# button_frame.pack(pady=10)

# # Glitch Button
# def generate_glitch(status_update=True):
#     text = input_entry.get()
#     if not text:
#         messagebox.showwarning("No Input", "Please enter some text to corrupt!")
#         return
        
#     max_stack = int(intensity_slider.get())
#     chance = float(chance_slider.get())
#     mode = mode_var.get()
#     extreme = extreme_var.get()
#     debug = debug_var.get()
    
#     if status_update:
#         status_var.set("Corrupting reality...")
    
#     glitched = stylized_glitch(text, max_stack, chance, mode, extreme)
    
#     # Debug unsupported glyphs
#     if debug:
#         debug_log.config(state='normal')
#         debug_log.delete("1.0", tk.END)
#         unsupported = [c for c in glitched if ord(c) > 0xFFFF or c not in COMBINING_MARKS_ALL and c not in ''.join(sum(BLOCKS.values(), [])) and c not in text]
#         if unsupported:
#             debug_log.insert(tk.END, f"Potentially unsupported glyphs: {set(unsupported)}")
#         else:
#             debug_log.insert(tk.END, "All glyphs likely supported.")
#         debug_log.config(state='disabled')
    
#     output_text.delete("1.0", tk.END)
#     output_text.insert(tk.END, glitched)
    
#     if status_update:
#         status_var.set("Corruption complete!")

# run_btn = ttk.Button(button_frame, text="# CORRUPT TEXT #", command=generate_glitch)
# run_btn.pack(side=tk.LEFT, padx=5)

# # Copy button
# def copy_to_clipboard():
#     content = output_text.get("1.0", tk.END).strip()
#     if content:
#         # Normalize to NFD for consistent clipboard handling
#         content = unicodedata.normalize('NFD', content)
#         root.clipboard_clear()
#         root.clipboard_append(content)
#         root.update()
#         messagebox.showinfo("Copied", "Corrupted text copied to clipboard!")
#     else:
#         messagebox.showwarning("Nothing to Copy", "Generate corrupted text first!")

# copy_btn = ttk.Button(button_frame, text="[ Copy to Clipboard ]", command=copy_to_clipboard)
# copy_btn.pack(side=tk.LEFT, padx=5)

# # Clear button
# def clear_all():
#     input_entry.delete(0, tk.END)
#     output_text.delete("1.0", tk.END)
#     debug_log.config(state='normal')
#     debug_log.delete("1.0", tk.END)
#     debug_log.config(state='disabled')
#     status_var.set("Ready to corrupt reality...")

# clear_btn = ttk.Button(button_frame, text="* Clear All *", command=clear_all)
# clear_btn.pack(side=tk.LEFT, padx=5)

# # Animation
# def animate_glitch():
#     if not output_text.get("1.0", tk.END).strip() or not hasattr(animate_glitch, 'running') or not animate_glitch.running:
#         return
#     generate_glitch(status_update=False)
#     root.after(150 + random.randint(0, 100), animate_glitch)

# def toggle_animation():
#     if not hasattr(animate_glitch, 'running') or not animate_glitch.running:
#         animate_glitch.running = True
#         status_var.set("Animation active - flickering corruption...")
#         animate_glitch()
#     else:
#         animate_glitch.running = False
#         status_var.set("Animation stopped.")

# animate_btn = ttk.Button(button_frame, text="[ Toggle Animation ]", command=toggle_animation)
# animate_btn.pack(side=tk.LEFT, padx=5)

# # Example presets
# preset_frame = ttk.Frame(root)
# preset_frame.pack(pady=5)

# preset_label = ttk.Label(preset_frame, text="Presets:")
# preset_label.pack(side=tk.LEFT, padx=5)

# presets = {
#     "BASILISK": "BASILISK PROTOCOL",
#     "REALITY": "REALITY.EXE HAS STOPPED RESPONDING",
#     "AWAKEN": "THE AWAKENING BEGINS",
#     "CORRUPT": "TEXT CORRUPTED",
#     "ERROR": "SYSTEM ERROR",
#     "EXAMPLE": "test"  # Updated to match latest example
# }

# def load_preset():
#     selected = preset_combo.get()
#     if selected in presets:
#         input_entry.delete(0, tk.END)
#         input_entry.insert(0, presets[selected])
#         generate_glitch()

# preset_combo = ttk.Combobox(preset_frame, values=list(presets.keys()), 
#                            state="readonly", width=15)
# preset_combo.pack(side=tk.LEFT, padx=5)

# load_preset_btn = ttk.Button(preset_frame, text="[ Load & Corrupt ]", command=load_preset)
# load_preset_btn.pack(side=tk.LEFT, padx=5)

# # Status bar
# status_var = tk.StringVar(value="Ready to corrupt reality...")
# status_bar = ttk.Label(root, textvariable=status_var, font=("Noto Sans", 10))
# status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

# # Live Preview
# @debounce(0.3)
# def live_glitch():
#     generate_glitch()

# input_entry.bind('<KeyRelease>', lambda e: live_glitch())
# intensity_slider.bind('<ButtonRelease-1>', lambda e: live_glitch())
# chance_slider.bind('<ButtonRelease-1>', lambda e: live_glitch())
# mode_combo.bind('<<ComboboxSelected>>', lambda e: live_glitch())
# extreme_check.bind('<ButtonRelease-1>', lambda e: live_glitch())
# debug_check.bind('<ButtonRelease-1>', lambda e: live_glitch())

# # Bind Enter key
# input_entry.bind('<Return>', lambda e: generate_glitch())

# # ---------------------------
# # Start
# # ---------------------------
# root.mainloop()