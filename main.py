import tkinter
import customtkinter
from typing import List

from ExportData import ExportData


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


currentVersion = "0.0.1"


class App(customtkinter.CTk):
    _data: ExportData

    def write_text_to_output(self, text: str, text_color: str = "#FFFFFF"):
        self._outputBox.configure(text_color=text_color)
        self._outputBox.configure(state="normal")
        self._outputBox.delete("1.0", customtkinter.END)
        self._outputBox.insert("0.0", text)
        self._outputBox.configure(state="disabled")

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Sam Art Checker")
        self.geometry(f"{412}x{317}")
        self.resizable(False, False)
        # self.wm_iconbitmap(resource_path("logo.ico"))

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self._data = ExportData()

        self._loadButton = customtkinter.CTkButton(
            self,
            text="Load",
            command=self.btn_event_load,
            width=100,
        )
        self._loadButton.grid(row=0, column=0, padx=0, pady=(10, 10))

        self._checkButton = customtkinter.CTkButton(
            self,
            text="Check",
            command=self.btn_event_check,
            width=100,
        )
        self._checkButton.grid(row=0, column=1, padx=0, pady=(10, 10))
        self._checkButton._state = tkinter.DISABLED
        # self._checkButton.configure(text_color_disabled="#0000FF")

        self._clearButton = customtkinter.CTkButton(
            self,
            text="Clear",
            command=self.btn_event_clear,
            width=100,
            fg_color="#E93939",
            hover_color="#922222",
        )
        self._clearButton.grid(row=0, column=2, padx=0, pady=(10, 10))

        self.version_label = customtkinter.CTkLabel(
            self,
            text="v" + currentVersion + "\nSamBaker",
            font=customtkinter.CTkFont(size=10),
        )
        self.version_label.grid(row=0, column=3, padx=0, pady=(10, 10))

        self._outputBox = customtkinter.CTkTextbox(self, width=400, height=200)
        self._outputBox.grid(
            row=1,
            rowspan=2,
            column=0,
            columnspan=4,
            padx=20,
            pady=(0, 0),
            sticky="nsew",
        )
        self._outputBox.configure(state="disabled")
        self.write_text_to_output(text="Load the export folder from the art directory.")

    def btn_event_load(self):
        self._data.load_export_path()
        if self._data._exportPath is "":
            self.write_text_to_output(
                text="Export path not loaded!", text_color="#FF0000"
            )
            self._checkButton._state = tkinter.DISABLED
            return

        self.write_text_to_output(
            text="Path loaded successfully.\nYou can now check this directory!",
            text_color="#00FF00",
        )

        self._checkButton._state = tkinter.NORMAL

    def btn_event_check(self):
        (
            atlas_count,
            oversized_files,
            max_dimension_files,
        ) = self._data.calculate_atlas_count(self._data._exportPath)

        output_str = ""

        output_str += "Number of atlases required: {}\n".format(atlas_count)
        output_str += "\n"

        if len(oversized_files) > 0:
            output_str += "PNG files exceeding the size of the atlas:\n"
            for file in oversized_files:
                output_str += file + "\n"

        output_str += "\n"

        if len(max_dimension_files) > 0:
            output_str += "PNG files exceeding 1024 width or 1024 height:\n"
            for file in max_dimension_files:
                output_str += file + "\n"

        output_str += "\n"

        output_str += "Please keep in mind this tool obviosuly does not consider any minui resources (unless you added them) or atlas hints."

        self.write_text_to_output("")
        self.write_text_to_output(output_str)

    def btn_event_clear(self):
        self.write_text_to_output(text="")


if __name__ == "__main__":
    app = App()
    app.mainloop()
