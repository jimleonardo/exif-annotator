import os
import pytest
from PIL import Image
from exif import Image as ExifImage
import shutil

@pytest.fixture
def test_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path

@pytest.fixture
def sample_image(test_dir):
    """Create a sample image with known dimensions."""
    img_path = test_dir / "test.jpg"
    # Create a 100x100 black image
    img = Image.new('RGB', (100, 100), color='black')
    img.save(img_path, 'JPEG')
    return img_path

@pytest.fixture
def output_dir(test_dir):
    """Create an output directory for processed images."""
    out_dir = test_dir / "output"
    out_dir.mkdir(exist_ok=True)
    return out_dir

@pytest.fixture
def cleanup():
    """Cleanup function to run after tests."""
    yield
    # Clean up any test directories that might have been created
    test_dirs = ['processed_images', 'images with exif', 'output']
    for d in test_dirs:
        if os.path.exists(d):
            shutil.rmtree(d) 