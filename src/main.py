import customtkinter as ctk
from tkinter import messagebox, filedialog
import qrcode
import os
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import webbrowser
from PIL import Image, ImageTk
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Generator & Scanner")
        self.resizable(True, True)
        self.base_width = 800
        self.base_height = 600
        self.geometry(f"{self.base_width}x{self.base_height}")
        self.minsize(500, 400)

        
        self.base_title_font_size = 32
        self.base_subtitle_font_size = 16
        self.base_button_font_size = 20
        self.base_button_height = 70
        self.base_pady_title = 50
        self.base_pady_subtitle = 40
        self.base_pady_button = 20
        self.base_pady_exit = 40
        self.base_padx_button = 60

        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.main_frame, text="🔍 QR Code Toolkit", anchor="center")
        self.sub_label = ctk.CTkLabel(self.main_frame, text="Choose to build or detect QR code", anchor="center")
        self.btn_generate = ctk.CTkButton(self.main_frame, text="✨ Make QR Code", command=self.open_generator)
        self.btn_scan = ctk.CTkButton(self.main_frame, text="📷 Detect QR Code", command=self.open_scanner)
        self.btn_exit = ctk.CTkButton(self.main_frame, text="🚪 Exit", command=self.quit,
                                      fg_color="gray30", hover_color="gray20")

        self.bind("<Configure>", self.on_resize)
        self.after(10, self.apply_scaling)

    def on_resize(self, event):
        if event.widget == self:
            self.apply_scaling()

    def apply_scaling(self):
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        if current_width < 50 or current_height < 50:
            current_width, current_height = self.base_width, self.base_height

        scale_w = current_width / self.base_width
        scale_h = current_height / self.base_height
        scale = min(scale_w, scale_h)
        scale = max(0.5, min(scale, 1.8))

        title_font_size = int(self.base_title_font_size * scale)
        subtitle_font_size = int(self.base_subtitle_font_size * scale)
        button_font_size = int(self.base_button_font_size * scale)
        button_height = int(self.base_button_height * scale)

        pady_title = int(self.base_pady_title * scale)
        pady_subtitle = int(self.base_pady_subtitle * scale)
        pady_button = int(self.base_pady_button * scale)
        pady_exit = int(self.base_pady_exit * scale)
        padx_button = int(self.base_padx_button * scale)

        self.title_label.configure(font=ctk.CTkFont(size=title_font_size, weight="bold"))
        self.sub_label.configure(font=ctk.CTkFont(size=subtitle_font_size))
        self.btn_generate.configure(font=ctk.CTkFont(size=button_font_size, weight="bold"), height=button_height)
        self.btn_scan.configure(font=ctk.CTkFont(size=button_font_size, weight="bold"), height=button_height)
        self.btn_exit.configure(font=ctk.CTkFont(size=button_font_size-4), height=int(button_height*0.7))

        for widget in [self.title_label, self.sub_label, self.btn_generate, self.btn_scan, self.btn_exit]:
            widget.pack_forget()

        self.title_label.pack(pady=(pady_title, 10))
        self.sub_label.pack(pady=(0, pady_subtitle))
        self.btn_generate.pack(pady=pady_button, padx=padx_button, fill="x")
        self.btn_scan.pack(pady=pady_button, padx=padx_button, fill="x")
        self.btn_exit.pack(pady=(pady_exit, pady_button), padx=padx_button, fill="x")

    def open_generator(self):
        generator_window = ctk.CTkToplevel(self)
        generator_window.title("Make QR Code")
        generator_window.geometry("500x400")
        generator_window.resizable(True, True)
        generator_window.minsize(400, 300)
        generator_window.transient(self)
        generator_window.grab_set()

        frame = ctk.CTkFrame(generator_window, corner_radius=20)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        lbl_title = ctk.CTkLabel(frame, text="🔧 Make New QR Code ", font=ctk.CTkFont(size=22, weight="bold"))
        lbl_title.pack(pady=(30, 20))

        lbl_entry = ctk.CTkLabel(frame, text="Please enter the website address or text you are looking for.", font=ctk.CTkFont(size=14))
        lbl_entry.pack(pady=(10, 5))

        entry_data = ctk.CTkEntry(frame, placeholder_text="for example: https://google.com", width=300, height=40)
        entry_data.pack(pady=10)

        def generate_and_save():
            data = entry_data.get().strip()
            if not data:
                messagebox.showwarning("Error", "Please enter text or address.")
                return
            try:
                qr = qrcode.QRCode(box_size=10, border=4)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                save_path = os.path.join(os.getcwd(), "generated_qrcode.png")
                img.save(save_path)
                messagebox.showinfo("Successful", f"QR Code Successfully created and saved.\n Path:{save_path}")
                generator_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"  There is a problem:\n{str(e)}")

        btn_generate = ctk.CTkButton(frame, text="✨ generate and save", command=generate_and_save, height=50, font=ctk.CTkFont(size=16))
        btn_generate.pack(pady=30, padx=40, fill="x")

        btn_close = ctk.CTkButton(frame, text="Exit", command=generator_window.destroy, fg_color="gray30", hover_color="gray20", height=35)
        btn_close.pack(pady=10, padx=40, fill="x")

    def open_scanner(self):
        # پنجره انتخاب روش تشخیص
        scanner_menu = ctk.CTkToplevel(self)
        scanner_menu.title("QR Code Detect")
        scanner_menu.geometry("450x300")
        scanner_menu.resizable(False, False)
        scanner_menu.transient(self)
        scanner_menu.grab_set()

        frame = ctk.CTkFrame(scanner_menu, corner_radius=20)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        label = ctk.CTkLabel(frame, text="Choose how to detect:", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=(30, 20))

        btn_camera = ctk.CTkButton(frame, text="📸 Camera", command=lambda: self.start_camera_scanner(scanner_menu), height=50, font=ctk.CTkFont(size=16))
        btn_camera.pack(pady=15, padx=40, fill="x")

        btn_gallery = ctk.CTkButton(frame, text="🖼️ Gallery", command=lambda: self.scan_from_gallery(scanner_menu), height=50, font=ctk.CTkFont(size=16))
        btn_gallery.pack(pady=15, padx=40, fill="x")

        btn_close = ctk.CTkButton(frame, text="Close", command=scanner_menu.destroy, fg_color="gray30", hover_color="gray20", height=35)
        btn_close.pack(pady=(30, 20), padx=40, fill="x")

    def start_camera_scanner(self, parent_window):
        parent_window.destroy()  # بستن پنجره منوی انتخاب
        # پنجره دوربین
        camera_window = ctk.CTkToplevel(self)
        camera_window.title("Scan QR with camera")
        camera_window.geometry("800x600")
        camera_window.minsize(640, 480)

        # برچسب برای نمایش تصویر
        video_label = ctk.CTkLabel(camera_window, text="")
        video_label.pack(expand=True, fill="both", padx=10, pady=10)

        # متغیر برای کنترل حلقه دوربین
        camera_window.running = True
        camera_window.cap = None

        def open_camera():
            camera_window.cap = cv2.VideoCapture(0)
            if not camera_window.cap.isOpened():
                messagebox.showerror("Error", "Doesn't find camera.")
                camera_window.destroy()
                return

            def update_frame():
                if not camera_window.running:
                    return
                ret, frame = camera_window.cap.read()
                if ret:
                    # تشخیص QR کدها
                    decoded_objects = decode(frame)
                    for obj in decoded_objects:
                        data = obj.data.decode('utf-8')
                        # رسم مستطیل دور کد
                        points = obj.polygon
                        if points:
                            pts = np.array([(p.x, p.y) for p in points], np.int32)
                            pts = pts.reshape((-1, 1, 2))
                            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                        # اگر داده پیدا شد، از کاربر بپرسیم
                        if data:
                            camera_window.running = False  # توقف تشخیص بعد از اولین پیدا کردن
                            camera_window.cap.release()
                            # نمایش سوال در یک پنجره جدید (از thread اصلی tkinter استفاده کن)
                            camera_window.after(0, lambda d=data: self.ask_open_link(d, camera_window))
                            return
                    # تبدیل فریم به فرمت مناسب برای CTkLabel
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame_rgb)
                    imgtk = ImageTk.PhotoImage(image=img)
                    video_label.imgtk = imgtk
                    video_label.configure(image=imgtk)
                # ادامه حلقه
                if camera_window.running:
                    camera_window.after(10, update_frame)

            update_frame()

        # شروع دوربین در یک thread جداگانه برای جلوگیری از قفل شدن UI
        threading.Thread(target=open_camera, daemon=True).start()

        # دکمه بستن در پایین پنجره
        btn_close_cam = ctk.CTkButton(camera_window, text="Close the camera", command=lambda: self.close_camera(camera_window), height=35)
        btn_close_cam.pack(side="bottom", pady=10)

        # وقتی پنجره بسته شد، دوربین را آزاد کن
        camera_window.protocol("WM_DELETE_WINDOW", lambda: self.close_camera(camera_window))

    def close_camera(self, window):
        window.running = False
        if hasattr(window, 'cap') and window.cap is not None:
            window.cap.release()
        window.destroy()

    def ask_open_link(self, url, parent_window):
        # بستن پنجره دوربین یا گالری اگر هنوز باز است
        if parent_window and parent_window.winfo_exists():
            parent_window.destroy()
        # سوال از کاربر
        answer = messagebox.askyesno("Link found", f"The following address was detected:\n{url}\n\nDo you want to open the browser?")
        if answer:
            webbrowser.open(url)

    def scan_from_gallery(self, parent_window):
        parent_window.destroy()
        file_path = filedialog.askopenfilename(
            title="Choose QR Code Picture",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not file_path:
            return
        try:
            # خواندن تصویر با OpenCV
            img = cv2.imread(file_path)
            if img is None:
                messagebox.showerror("Error", "The image file is not valid.")
                return
            decoded_objects = decode(img)
            if not decoded_objects:
                messagebox.showinfo("Result", "There is no QR code in the picture.")
                return
            # اولین کد را می‌گیریم
            data = decoded_objects[0].data.decode('utf-8')
            self.ask_open_link(data, None)
        except Exception as e:
            messagebox.showerror("Error", f"There is a problem to read picture:\n{str(e)}")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
