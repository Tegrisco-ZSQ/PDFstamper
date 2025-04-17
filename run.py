import os
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class PDFStamperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Offline PDF Text‑Note Adder")
        self.geometry("400x260")
        self.pdf_paths = []
        self.output_dir = ""

        # Only keep the numeric inputs in the main form:
        tk.Label(self, text="Font size (pt):").pack(anchor="w", padx=10, pady=(10,0))
        self.font_size = tk.Spinbox(self, from_=6, to=72, width=5)
        self.font_size.delete(0, "end"); self.font_size.insert(0, "12")
        self.font_size.pack(padx=10, anchor="w")

        tk.Label(self, text="Margin from right (pt):").pack(anchor="w", padx=10, pady=(10,0))
        self.margin_x = tk.Spinbox(self, from_=0, to=500, width=5)
        self.margin_x.delete(0, "end"); self.margin_x.insert(0, "50")
        self.margin_x.pack(padx=10, anchor="w")

        tk.Label(self, text="Margin from top (pt):").pack(anchor="w", padx=10, pady=(10,0))
        self.margin_y = tk.Spinbox(self, from_=0, to=500, width=5)
        self.margin_y.delete(0, "end"); self.margin_y.insert(0, "50")
        self.margin_y.pack(padx=10, anchor="w")

        tk.Button(self, text="Select PDF files…", command=self.select_pdfs).pack(pady=8)
        tk.Button(self, text="Select output folder…", command=self.select_output).pack()
        tk.Button(self, text="Run stamping", command=self.run).pack(pady=12)

    def select_pdfs(self):
        paths = filedialog.askopenfilenames(
            title="Choose PDF files",
            filetypes=[("PDF files","*.pdf")])
        if paths:
            self.pdf_paths = list(paths)
            messagebox.showinfo("Selected", f"{len(paths)} files selected")

    def select_output(self):
        d = filedialog.askdirectory(title="Select output folder")
        if d:
            self.output_dir = d
            messagebox.showinfo("Output", f"Output folder set to:\n{d}")

    def run(self):
        if not self.pdf_paths:
            messagebox.showerror("Error", "No PDFs selected")
            return
        if not self.output_dir:
            messagebox.showerror("Error", "No output folder chosen")
            return

        # **Prompt for the text note each time**
        note = simpledialog.askstring("Text Note", "Enter the text to stamp:")
        if not note:
            messagebox.showwarning("Cancelled", "No text entered; aborting.")
            return

        fs = float(self.font_size.get())
        mx = float(self.margin_x.get())
        my = float(self.margin_y.get())

        for path in self.pdf_paths:
            doc  = fitz.open(path)
            page = doc[0]
            r    = page.rect

            # measure text width
            tw = fitz.get_text_length(note, fontname="helv", fontsize=fs)
            x  = r.width - mx - tw
            y  = my

            page.insert_text((x, y),
                             note,
                             fontname="helv",
                             fontsize=fs,
                             fill=(0,0,0))

            out_path = os.path.join(self.output_dir, os.path.basename(path))
            doc.save(out_path)
            doc.close()

        messagebox.showinfo("Done", f"Stamped {len(self.pdf_paths)} PDFs.")

if __name__ == "__main__":
    PDFStamperApp().mainloop()
