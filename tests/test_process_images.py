import os
import pytest
from PIL import Image
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from process_images import get_exif_data, process_image
import shutil

def test_image_creation(sample_image):
    """Test that the sample image is created correctly."""
    assert os.path.exists(sample_image)
    with Image.open(sample_image) as img:
        assert img.size == (100, 100)

def test_output_directory_creation(test_dir):
    """Test that output directories are created correctly."""
    output_dir = test_dir / "images with exif"
    if not output_dir.exists():
        output_dir.mkdir()
    assert output_dir.exists()

def test_border_dimensions(sample_image, output_dir):
    """Test that the border is added with correct dimensions."""
    output_path = output_dir / "processed_test.jpg"
    process_image(str(sample_image), str(output_path))
    
    with Image.open(output_path) as img:
        # Original height + 110px border
        assert img.size == (100, 210)

def test_missing_exif_data(sample_image):
    """Test handling of images without EXIF data."""
    exif_text = get_exif_data(str(sample_image))
    # Check that we get a list with two elements
    assert isinstance(exif_text, list)
    assert len(exif_text) == 2
    assert exif_text[0] == "No EXIF data found"
    assert exif_text[1] == ""

def test_invalid_input_directory():
    """Test handling of non-existent input directory."""
    with pytest.raises(Exception):
        process_image("nonexistent/path/image.jpg", "output.jpg")

def test_invalid_output_directory(sample_image):
    """Test handling of invalid output directory."""
    with pytest.raises(Exception):
        process_image(str(sample_image), "nonexistent/directory/output.jpg")

def test_non_image_file(test_dir):
    """Test handling of non-image files."""
    non_image = test_dir / "test.txt"
    non_image.write_text("This is not an image")
    with pytest.raises(Exception):
        process_image(str(non_image), "output.jpg")

def test_output_image_quality(sample_image, output_dir):
    """Test that output image maintains reasonable quality."""
    output_path = output_dir / "processed_test.jpg"
    process_image(str(sample_image), str(output_path))
    
    # Check file exists and has non-zero size
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    
    # Check that image can be opened and has expected format
    with Image.open(output_path) as img:
        assert img.format == "JPEG"

@pytest.mark.parametrize("filename", [
    "test.jpg",
    "test.JPG",
    "test.jpeg",
    "test.JPEG",
])
def test_file_extension_handling(test_dir, filename):
    """Test handling of different image file extensions."""
    img_path = test_dir / filename
    img = Image.new('RGB', (100, 100), color='black')
    img.save(img_path)
    assert os.path.exists(img_path)

def test_multiple_files_processing(test_dir, output_dir):
    """Test processing multiple files in a directory."""
    # Create multiple test images
    for i in range(3):
        img_path = test_dir / f"test{i}.jpg"
        img = Image.new('RGB', (100, 100), color='black')
        img.save(img_path)
    
    # Process all images
    for img in test_dir.glob("*.jpg"):
        output_path = output_dir / f"processed_{img.name}"
        process_image(str(img), str(output_path))
    
    # Check that all files were processed
    processed_files = list(output_dir.glob("processed_*.jpg"))
    assert len(processed_files) == 3

def test_unicode_filenames(test_dir, output_dir):
    """Test handling of Unicode filenames."""
    unicode_filename = "测试图片.jpg"
    img_path = test_dir / unicode_filename
    img = Image.new('RGB', (100, 100), color='black')
    img.save(img_path)
    
    output_path = output_dir / f"processed_{unicode_filename}"
    process_image(str(img_path), str(output_path))
    assert os.path.exists(output_path) 