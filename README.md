# EXIF Annotator

This script processes JPG images by adding a black border at the bottom containing EXIF information arranged in two lines:
- Line 1: Capture date, camera model, and lens model
- Line 2: Technical details (focal length, f-stop, shutter speed, and ISO)

## Requirements

- Python 3.x
- Pillow library
- exif library
- pytest (for running tests)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The script requires an input directory containing the JPG images to process:

```bash
python process_images.py /path/to/your/images
```

Optional arguments:
- `-s`, `--subfolder`: Name of the subfolder to create in the input directory (default: "images with exif")
- `-o`, `--output_dir`: Full path to a custom output directory (if you want to save outside the input directory)

Examples:
```bash
# Use default subfolder "images with exif" in input directory
python process_images.py /path/to/your/images

# Specify a custom subfolder name
python process_images.py /path/to/your/images -s "processed_photos"

# Save to a completely different location
python process_images.py /path/to/your/images -o /path/to/output
```

The script will:
- Process all JPG files in the specified input directory
- By default, save the processed images in an "images with exif" subfolder within the input directory
- Add a 110-pixel high black border at the bottom with EXIF information

## Testing

The project includes a comprehensive test suite. To run the tests:

```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run a specific test
python -m pytest tests/test_process_images.py::test_missing_exif_data
```

The test suite covers:
- Basic functionality (image processing, border addition)
- EXIF data extraction and formatting
- Error handling (missing files, invalid directories)
- File format support (different extensions)
- Unicode filename support
- Multiple file processing

## Output

The processed images will contain the following EXIF information in the border:

Top line:
- Capture date and time
- Camera model
- Lens model

Bottom line:
- Focal length (mm)
- F-stop (f/number)
- Shutter speed (fraction of a second)
- ISO value

If any EXIF data is not available, it will be marked as "N/A". 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 