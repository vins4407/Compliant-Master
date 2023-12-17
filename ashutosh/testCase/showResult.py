import tkinter as tk

def update_content():
    with open('output.txt', 'r') as file:
        content = file.read()

    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, content)

    root.after(1000, update_content)

def main():
    global root, text_widget

    root = tk.Tk()
    root.title("Real-Time File Viewer")

    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(expand=True, fill='both')

    update_content()

    root.mainloop()

# If you want to run this file independently, without being imported
if __name__ == "__main__":
    main()
