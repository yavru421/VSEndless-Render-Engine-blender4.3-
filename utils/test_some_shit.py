#!/usr/bin/env python3
"""
VSEndless Render Engine Compatibility Test Script
This script checks if your system meets the requirements to use VSEndless 2.0
with GPU acceleration features.
"""

import os
import sys
import platform
import subprocess
import shutil
import json
import re
from pathlib import Path
import tempfile

# ANSI color codes for prettier output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD} {text} {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_section(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}[+] {text}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"  {text}")

def check_command_exists(command):
    """Check if a command exists in the system PATH"""
    return shutil.which(command) is not None

def run_command(command, shell=False):
    """Run a command and return its output"""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell,
            check=False
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def check_system():
    """Check basic system requirements"""
    print_section("System Information")
    
    # OS info
    print_info(f"Operating System: {platform.system()} {platform.release()} {platform.version()}")
    print_info(f"Architecture: {platform.machine()}")
    print_info(f"Python Version: {platform.python_version()}")
    
    # CPU info
    if platform.system() == "Windows":
        stdout, stderr, _ = run_command("wmic cpu get name", shell=True)
        if stdout:
            cpu_info = stdout.strip().split('\n')
            if len(cpu_info) > 1:
                print_info(f"CPU: {cpu_info[1].strip()}")
    elif platform.system() == "Linux":
        stdout, stderr, _ = run_command(["grep", "model name", "/proc/cpuinfo"])
        if stdout:
            cpu_info = stdout.strip().split('\n')[0]
            cpu_model = cpu_info.split(':')[1].strip() if ':' in cpu_info else "Unknown"
            print_info(f"CPU: {cpu_model}")
    elif platform.system() == "Darwin":  # macOS
        stdout, stderr, _ = run_command(["sysctl", "-n", "machdep.cpu.brand_string"])
        if stdout:
            print_info(f"CPU: {stdout.strip()}")
    
    # Memory info
    import psutil
    virtual_memory = psutil.virtual_memory()
    total_ram_gb = round(virtual_memory.total / (1024**3), 2)
    print_info(f"Total RAM: {total_ram_gb} GB")

    if total_ram_gb < 8:
        print_warning("Less than 8GB RAM detected. VSEndless may experience performance issues.")
    else:
        print_success(f"RAM size is sufficient ({total_ram_gb} GB)")

def check_ffmpeg():
    """Check FFmpeg installation and capabilities"""
    print_section("FFmpeg Information")
    
    if not check_command_exists("ffmpeg"):
        print_error("FFmpeg is not installed or not in PATH")
        print_info("  Please install FFmpeg: https://ffmpeg.org/download.html")
        return False
    
    # Get FFmpeg version
    stdout, stderr, _ = run_command(["ffmpeg", "-version"])
    if not stdout:
        print_error("Failed to get FFmpeg version")
        return False
    
    version_line = stdout.split('\n')[0]
    print_info(f"FFmpeg Version: {version_line}")
    print_success("FFmpeg is installed!")
    
    # Check if FFmpeg supports CUDA
    if "enable-cuda" not in stdout and "enable-nvenc" not in stdout:
        print_warning("FFmpeg is not compiled with CUDA and NVENC support")
        print_info("  To enable GPU acceleration, you need FFmpeg with CUDA and NVENC support")
        print_info("  Please download a version from: https://github.com/BtbN/FFmpeg-Builds/releases")
    else:
        print_success("FFmpeg has GPU acceleration support!")
        
        if "enable-cuda" in stdout:
            print_info("  ✓ CUDA support detected")
        if "enable-nvenc" in stdout:
            print_info("  ✓ NVENC support detected")
        if "enable-nvdec" in stdout:
            print_info("  ✓ NVDEC support detected")
    
    # Check ffmpeg encoders
    stdout, stderr, _ = run_command(["ffmpeg", "-encoders"])
    
    h264_encoders = [line for line in stdout.split('\n') if "h264" in line]
    hevc_encoders = [line for line in stdout.split('\n') if "hevc" in line]
    
    print_info("\nAvailable H.264 Encoders:")
    if any("nvenc" in line for line in h264_encoders):
        print_success("  ✓ h264_nvenc detected (Hardware accelerated H.264)")
    else:
        print_warning("  ⚠ h264_nvenc not detected (Hardware accelerated H.264 unavailable)")
    
    print_info("\nAvailable H.265/HEVC Encoders:")
    if any("nvenc" in line for line in hevc_encoders):
        print_success("  ✓ hevc_nvenc detected (Hardware accelerated H.265)")
    else:
        print_warning("  ⚠ hevc_nvenc not detected (Hardware accelerated H.265 unavailable)")
    
    return True

