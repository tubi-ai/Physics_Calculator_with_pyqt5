import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, 
    QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox
)
from PyQt5.QtCore import Qt

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Physics Calculator")
        self.setGeometry(100, 100, 600, 800)
        
        # Track the last active entry
        self.active_entry = None

        # Creat central widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create three tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Ohm's Law: V = I * R")
        self.tabs.addTab(self.tab2, "Ampère's Law: B = μ * I / (2 * π * r)")
        self.tabs.addTab(self.tab3, "Faraday's Law: E = - ΔΦ / Δt")

        # Create layouts and add components for each tab
        self.create_tab1_layout()
        self.create_tab2_layout()
        self.create_tab3_layout()

        # Add equality and reset buttons
        button_layout = QVBoxLayout()
        self.equal_button = QPushButton("=")
        self.equal_button.clicked.connect(self.calculate)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)

        button_layout.addWidget(self.equal_button)
        button_layout.addWidget(self.reset_button)
        main_layout.addLayout(button_layout)

    def create_tab1_layout(self):
        layout = QGridLayout(self.tab1)
        self.combo_ohm = QComboBox()
        self.combo_ohm.addItems(["Voltage (V) & Resistance (R)", 
                                 "Voltage (V) & Current (I)", 
                                 "Resistance (R) & Current (I)"])
        layout.addWidget(self.combo_ohm, 0, 0, 1, 2)

        self.entry_ohm = self.create_entry_with_label(layout, "R =", "Ω", 1)
        self.entry_volt = self.create_entry_with_label(layout, "V =", "V", 2)
        self.entry_current = self.create_entry_with_label(layout, "I =", "A", 3)
        
        # Create button set
        grid = QGridLayout()
        self.create_buttons(grid)
        layout.addLayout(grid, 4, 0, 1, 3)  # Example row/column values

    def create_tab2_layout(self):
        layout = QGridLayout(self.tab2)
        self.combo_amp = QComboBox()
        self.combo_amp.addItems([
            "Magnetic Field (B) & Current (I) & μ", 
            "Radius (r) & Current (I) & μ",
            "B & r & μ", 
            "B & I & r"
        ])
        layout.addWidget(self.combo_amp, 0, 0, 1, 2)

        self.entry_B = self.create_entry_with_label(layout, "B =", "T", 1)
        self.entry_I = self.create_entry_with_label(layout, "I =", "A", 2)
        self.entry_r = self.create_entry_with_label(layout, "r =", "m", 3)
        self.entry_mu = self.create_entry_with_label(layout, "μ =", "H/m", 4)
        
        # Create button set
        grid = QGridLayout()
        self.create_buttons(grid)
        layout.addLayout(grid, 9, 0, 1, 3)  # Example row/column values

    def create_tab3_layout(self):
        layout = QGridLayout(self.tab3)
        self.combo_far = QComboBox()
        self.combo_far.addItems([
            "E & ΔΦ", 
            "ΔΦ & Δt", 
            "E & Δt"
        ])
        layout.addWidget(self.combo_far, 0, 0, 1, 2)

        self.entry_df = self.create_entry_with_label(layout, "ΔΦ =", "Wb", 1)
        self.entry_dt = self.create_entry_with_label(layout, "Δt =", "s", 2)
        self.entry_E = self.create_entry_with_label(layout, "E =", "V", 3)
        
        # Create button set
        grid = QGridLayout()
        self.create_buttons(grid)
        layout.addLayout(grid, 4, 0, 1, 3)  # Example row/column values


    def create_buttons(self, layout):
        """Tuş takımı oluştur ve grid içine ekle."""
        buttons = [
                ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
                ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
                ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
                ('.', 3, 0), ('0', 3, 1), ('Delete', 3, 2)
            ]
    
        for (text, row, col) in buttons:
            button = QPushButton(text)
            button.clicked.connect(lambda _, t=text: self.command_callback(t))
            layout.addWidget(button, row, col)
    
        # Widen grid columns and rows equally
        for i in range(3):
            layout.setColumnStretch(i, 1)
        for j in range(4):
            layout.setRowStretch(j, 1)

    def command_callback(self, value):
        """Butonların tıklanma olayını işler."""
        if self.active_entry:
            if value == 'Delete':
                self.active_entry.backspace()
            else:
                self.active_entry.insert(value)

    def create_entry_with_label(self, layout, label_text, unit_text, row):
        label = QLabel(label_text)
        entry = QLineEdit()
        unit_label = QLabel(unit_text)

        entry.focusInEvent = lambda _: self.set_active_entry(entry)

        layout.addWidget(label, row, 0)
        layout.addWidget(entry, row, 1)
        layout.addWidget(unit_label, row, 2)

        return entry

    def set_active_entry(self, entry):
        """Set the currently active entry field."""
        self.active_entry = entry

    def calculate(self):
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:  # Ohm's Law
            v = self.get_value(self.entry_volt)
            r = self.get_value(self.entry_ohm)
            i = self.get_value(self.entry_current)

            if "Resistance (R) & Current (I)" in self.combo_ohm.currentText():
                result = r * i
                self.entry_volt.setText(str(result))
            elif "Voltage (V) & Resistance (R)" in self.combo_ohm.currentText():
                result = v / r if r != 0 else "Error"
                self.entry_current.setText(str(result))
            elif "Voltage (V) & Current (I)" in self.combo_ohm.currentText():
                result = v / i if i != 0 else "Error"
                self.entry_ohm.setText(str(result))

        elif current_tab == 1:  # Ampère's Law
            b_combobox = self.combo_amp.currentText()
            I = self.get_value(self.entry_I)
            r = self.get_value(self.entry_r)
            mu = self.get_value(self.entry_mu)
            B = self.get_value(self.entry_B)
            
            if "Magnetic Field (B) & Current (I) & μ" in b_combobox:
                result = (mu * I) / (2 * 3.14159 * B) if B!=0 else "Error: Magnetic Field cannot be zero!"
                self.entry_r.setText(str(result))
      
            elif "Radius (r) & Current (I) & μ" in b_combobox:
                result = (mu * I) / (2 * 3.14159 * r)  if r != 0 else "Error: Radius cannot be zero!"
                self.entry_B.setText(str(result))
                                      
            elif "B & r & μ" in b_combobox:
                result = (B * (2 * 3.14159 * r)) / mu  if mu != 0 else "Error: Magnetic Permeability of the Medium cannot be zero!"                           
                self.entry_I.setText(str(result))
               
            elif "B & I & r" in b_combobox:
                result = (B * (2 * 3.14159 * r)) / I if I != 0 else "Error: Current cannot be zero!"
                self.entry_mu.setText(str(result))
            

        elif current_tab == 2:  # Faraday's Law
            f_combobox = self.combo_far.currentText()
            dphi = self.get_value(self.entry_df)
            dt = self.get_value(self.entry_dt)
            E = self.get_value(self.entry_E)
           
            if "ΔΦ & Δt" in f_combobox:
                result = -dphi / dt if dt != 0 else "Error: Current cannot be zero!"
                self.entry_E.setText(str(result))
                
            elif "E & Δt" in f_combobox:
                result = -E * dt
                self.entry_df.setText(str(result))
                
            elif "E & ΔΦ" in f_combobox:
                result = -dphi / E if E != 0 else "Error: Current cannot be zero!"
                self.entry_dt.setText(str(result))

    def reset(self):
        # Clear all input fields
        for entry in [self.entry_ohm, self.entry_volt, self.entry_current, 
                      self.entry_B, self.entry_I, self.entry_r, 
                      self.entry_mu, self.entry_df, self.entry_dt, self.entry_E]:
            entry.clear()

    def get_value(self, entry):
        try:
            return float(entry.text())
        except ValueError:
            return 0.0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
