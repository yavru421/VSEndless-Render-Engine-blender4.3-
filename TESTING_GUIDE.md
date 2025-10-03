# TESTING_GUIDE.md: How to Test VSEndless APT

## 🧪 **VSEndless Testing Guide**

### **Prerequisites**
- ✅ Blender 4.5+ installed
- ✅ Windows 10/11, macOS 10.15+, or Linux Ubuntu 20.04+
- ⚠️ Optional: FFmpeg with NVENC support (for GPU acceleration)
- ⚠️ Optional: NVIDIA GPU with recent drivers

### **Installation Steps**

#### **1. Install the Add-on**
```bash
1. Download: VSEndless_GPU_Render_Engine_v5.0.0_20251002.zip
2. Open Blender 4.5+
3. Go to: Edit > Preferences > Add-ons
4. Click: Install...
5. Select: VSEndless_GPU_Render_Engine_v5.0.0_20251002.zip
6. Enable: "VSEndless - GPU Accelerated Render Engine (APT)"
7. Save Preferences
```

#### **2. Verify Installation**
```bash
✅ Check for "VSEndless" tab in Video Sequence Editor sidebar
✅ Check for "VSEndless GPU Render Engine (APT)" in Render Properties
✅ Look for APT initialization messages in console
```

### **Basic Testing Workflow**

#### **Test 1: Basic Functionality**
```bash
1. Switch to Video Sequence Editor
2. Add a video file to timeline
3. Open VSEndless panel in sidebar
4. Click "Check GPU Capabilities"
5. Verify GPU detection messages
```

#### **Test 2: AI Features**
```bash
1. Select a video strip in timeline
2. Go to "VSEndless AI Engine" panel
3. Click "Analyze Timeline"
4. Check for AI recommendations
5. Try "AI Optimize Settings" → Balanced
```

#### **Test 3: Render Test**
```bash
1. Set output path in VSEndless panel
2. Choose codec (h264_nvenc if GPU available)
3. Click "VSEndless Render"
4. Check console for APT messages
5. Verify output file created
```

#### **Test 4: Advanced Features**
```bash
1. Try "AI Upscale Strip" (if strip selected)
2. Test "AI Scene Detection"
3. Check "Cloud Rendering (Pro)" panel
4. Explore different render presets
```

### **Expected Results**

#### **✅ Success Indicators:**
- VSEndless panels appear in UI
- GPU detection works (if NVIDIA GPU available)
- Basic rendering produces output file
- AI analysis provides recommendations
- No Python errors in console

#### **⚠️ Warnings (Normal):**
- "AI features not available" if numpy/cv2 missing
- "Cloud features not available" if no internet/auth
- "NVENC not detected" if no NVIDIA GPU
- "FFmpeg not found" if not in PATH

#### **❌ Failure Indicators:**
- Add-on fails to enable
- Python import errors
- UI panels don't appear
- Render operations crash Blender

### **Troubleshooting**

#### **Problem: Add-on won't enable**
```bash
Solution:
1. Check Blender version (must be 4.5+)
2. Look for errors in System Console (Window > Toggle System Console)
3. Try fresh Blender installation
```

#### **Problem: No AI features**
```bash
Solution:
1. Install: pip install numpy opencv-python
2. Restart Blender
3. Check if features appear
```

#### **Problem: GPU not detected**
```bash
Solution:
1. Update NVIDIA drivers
2. Check nvidia-smi command works
3. Install FFmpeg with NVENC support
```

#### **Problem: Render fails**
```bash
Solution:
1. Check FFmpeg installation
2. Test with simple H.264 codec first
3. Check output path permissions
4. Look for detailed errors in console
```

### **Performance Testing**

#### **Benchmark Tests:**
1. **Small Timeline** (30 seconds, 1080p)
   - Should render in under 1 minute
   - CPU usage should be moderate
   - GPU usage high if NVENC enabled

2. **AI Analysis** (1-2 minute video)
   - Analysis should complete in 10-30 seconds
   - Should provide codec/bitrate recommendations
   - Scene detection should find cuts

3. **Memory Usage**
   - Should not exceed 2GB RAM for typical projects
   - GPU VRAM usage depends on resolution

### **APT Verification**

#### **Check APT Messages:**
```bash
Expected console output:
[APT] Initializing VSEndless with Algebraic Pipeline Theory
[APT] VSEndless pipeline stages activated successfully
[VSEndless.APT] AI operators pipeline stage activated
[VSEndless.APT] Cloud operators pipeline stage activated
```

#### **Mathematical Correctness:**
- Input domains should be validated
- Render pipeline should be deterministic
- Error propagation should be algebraically sound
- Each stage should log its transformations

### **Reporting Issues**

If you find bugs, please report with:
1. **System Info:** OS, Blender version, GPU model
2. **Steps to Reproduce:** Exact sequence that caused issue
3. **Console Output:** Copy all VSEndless/APT messages
4. **Timeline Details:** Video formats, effects used
5. **Expected vs Actual:** What should have happened

### **Advanced Testing**

For developers and advanced users:

#### **Code Inspection:**
```python
# Check APT compliance in Python console:
import bpy
addon = bpy.context.preferences.addons.get('VSEndless_GPU_Render_Engine')
print(f"APT Module: {addon.module}")
```

#### **Performance Profiling:**
```python
# Time render operations:
import time
start = time.time()
# ... perform render ...
print(f"Render time: {time.time() - start:.2f}s")
```

---

**Happy Testing! The future of APT-compliant video editing awaits! 🚀🧮✨**