def check_nvidia_gpu():
    """Check for NVIDIA GPU and its capabilities"""
    print_section("NVIDIA GPU Information")
    
    # Check if nvidia-smi is available (indicates NVIDIA drivers are installed)
    if not check_command_exists("nvidia-smi"):
        print_error("nvidia-smi not found. NVIDIA drivers might not be installed.")
        print_info("  Please install NVIDIA drivers: https://www.nvidia.com/Download/index.aspx")
        return False
    
    # Get GPU info using nvidia-smi
    stdout, stderr, _ = run_command(["nvidia-smi", "--query-gpu=name,driver_version,memory.total,compute_mode", "--format=csv,noheader,nounits"])
    
    if not stdout:
        print_error("Failed to get NVIDIA GPU information")
        return False
    
    gpu_info = stdout.strip().split(',')
    if len(gpu_info) >= 3:
        gpu_name = gpu_info[0].strip()
        driver_version = gpu_info[1].strip()
        memory_mb = float(gpu_info[2].strip())
        memory_gb = round(memory_mb / 1024, 2)
        
        print_info(f"GPU: {gpu_name}")
        print_info(f"Driver Version: {driver_version}")
        print_info(f"Total GPU Memory: {memory_gb} GB")
        print_success("NVIDIA GPU detected!")
        
        # Check driver version
        driver_version_num = float(".".join(driver_version.split('.')[:2]))
        if driver_version_num < 450.0:
            print_warning(f"Your NVIDIA driver ({driver_version}) may be outdated. Recommend version 450.0+")
        else:
            print_success(f"NVIDIA driver version is sufficient ({driver_version})")
        
        # Check VRAM
        if memory_gb < 4:
            print_warning(f"GPU has only {memory_gb}GB VRAM. Performance may be limited.")
        else:
            print_success(f"GPU VRAM size is sufficient ({memory_gb} GB)")
    else:
        print_error("Failed to parse NVIDIA GPU information")
        return False
    
    return True

def check_cuda():
    """Check CUDA installation"""
    print_section("CUDA Information")
    
    # Check for nvcc (CUDA compiler)
    if check_command_exists("nvcc"):
        stdout, stderr, _ = run_command(["nvcc", "--version"])
        if stdout:
            cuda_version_match = re.search(r'V(\d+\.\d+\.\d+)', stdout)
            if cuda_version_match:
                cuda_version = cuda_version_match.group(1)
                print_info(f"CUDA Version: {cuda_version}")
                print_success("CUDA toolkit is installed!")
            else:
                print_error("Failed to determine CUDA version")
    else:
        # Alternative: try nvidia-smi to get CUDA version
        stdout, stderr, _ = run_command(["nvidia-smi"])
        if stdout:
            cuda_version_match = re.search(r'CUDA Version: (\d+\.\d+)', stdout)
            if cuda_version_match:
                cuda_version = cuda_version_match.group(1)
                print_info(f"CUDA Version: {cuda_version}")
                print_success("CUDA is available through NVIDIA drivers!")
            else:
                print_warning("CUDA version information not found")
                print_info("  CUDA toolkit might not be installed, but may not be needed if FFmpeg can use NVENC")
        else:
            print_warning("CUDA toolkit not detected")
            print_info("  CUDA toolkit installation is recommended for best performance")
            print_info("  Download from: https://developer.nvidia.com/cuda-downloads")
    
    return True

