import filecmp, os
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar
from ttkbootstrap import Style

def compare_files_in_folders(folder1, folder2):
    dcmp = filecmp.dircmp(folder1, folder2)

    only_in_folder1 = dcmp.left_only
    only_in_folder2 = dcmp.right_only
    temp = dcmp.common_files
    different_content_files = []
    common_files = []

    for file in temp:
        file1_path = f"{folder1}/{file}"
        file2_path = f"{folder2}/{file}"

        # Compare if two files are equal
        are_files_equal = filecmp.cmp(file1_path, file2_path)

        if are_files_equal:
            common_files.append(file)
        else:
            different_content_files.append(file)

    return only_in_folder1, only_in_folder2, common_files, different_content_files

def browse_folder(entry):
    folder_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_path)

def compare_folders():
    folder1_path = entry_folder1.get()
    folder2_path = entry_folder2.get()

    if not folder1_path or not folder2_path:
        result_list_only_in_folder1.delete(0, tk.END)
        result_list_only_in_folder1.insert(tk.END, "请指定两个文件夹")
        result_list_only_in_folder2.delete(0, tk.END)
        result_list_only_in_folder2.insert(tk.END, "")
        result_list_common_files.delete(0, tk.END)
        result_list_common_files.insert(tk.END, "")
        result_list_different_content.delete(0, tk.END)
        result_list_different_content.insert(tk.END, "")
        return

    only_in_folder1, only_in_folder2, common_files, different_content_files = compare_files_in_folders(folder1_path, folder2_path)

    result_list_only_in_folder1.delete(0, tk.END)
    result_list_only_in_folder1.insert(tk.END, *only_in_folder1)
    result_list_only_in_folder2.delete(0, tk.END)
    result_list_only_in_folder2.insert(tk.END, *only_in_folder2)
    result_list_common_files.delete(0, tk.END)
    result_list_common_files.insert(tk.END, *common_files)
    result_list_different_content.delete(0, tk.END)
    result_list_different_content.insert(tk.END, *different_content_files)

def delete_selected_files(current_listbox):
    if current_listbox in (result_list_only_in_folder1, result_list_only_in_folder2):
        folder_path = entry_folder1.get() if current_listbox == result_list_only_in_folder1 else entry_folder2.get()
        selected_indices = current_listbox.curselection()
        for index in reversed(selected_indices):
            file_name = current_listbox.get(index)
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
    if current_listbox in (result_list_common_files, result_list_different_content):
        selected_indices = current_listbox.curselection()
        for index in reversed(selected_indices):
            file_name = current_listbox.get(index)
            file_path = os.path.join(entry_folder1.get(), file_name)
            os.remove(file_path)
            file_path = os.path.join(entry_folder2.get(), file_name)
            os.remove(file_path)
    compare_folders()

def copy_selected_files(current_listbox):
    print("暂时无法复制")
#     selected_indices = current_listbox.curselection()
#     copied_files = []
#     if current_listbox in (result_list_only_in_folder1, result_list_only_in_folder2, result_list_common_files, result_list_different_content):
#         folder_path = entry_folder2.get() if current_listbox == result_list_only_in_folder2 else entry_folder1.get()
#         for index in selected_indices:
#             file_name = current_listbox.get(index)
#             file_path = os.path.join(folder_path, file_name)
#             copied_files.append(file_path)

#     # Join the copied file paths and copy to clipboard
#     clipboard_text = "\n".join(copied_files)
#     pyperclip.copy(clipboard_text)

# Create main window
root = tk.Tk()
root.title("文件夹比较工具")
root.geometry("560x380")
# 主题修改 可选['cyborg', 'journal', 'darkly', 'flatly' 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'superhero','sandstone']
Style(theme='pulse')  

# Folder 1 entry and browse button
label_folder1 = tk.Label(root, text="文件夹1:")
label_folder1.place(x=10, y=10)
entry_folder1 = tk.Entry(root, width=60)
entry_folder1.place(x=65, y=10)
button_browse1 = tk.Button(root, text="浏览", width=6, command=lambda: browse_folder(entry_folder1))
button_browse1.place(x=500, y=8)

# Folder 2 entry and browse button
label_folder2 = tk.Label(root, text="文件夹2:")
label_folder2.place(x=10, y=40)
entry_folder2 = tk.Entry(root, width=60)
entry_folder2.place(x=65, y=40)
button_browse2 = tk.Button(root, text="浏览", width=6, command=lambda: browse_folder(entry_folder2))
button_browse2.place(x=500, y=38)

# Compare button and result display
button_compare = tk.Button(root, text="比较文件夹", width=10, command=compare_folders)
button_compare.place(x=235, y=70)

# Use Listbox component to display comparison results with scrollbars
result_list_only_in_folder1 = Listbox(root, height=5, width=35, selectmode=tk.MULTIPLE)
result_list_only_in_folder1.place(x=10, y=100+25)
scrollbar_only_in_folder1 = Scrollbar(root, command=result_list_only_in_folder1.yview)
scrollbar_only_in_folder1.place(x=10+250, y=100+25, height=95)
result_list_only_in_folder1.config(yscrollcommand=scrollbar_only_in_folder1.set)
label_only_in_folder1 = tk.Label(root, text="Only in Folder 1:")
label_only_in_folder1.place(x=10, y=100)

result_list_only_in_folder2 = Listbox(root, height=5, width=35, selectmode=tk.MULTIPLE)
result_list_only_in_folder2.place(x=285, y=100+25)
scrollbar_only_in_folder2 = Scrollbar(root, command=result_list_only_in_folder2.yview)
scrollbar_only_in_folder2.place(x=285+250, y=100+25, height=95)
result_list_only_in_folder2.config(yscrollcommand=scrollbar_only_in_folder2.set)
label_only_in_folder2 = tk.Label(root, text="Only in Folder 2:")
label_only_in_folder2.place(x=285, y=100)

result_list_common_files = Listbox(root, height=5, width=35, selectmode=tk.MULTIPLE)
result_list_common_files.place(x=10, y=220+25)
scrollbar_common_files = Scrollbar(root, command=result_list_common_files.yview)
scrollbar_common_files.place(x=10+250, y=220+25, height=95)
result_list_common_files.config(yscrollcommand=scrollbar_common_files.set)
label_common_files = tk.Label(root, text="Common Files:")
label_common_files.place(x=10, y=220)

result_list_different_content = Listbox(root, height=5, width=35, selectmode=tk.MULTIPLE)
result_list_different_content.place(x=285, y=220+25)
scrollbar_different_content = Scrollbar(root, command=result_list_different_content.yview)
scrollbar_different_content.place(x=285+250, y=220+25, height=95)
result_list_different_content.config(yscrollcommand=scrollbar_different_content.set)
label_different_content = tk.Label(root, text="Different Content Files:")
label_different_content.place(x=285, y=220)

button_delete = tk.Button(root, text="删除", width=10, command=lambda: delete_selected_files(root.focus_get()))
button_delete.place(x=170, y=345)
button_copy = tk.Button(root, text="复制", width=10, command=lambda: copy_selected_files(root.focus_get()))
button_copy.place(x=300, y=345)

# Start the main loop
root.mainloop()
