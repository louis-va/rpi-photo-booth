# rpi-photo-booth

A simple Raspberry Pi-based photo booth that captures images, displays a countdown and effects on an OLED screen, and prints photos using a thermal printer.

## Features

- Countdown timer with live camera preview on OLED display
- Flash and blink effects before photo capture
- Prints captured photo on a thermal printer
- Button-activated photo process

## Hardware Requirements

- Raspberry Pi (tested on Pi 4)
- SPI OLED display (SSD1309, 128x64)
- Thermal printer (ESC/POS compatible, serial interface)
- Push button (connected to GPIO 17)
- Camera module (compatible with Picamera2)
- Required wiring for SPI, GPIO, and serial connections

## Software Requirements

- Raspberry Pi OS Lite
- Python 3.13+
- System packages: `python3-picamera2`, `python3-serial`
- Python packages: `luma-oled`, `pillow`, `python-escpos`

## Raspberry Pi Setup

1. **Download Raspberry Pi OS Lite**  
   Use the Raspberry Pi Imager to flash the OS.  
   Enable SSH, set hostname, username/password, Wi-Fi SSID, password, and country.

2. **Connect to Raspberry Pi**  
   ```
   ssh <username>@raspberrypi.local
   ```

3. **Update System**  
   ```
   sudo apt update && sudo apt upgrade -y
   ```

4. **Install Required Packages**  
   ```
   sudo apt install git curl python3-picamera2 python3-serial -y
   ```

5. **Install uv (Python package manager)**  
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

6. **Add uv to PATH**  
   Add to your `~/.bashrc`:
   ```
   export PATH="$HOME/.cargo/bin:$PATH"
   ```

7. **Initialize Python Environment**  
   ```
   uv venv --system-site-packages
   source .venv/bin/activate
   ```

8. **Enable SPI Interface**  
   ```
   sudo raspi-config
   ```
   Select: `Interfacing Options -> SPI -> Yes`

9. **Reboot**  
   ```
   sudo reboot
   ```

10. **Set Permissions**  
    ```
    sudo usermod -aG spi,gpio $USER
    ```

## Project Setup

1. Clone this repository:
   ```
   git clone <repo-url>
   cd rpi-photo-booth
   ```

2. Install Python dependencies:
   ```
   uv pip install -r requirements.txt
   ```
   Or, if using `pyproject.toml`:
   ```
   uv pip install
   ```

3. Place `JetBrainsMono-Bold.ttf` in the project directory.

## Usage

1. Connect all hardware components.
2. Activate Python environment:
   ```
   source .venv/bin/activate
   ```
3. Run the photo booth:
   ```
   python3 main.py
   ```
4. Press the button to start the photo process.

## Notes

- Ensure the serial printer is connected to `/dev/serial0`.
- Adjust GPIO and device parameters in `main.py` if needed.
- For troubleshooting, check hardware connections and permissions.

## License

MIT