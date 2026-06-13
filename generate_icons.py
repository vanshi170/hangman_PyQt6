import os

def create_svgs():
    os.makedirs(r'c:\Users\VICTUS\Desktop\Desktop Data\hangman_python\assets\icons', exist_ok=True)
    
    colors = {
        'light': '#000000',
        'dark': '#ffffff'
    }
    
    # SVG Paths
    sun_path = "M12 4V2M12 22v-2M4 12H2m20 0h-2m-2.05-6.95l1.41-1.41M5.64 18.36l1.41-1.41m12.73 0l-1.41-1.41M5.64 5.64l1.41 1.41M12 17a5 5 0 100-10 5 5 0 000 10z"
    moon_path = "M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"
    up_arrow_path = "M18 15l-6-6-6 6"
    down_arrow_path = "M6 9l6 6 6-6"
    check_path = "M20 6L9 17l-5-5"
    
    base_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{path}"/></svg>'
    
    icons = [
        ('sun', sun_path),
        ('moon', moon_path),
        ('up_arrow', up_arrow_path),
        ('down_arrow', down_arrow_path),
        ('check', check_path)
    ]
    
    for theme, color in colors.items():
        for name, path in icons:
            filename = rf'c:\Users\VICTUS\Desktop\Desktop Data\hangman_python\assets\icons\{name}_{theme}.svg'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(base_svg.format(color=color, path=path))
                
if __name__ == '__main__':
    create_svgs()
    print("SVGs created successfully.")
