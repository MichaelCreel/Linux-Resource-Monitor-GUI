# Resource Monitor

A graphical Resource Monitor designed for Linux systems. Displays the average CPU usage over all cores, memory usage, and GPU usage. Based on my C-based terminal version, [Linux Resource Monitor](https://github.com/MichaelCreel/Linux-Resource-Monitor).

## Dependencies

- Python
  ```bash
  sudo apt install python3
- GPU:
  - nvidia-smi (for NVIDIA cards)
  - amdgpu_top (for AMD cards)
  - intel_gpu_top (for Intel cards)

## Installation

1. Open a terminal `Ctrl + Alt + T`
2. Clone the repository
   ```bash
   git clone https://github.com/MichaelCreel/Linux-Resource-Monitor-GUI
4. Open app directory
   ```bash
   cd ~/Linux-Resource-Monitor-GUI/
5. Run app
   ```bash
   python3 resource-monitor-gui.py

## Notes

- If GPU tools are not found, your GPU usage will remain undetected
- Designed for Debian
- Root access required for intel_gpu_top
- Tested with an NVIDIA graphics card

## License
MIT License