def test_gpu_transcoding():
    """Test GPU transcoding capabilities with a simple FFmpeg command"""
    print_section("GPU Transcoding Test")
    
    # Create a test video file
    temp_dir = tempfile.gettempdir()
    test_input = Path(temp_dir) / "vsendless_test_input.mp4"
    test_output = Path(temp_dir) / "vsendless_test_output.mp4"
    
    # Create a test video if it doesn't exist
    if not test_input.exists():
        print_info("Creating a test video file...")
        # Generate a 5-second test video with a color pattern
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=duration=5:size=1920x1080:rate=30", 
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(test_input)
        ]
        stdout, stderr, returncode = run_command(cmd)
        
        if returncode != 0:
            print_error("Failed to create test video")
            print_info(f"Error: {stderr}")
            return False
    
    # Test NVENC encoding
    print_info("Testing NVENC encoding...")
    cmd = [
        "ffmpeg", "-y", "-hwaccel", "cuda", "-hwaccel_output_format", "cuda",
        "-i", str(test_input), "-c:v", "h264_nvenc", "-preset", "p3", 
        "-b:v", "5M", "-t", "3", str(test_output)
    ]
    
    start_time = os.times().system
    stdout, stderr, returncode = run_command(cmd)
    end_time = os.times().system
    elapsed_time = end_time - start_time
    
    if returncode != 0:
        print_error("NVENC encoding test failed")
        print_info(f"Error: {stderr}")
        return False
    
    print_success("NVENC encoding test successful!")
    print_info(f"Encoding time: {elapsed_time:.2f} seconds")
    
    # Test CUDA filters
    print_info("\nTesting CUDA filters...")
    cmd = [
        "ffmpeg", "-y", "-hwaccel", "cuda", "-hwaccel_output_format", "cuda",
        "-i", str(test_input), 
        "-vf", "scale_cuda=1280:720",
        "-c:v", "h264_nvenc", "-preset", "p3", 
        "-b:v", "5M", "-t", "3", 
        str(test_output).replace('.mp4', '_scaled.mp4')
    ]
    
    stdout, stderr, returncode = run_command(cmd)
    
    if returncode != 0:
        print_error("CUDA filters test failed")
        print_info(f"Error: {stderr}")
        print_warning("Your FFmpeg may not support CUDA filters")
    else:
        print_success("CUDA filters test successful!")
    
    # Clean up test files
    try:
        if test_input.exists():
            test_input.unlink()
        if test_output.exists():
            test_output.unlink()
        scaled_output = Path(str(test_output).replace('.mp4', '_scaled.mp4'))
        if scaled_output.exists():
            scaled_output.unlink()
    except:
        print_warning("Failed to clean up test files")
    
    return True

def generate_report():
    """Generate a summary report"""
    print_header("VSEndless Compatibility Report Summary")
    
    # System requirements
    print_success("System check complete!")
    print_info("For best results with VSEndless Render Engine 2.0:")
    print_info("1. Make sure FFmpeg is installed with CUDA and NVENC support")
    print_info("2. Keep your NVIDIA drivers updated")
    print_info("3. For best performance, use an NVIDIA GPU with at least 4GB VRAM")
    print_info("\nIf any tests failed, please check the error messages above and fix the issues.")
    print_info("For more information, visit: https://github.com/yavru421/VSEndless-Render-Engine-blender4.3-")

def main():
    print_header("VSEndless Render Engine 2.0 Compatibility Test")
    print_info("This script will check if your system meets the requirements to run VSEndless 2.0")
    print_info("with full GPU acceleration capabilities.\n")
    
    # Run all checks
    check_system()
    has_ffmpeg = check_ffmpeg()
    has_nvidia_gpu = check_nvidia_gpu()
    
    if has_ffmpeg and has_nvidia_gpu:
        check_cuda()
        test_gpu_transcoding()
    
    generate_report()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print_warning("\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nAn unexpected error occurred: {str(e)}")
        sys.exit(1)
