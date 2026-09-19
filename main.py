import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class SqlDiffUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SqlDiff UI")
        self.root.geometry("700x550")
        self.root.minsize(600, 450)

        # Variables para almacenar rutas
        self.db1_path = tk.StringVar()
        self.db2_path = tk.StringVar()

        default_sqldiff = shutil.which("sqldiff")
        # Si no lo encuentra en el PATH, lo deja vacio
        if not default_sqldiff:
            default_sqldiff = ""
        self.sqldiff_path = tk.StringVar(value=default_sqldiff)

        # Variables para los flags de sqldiff
        self.flag_primarykey = tk.BooleanVar(value=True)
        self.flag_schema = tk.BooleanVar(value=False)
        self.flag_summary = tk.BooleanVar(value=False)
        self.flag_transaction = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        # --- SECCIÓN DE ARCHIVOS ---
        file_frame = ttk.LabelFrame(
            self.root, text=" File config ", padding=10
        )
        file_frame.pack(fill="x", padx=10, pady=5)

        # Ruta de sqldiff.exe
        ttk.Label(file_frame, text="sqldiff path:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        ttk.Entry(file_frame, textvariable=self.sqldiff_path, width=50).grid(
            row=0, column=1, padx=5, pady=2
        )
        ttk.Button(file_frame, text="Search...", command=self.browse_sqldiff).grid(
            row=0, column=2, pady=2
        )

        # Base de datos 1 (Origen)
        ttk.Label(file_frame, text="Original database:").grid(
            row=1, column=0, sticky="w", pady=2
        )
        ttk.Entry(file_frame, textvariable=self.db1_path, width=50).grid(
            row=1, column=1, padx=5, pady=2
        )
        ttk.Button(file_frame, text="Select...", command=self.browse_db1).grid(
            row=1, column=2, pady=2
        )

        # Base de datos 2 (Destino/Modificada)
        ttk.Label(file_frame, text="Modified database:").grid(
            row=2, column=0, sticky="w", pady=2
        )
        ttk.Entry(file_frame, textvariable=self.db2_path, width=50).grid(
            row=2, column=1, padx=5, pady=2
        )
        ttk.Button(file_frame, text="Select...", command=self.browse_db2).grid(
            row=2, column=2, pady=2
        )

        # --- SECCIÓN DE FLAGS ---
        flags_frame = ttk.LabelFrame(self.root, text=" Options ", padding=10)
        flags_frame.pack(fill="x", padx=10, pady=5)

        ttk.Checkbutton(
            flags_frame,
            text="Use primary key instead of rowid (--primarykey)",
            variable=self.flag_primarykey,
        ).pack(anchor="w", pady=2)
        ttk.Checkbutton(
            flags_frame,
            text="Only compare schemas, no data (--schema)",
            variable=self.flag_schema,
        ).pack(anchor="w", pady=2)
        ttk.Checkbutton(
            flags_frame,
            text="Show number of changed rows (--summary)",
            variable=self.flag_summary,
        ).pack(anchor="w", pady=2)
        ttk.Checkbutton(
            flags_frame,
            text="Wrap the SQL output with BEGIN...COMMIT (--transaction)",
            variable=self.flag_transaction,
        ).pack(anchor="w", pady=2)

        # --- BOTÓN DE EJECUCIÓN ---
        self.btn_run = ttk.Button(self.root, text="Compare databases", command=self.run_diff)
        self.btn_run.pack(pady=10)

        # --- SECCIÓN DE RESULTADO ---
        result_frame = ttk.LabelFrame(self.root, text=" Result ", padding=5)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Añadimos un Text widget con Scrollbar para ver el output SQL
        self.txt_result = tk.Text(result_frame, wrap="none", font=("Consolas", 10))
        ysb = ttk.Scrollbar(
            result_frame, orient="vertical", command=self.txt_result.yview
        )
        xsb = ttk.Scrollbar(
            result_frame, orient="horizontal", command=self.txt_result.xview
        )
        self.txt_result.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        # Ubicación en grid del frame de resultados
        self.txt_result.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")

        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

    # Métodos para buscar archivos
    def browse_sqldiff(self):
        filename = filedialog.askopenfilename(
            title="Select sqldiff executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
        )
        if filename:
            self.sqldiff_path.set(filename)

    def browse_db1(self):
        filename = filedialog.askopenfilename(
            title="Select database",
            filetypes=[
                ("SQLite DB", "*.db *.sqlite *.sqlite3"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.db1_path.set(filename)

    def browse_db2(self):
        filename = filedialog.askopenfilename(
            title="Select database",
            filetypes=[
                ("SQLite DB", "*.db *.sqlite *.sqlite3"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.db2_path.set(filename)

    # Lógica de ejecución
    def run_diff(self):
        sqldiff = self.sqldiff_path.get()
        db1 = self.db1_path.get()
        db2 = self.db2_path.get()

        # Validaciones iniciales
        if not db1 or not db2:
            messagebox.showerror("Error", "Please, select both databases.")
            return

        # Construir el comando comando básico
        cmd = [sqldiff]

        # Añadir flags condicionales
        if self.flag_primarykey.get():
            cmd.append("--primarykey")
        if self.flag_schema.get():
            cmd.append("--schema")
        if self.flag_summary.get():
            cmd.append("--summary")
        if self.flag_transaction.get():
            cmd.append("--transaction")

        # Añadir los argumentos de base de datos
        cmd.extend([db1, db2])

        # Limpiar la ventana de texto de ejecuciones anteriores
        self.txt_result.delete("1.0", tk.END)

        try:
            # Ejecutar sqldiff de forma segura
            # startupinfo previene que parpadee una consola CMD en Windows
            startupinfo = None
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                startupinfo=startupinfo,
            )

            # Mostrar salida en pantalla
            if result.stdout:
                self.txt_result.insert(tk.END, result.stdout)
            else:
                if result.returncode == 0:
                    self.txt_result.insert(
                        tk.END, "--- Both databases are identical ---"
                    )

            if result.stderr:
                self.txt_result.insert(tk.END, f"\n[ERRORS]:\n{result.stderr}")

        except FileNotFoundError:
            messagebox.showerror(
                "Execution error",
                f"{sqldiff} not found",
            )
        except Exception as e:
            messagebox.showerror("Unexpected error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = SqlDiffUI(root)
    root.mainloop()
