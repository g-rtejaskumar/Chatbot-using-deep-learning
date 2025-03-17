import os
import shutil

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".js", ".html", ".css", ".php"],
    "Others": []  
}

def organize_folder(folder_path):
    """Organizes files in the given folder into categorized subfolders."""
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist!")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isdir(file_path):
            continue

        _, extension = os.path.splitext(filename)
        category = "Others" 

        for cat, extensions in FILE_CATEGORIES.items():
            if extension.lower() in extensions:
                category = cat
                break

        category_folder = os.path.join(folder_path, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        shutil.move(file_path, os.path.join(category_folder, filename))

    print(f"Files in {folder_path} have been organized successfully!")

if __name__ == "__main__":
    folder_to_organize = input("Enter the full path of the folder you want to organize: ")
    organize_folder(folder_to_organize)
