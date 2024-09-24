import os

def get_desktop_path():
    if os.name == 'nt':  # Windows
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:  # macOS/Linux
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    return desktop

desktop_path = get_desktop_path()
print(f"Desktop path: {desktop_path}")
if __name__ == '__main__':
    get_desktop_path()