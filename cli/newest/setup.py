from setuptools import setup

setup(
    name="video-processor",
    version="0.1.0",
    py_modules=["main"],  # Specify the single module (main.py)
    install_requires=[
        "pillow>=9.0.0",
        "imagehash>=4.2.0",
        "opencv-python>=4.5.0",
    ],
    entry_points={
        "console_scripts": [
            "video-processor = main:main",  # Maps CLI command to main:main()
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="CLI tool for video processing with keyframe and HLS stream management.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/video-processor",  # Optional: Replace with your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust license as needed
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)