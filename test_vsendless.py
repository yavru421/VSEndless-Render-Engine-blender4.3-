# test_vsendless.py: APT testing framework for VSEndless
# Quick validation of module imports and basic functionality

import sys
import importlib.util
import traceback
from pathlib import Path

def test_import_safety():
    """Test if VSEndless modules can be imported without errors"""
    print("🧪 Testing VSEndless Module Imports (APT Validation)")
    print("=" * 60)

    # Test basic Python imports first
    basic_modules = [
        'bpy',  # Might not be available outside Blender
        'logging',
        'subprocess',
        'json',
        'threading'
    ]

    print("\n📦 Testing Basic Dependencies:")
    for module in basic_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            if module == 'bpy':
                print(f"  ⚠️  {module} (Expected - only available in Blender)")
            else:
                print(f"  ❌ {module}: {e}")

    # Test optional dependencies
    optional_modules = [
        ('numpy', 'AI processing features'),
        ('cv2', 'Computer vision and scene detection'),
        ('requests', 'Cloud rendering features')
    ]

    print("\n🔬 Testing Optional Dependencies:")
    for module, feature in optional_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} - {feature}")
        except ImportError:
            print(f"  ⚠️  {module} - {feature} (Optional - install for full features)")

    print("\n🏗️  APT Module Structure Validation:")

    # Check if we can find the module files
    current_dir = Path(__file__).parent
    expected_files = [
        '__init__.py',
        'operators/__init__.py',
        'operators/render_operator.py',
        'operators/ai_operators.py',
        'operators/cloud_operators.py',
        'properties/__init__.py',
        'properties/render_properties.py',
        'ui/__init__.py',
        'ui/render_panel.py',
        'ui/ai_panel.py',
        'utils/__init__.py',
        'utils/ffmpeg_utils.py',
        'utils/ai_processor.py',
        'utils/cloud_renderer.py',
        'APT_METHODOLOGY.md'
    ]

    for file_path in expected_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - Missing!")

    print("\n🔍 Syntax Validation:")

    # Test Python syntax on key files
    python_files = [
        '__init__.py',
        'operators/render_operator.py',
        'utils/ffmpeg_utils.py'
    ]

    for file_path in python_files:
        full_path = current_dir / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                compile(source, str(full_path), 'exec')
                print(f"  ✅ {file_path} - Syntax OK")
            except SyntaxError as e:
                print(f"  ❌ {file_path} - Syntax Error: {e}")
            except Exception as e:
                print(f"  ⚠️  {file_path} - Warning: {e}")
        else:
            print(f"  ❌ {file_path} - File not found")

def test_apt_compliance():
    """Test APT methodology compliance"""
    print("\n🧮 Testing APT Compliance:")
    print("-" * 40)

    # Check for APT headers in modules
    apt_files = [
        '__init__.py',
        'operators/__init__.py',
        'ui/__init__.py',
        'utils/__init__.py'
    ]

    for file_path in apt_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                has_apt_notation = "Algebraic Notation" in content
                has_input_output = "Inputs:" in content or "Input:" in content

                if has_apt_notation and has_input_output:
                    print(f"  ✅ {file_path} - Full APT compliance")
                elif has_apt_notation:
                    print(f"  🔶 {file_path} - APT notation present")
                else:
                    print(f"  ⚠️  {file_path} - No APT notation")

            except Exception as e:
                print(f"  ❌ {file_path} - Error reading: {e}")

def test_blender_compatibility():
    """Test Blender-specific compatibility"""
    print("\n🎨 Testing Blender Compatibility:")
    print("-" * 40)

    # Check bl_info structure
    try:
        with open('__init__.py', 'r', encoding='utf-8') as f:
            content = f.read()

        if 'bl_info' in content:
            print("  ✅ bl_info found")

            # Check required fields
            required_fields = ['name', 'version', 'blender', 'category']
            for field in required_fields:
                if f'"{field}"' in content:
                    print(f"    ✅ {field} field present")
                else:
                    print(f"    ❌ {field} field missing")
        else:
            print("  ❌ bl_info not found - Required for Blender add-ons")

    except Exception as e:
        print(f"  ❌ Error checking bl_info: {e}")

def test_package_structure():
    """Test package structure"""
    print("\n📦 Testing Package Structure:")
    print("-" * 40)

    # Check ZIP contents
    import zipfile

    zip_files = list(Path('.').glob('VSEndless_GPU_Render_Engine_v*.zip'))

    if zip_files:
        latest_zip = max(zip_files, key=lambda x: x.stat().st_mtime)
        print(f"  📁 Found package: {latest_zip}")

        try:
            with zipfile.ZipFile(latest_zip, 'r') as zf:
                files = zf.namelist()

                # Check for proper nested structure
                has_addon_dir = any(f.startswith('VSEndless_GPU_Render_Engine/') for f in files)
                has_init = 'VSEndless_GPU_Render_Engine/__init__.py' in files

                if has_addon_dir and has_init:
                    print("  ✅ Proper add-on directory structure")
                    print(f"  📊 Total files in package: {len(files)}")
                else:
                    print("  ❌ Incorrect package structure")

        except Exception as e:
            print(f"  ❌ Error reading package: {e}")
    else:
        print("  ❌ No package found - run package.py first")

def main():
    """Run all tests"""
    print("🚀 VSEndless APT Testing Suite")
    print("=" * 60)

    try:
        test_import_safety()
        test_apt_compliance()
        test_blender_compatibility()
        test_package_structure()

        print("\n" + "=" * 60)
        print("🎯 Test Summary:")
        print("✅ = Pass, ⚠️ = Warning, ❌ = Fail, 🔶 = Partial")
        print("\n📝 Next Steps:")
        print("1. Install package in Blender 4.5+")
        print("2. Test in Video Sequence Editor")
        print("3. Try AI features (if dependencies available)")
        print("4. Test basic rendering workflow")

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()