import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox, QLabel, QHBoxLayout, QListWidget,
    QListWidgetItem, QAbstractItemView
)

class CSVAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.setWindowTitle("CSV Analyzer with Min & Max")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout()

        # Load button
        self.btn_load = QPushButton("Load CSV File")
        self.btn_load.clicked.connect(self.load_csv)
        layout.addWidget(self.btn_load)

        # X and Y selectors
        col_layout = QHBoxLayout()
        self.label_x = QLabel("X-axis:")
        self.combo_x = QComboBox()

        self.label_y = QLabel("Y-axis (multi-select):")
        self.list_y = QListWidget()
        self.list_y.setSelectionMode(QAbstractItemView.MultiSelection)

        col_layout.addWidget(self.label_x)
        col_layout.addWidget(self.combo_x)
        col_layout.addWidget(self.label_y)
        col_layout.addWidget(self.list_y)

        layout.addLayout(col_layout)

        # Plot buttons
        btn_layout = QHBoxLayout()
        self.btn_plot_line = QPushButton("Plot Line Graph")
        self.btn_plot_line.clicked.connect(self.plot_line)

        self.btn_plot_bar = QPushButton("Plot Bar Chart")
        self.btn_plot_bar.clicked.connect(self.plot_bar)

        self.btn_show_minmax = QPushButton("Show Min & Max")
        self.btn_show_minmax.clicked.connect(self.show_min_max)

        btn_layout.addWidget(self.btn_plot_line)
        btn_layout.addWidget(self.btn_plot_bar)
        btn_layout.addWidget(self.btn_show_minmax)

        layout.addLayout(btn_layout)

        # Table view
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", " ","CSV Files"," ",("*.csv"))
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.update_table()
                self.update_selectors()
                QMessageBox.information(self, "Success", f"File loaded: {file_path}\nRows: {len(self.df)} Columns: {len(self.df.columns)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file:\n{e}")

    def update_table(self):
        self.table.clear()
        if self.df is not None:
            self.table.setColumnCount(len(self.df.columns))
            self.table.setRowCount(min(50, len(self.df)))
            self.table.setHorizontalHeaderLabels(self.df.columns.tolist())

            for row in range(min(50, len(self.df))):
                for col in range(len(self.df.columns)):
                    item = QTableWidgetItem(str(self.df.iat[row, col]))
                    self.table.setItem(row, col, item)

    def update_selectors(self):
        self.combo_x.clear()
        self.list_y.clear()
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()

        self.combo_x.addItems(self.df.columns.tolist())  # Any column as X
        for col in numeric_cols:
            item = QListWidgetItem(col)
            self.list_y.addItem(item)

    def get_selected_y_columns(self):
        return [item.text() for item in self.list_y.selectedItems()]

    def plot_line(self):
        if self.df is None:
            QMessageBox.warning(self, "Warning", "Load a CSV file first!")
            return

        x_col = self.combo_x.currentText()
        y_cols = self.get_selected_y_columns()

        if not y_cols:
            QMessageBox.warning(self, "Warning", "Select at least one Y-axis column!")
            return

        self.df.plot(x=x_col, y=y_cols, kind='line', marker='o')
        plt.title(f"Line Graph: {', '.join(y_cols)} vs {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(", ".join(y_cols))
        plt.legend()
        plt.show()

    def plot_bar(self):
        if self.df is None:
            QMessageBox.warning(self, "Warning", "Load a CSV file first!")
            return

        x_col = self.combo_x.currentText()
        y_cols = self.get_selected_y_columns()

        if not y_cols:
            QMessageBox.warning(self, "Warning", "Select at least one Y-axis column!")
            return

        self.df.plot(x=x_col, y=y_cols, kind='bar')
        plt.title(f"Bar Chart: {', '.join(y_cols)} vs {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(", ".join(y_cols))
        plt.legend()
        plt.show()

    def show_min_max(self):
        if self.df is None:
            QMessageBox.warning(self, "Warning", "Load a CSV file first!")
            return

        y_cols = self.get_selected_y_columns()

        if not y_cols:
            QMessageBox.warning(self, "Warning", "Select at least one Y-axis column!")
            return

        result = ""
        for col in y_cols:
            min_val = self.df[col].min()
            max_val = self.df[col].max()
            result += f"{col}: Min = {min_val}, Max = {max_val}\n"

        QMessageBox.information(self, "Min & Max Values", result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CSVAnalyzer()
    window.show()
    sys.exit(app.exec_())
