import subprocess
import re
import customtkinter as ctk
from customtkinter import filedialog
import platform
import socket
import psutil
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tkinter as tk

class ReportGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compliance Master System Report Generator")

        self.generate_button = ctk.CTkButton(root, text="Generate Report", command=self.generate_report)
        self.generate_button.pack(pady=10)

        self.text_widget = tk.Text(root, height=20, width=80, fg="black", font=("Arial", 10))
        self.text_widget.pack(padx=10, pady=10)

        self.download_button = ctk.CTkButton(root, text="Save Report", command=self.save_report, state=tk.DISABLED)
        self.download_button.pack(pady=10)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    def generate_report(self):
        system_info = self.get_system_info()
        report_text = self.format_system_info(system_info)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, report_text)
        self.download_button.configure(state=tk.NORMAL)

    def save_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            try:
                doc = SimpleDocTemplate(file_path, pagesize=letter)
                elements = []

                styles = getSampleStyleSheet()

                report_text = self.text_widget.get(1.0, tk.END)
                report_paragraphs = [Paragraph(line, styles["Normal"]) for line in report_text.split('\n')]
                elements.extend(report_paragraphs)

                elements.append(Paragraph("\nDisk Space Usage:", styles["Heading2"]))
                disk_space_table = self.create_disk_space_table()
                elements.append(disk_space_table)

                doc.build(elements)
                self.status_label.configure(text=f"Report saved to {file_path}")
            except Exception as e:
                print(f"Error saving PDF: {e}")
                self.status_label.configure(text=f"Error saving PDF: {e}")

    def create_disk_space_table(self):
        partitions = psutil.disk_partitions()
        data = [["Filesystem", "Size", "Used", "Avail", "Use%"]]
        for partition in partitions:
            partition_info = psutil.disk_usage(partition.mountpoint)
            data.append([
                partition.device, partition_info.total, partition_info.used,
                partition_info.free, partition_info.percent
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table

    def get_memory_info(self):
        try:
            result = subprocess.run(["dmidecode", "--type", "17"], capture_output=True, text=True, check=True)
            form_factor_match = re.search(r"Form Factor:\s*(.+)", result.stdout)
            locator_match = re.search(r"Locator:\s*(.+)", result.stdout)

            form_factor = form_factor_match.group(1).strip() if form_factor_match else "N/A"
            locator = locator_match.group(1).strip() if locator_match else "N/A"

            return form_factor, locator
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving memory information: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return "N/A", "N/A"

    def get_system_info(self):
        info = {
            "Hostname": socket.gethostname(),
            "Manufacturer": platform.system(),
            "Product Name": platform.node(),
            "Serial Number": platform.processor(),
            "BIOS Version": platform.architecture(),
            "System Version": platform.version(),
            "Baseboard Manufacture": platform.machine(),
            "Baseboard Product Name": platform.processor(),
            "Baseboard Version": platform.python_compiler(),
            "Baseboard Serial Number": platform.python_version(),
        }

        try:
            battery = psutil.sensors_battery()
            info["Battery Percent"] = battery.percent if battery else None

            info["CPU Cores"] = psutil.cpu_count(logical=False)

            cpu_info = platform.uname()
            info["CPU Information"] = cpu_info if cpu_info else None

            memory_info = psutil.virtual_memory()
            info["Total Memory"] = memory_info.total if memory_info else None

            disk_info = psutil.disk_usage('/')
            info["Total Disk Space"] = disk_info.total if disk_info else None
            info["Used Disk Space"] = disk_info.used if disk_info else None
            info["Available Disk Space"] = disk_info.free if disk_info else None
            info["Disk Space Usage Percentage"] = disk_info.percent if disk_info else None

            network_info = psutil.net_if_addrs()
            info["Network Configuration"] = network_info if network_info else None

            form_factor, locator = self.get_memory_info()
            info["Memory Device"] = {
                "Total Width": memory_info.width if memory_info else None,
                "Data Width": memory_info.bits if memory_info else None,
                "Size": memory_info.total if memory_info else None,
                "Form Factor": form_factor,
                "Locator": locator,
            }

        except Exception as e:
            print(f"Error retrieving additional information: {e}")

        return info

    def format_system_info(self, info):
        formatted_info = ""
        for key, value in info.items():
            if key == "CPU Information":
                formatted_info += f"\n{key}:\n"
                for cpu_key, cpu_value in zip(value._fields, value):
                    formatted_info += f"{cpu_key}: {cpu_value}\n"
            elif key == "Total Memory":
                formatted_info += f"\nMemory Information:\n"
                formatted_info += f"{key}: {value} bytes\n"
            elif key == "Disk Space Usage Percentage":
                formatted_info += f"\nDisk Space:\n"
                formatted_info += f"{key}: {value}%\n"
                formatted_info += "Filesystem      Size  Used Avail Use% Mounted on\n"
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    partition_info = psutil.disk_usage(partition.mountpoint)
                    formatted_info += f"{partition.device}  {partition_info.total}  {partition_info.used}  {partition_info.free}  {partition_info.percent}\n"
            elif key == "Memory Device":
                formatted_info += f"\nMemory Device:\n"
                for mem_key, mem_value in value.items():
                    formatted_info += f"{mem_key}: {mem_value}\n"
            elif key == "Network Configuration":
                formatted_info += f"\n{key}:\n"
                for iface, addresses in value.items():
                    formatted_info += f"  {iface}:\n"
                    for address in addresses:
                        formatted_info += f"    {address.family.name} Address: {address.address}\n"
            else:
                formatted_info += f"{key}: {value}\n"
        return formatted_info

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGeneratorApp(root)
    root.mainloop()