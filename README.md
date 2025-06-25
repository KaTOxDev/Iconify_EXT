# Iconify_EXT

**Iconify_EXT** is a simple Windows utility to associate custom file extensions with icons and (optionally) applications, using a user-friendly PyQt6 GUI.

## Features

- Assign a custom icon (`.ico`) to any file extension.
- Optionally associate an application to open files of that type.
- Restart Windows Explorer from the app to apply changes immediately.
- Simple, modern PyQt6 interface.

## Requirements

- Windows OS
- Python 3.8+
- [PyQt6](https://pypi.org/project/PyQt6/)

Install requirements with:

```
pip install -r requirements.txt
```

## Usage

1. **Run as Administrator:**  
   The app will prompt for admin rights if not already running as admin (required for registry changes).

2. **Set File Extension:**  
   Enter the file extension you want to associate (e.g., `.kato`).

3. **Choose Icon:**  
   Browse and select a `.ico` file to use as the icon.

4. **(Optional) Associate App:**  
   Browse and select an application (`.exe`) to open files of this type.

5. **Apply Association:**  
   Click "🔥 Apply Association" to write the changes to the Windows registry.

6. **Restart Explorer:**  
   Click "♻️ Restart Explorer" to refresh icons and associations.

## Running

```bash
python main.py
```

## Notes

- **Administrator rights are required** to modify file associations and icons.
- Changes affect all users on the system.
- Use with caution; incorrect registry edits can affect system behavior.

## License

MIT License

---
Made with