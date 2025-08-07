import qrcode
import re
import os
import platform
import subprocess

def is_valid_url(url):
    return re.match(r'https?://\S+\.\S+', url)

def preview_image(path):
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", path])
        elif system == "Windows":
            os.startfile(path)
        else:  # Linux
            subprocess.run(["xdg-open", path])
    except Exception:
        print("⚠️ Could not open image automatically.")

def get_color(prompt, default):
    color = input(f"{prompt} (default: {default}): ").strip().lower()
    return color if color else default

def generate_qr_code():
    url = input("🔗 Enter the URL to generate a QR code: ").strip()
    if not url:
        print("❌ No URL provided. Exiting.")
        return
    if not is_valid_url(url):
        print("❌ Invalid URL. It must start with http:// or https://")
        return

    filename = input("💾 Enter a filename to save (default: qr.png): ").strip()
    if not filename:
        filename = "qr.png"
    elif not filename.lower().endswith(".png"):
        filename += ".png"

    # Ask for color choices
    print("\n🎨 Let's customize the QR code colors!")
    fill_color = get_color("🔵 Enter foreground (QR) color", "black")
    back_color = get_color("⚪ Enter background color", "white")

    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(filename)

        print(f"\n✅ QR code saved as '{filename}' in '{os.getcwd()}'")

        view = input("👀 Do you want to preview the QR code? (y/n): ").strip().lower()
        if view == 'y':
            preview_image(filename)

    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️ Try using valid color names like 'black', 'white', 'blue', 'red', etc.")

if __name__ == "__main__":
    generate_qr_code()
