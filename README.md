# Project Calculator

## Overview
This project is a comprehensive calculator and utility tool developed as a 12th grade project. It is built using **Python** and the **KivyMD** framework, aiming to provide a cross-platform, modern, and user-friendly experience. The goal is to evolve this project into a "Swiss knife" of tools, offering a wide range of functionalities beyond basic calculations.

## About KivyMD and Python GUI

### What is KivyMD?
[KivyMD](https://kivymd.readthedocs.io/en/latest/) is an open-source library that provides Material Design components for the [Kivy](https://kivy.org/) framework. Kivy is a Python library for rapid development of applications that make use of innovative user interfaces, such as multi-touch apps. KivyMD extends Kivy by adding ready-to-use widgets following Google's Material Design guidelines, making it easier to create visually appealing and consistent GUIs.

**Key Features of KivyMD:**
- Material Design widgets (buttons, dialogs, navigation drawers, etc.)
- Cross-platform support (Windows, macOS, Linux, Android, iOS)
- Highly customizable and extensible
- Active community and extensive documentation

### Why Python for GUI?
Python is a versatile and beginner-friendly programming language. Using Python for GUI development allows for rapid prototyping and easy maintenance. With frameworks like Kivy and KivyMD, developers can create modern, touch-friendly, and cross-platform applications with minimal effort.

## Project Features
- Standard calculator functions
- Date and time calculations
- Currency conversion
- History tracking
- Modular design for future expansion

## Planned Evolution
This project is intended to grow into a multi-tool application, incorporating features such as:
- Unit conversion
- Scientific calculator
- Financial tools
- Customizable themes
- And more!

## Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project-calculator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure
```
project-calculator/
├── main.py           # Main application logic
├── main_app.py       # App entry point
├── widgets.py        # Custom widgets
├── page.py           # Page management
├── properties.py     # App properties
├── settings.py       # User settings
├── solve.py          # Calculation logic
├── history.py        # History management
├── config.json       # Configuration file
├── requirements.txt  # Python dependencies
├── images/           # UI images and icons
└── ...
```

## Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Calculator Page
![Calculator Page](screenshots/calculator.png)

### Date Calculation Page
![Date Calculation Page](screenshots/date_calc.png)

### Currency Converter Page
![Currency Converter Page](screenshots/currency.png)

*Add screenshots of additional pages as the project evolves.*

## Contributing
Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or suggestions.

## License
This project is licensed under the MIT License.

## Acknowledgements
- [Kivy](https://kivy.org/)
- [KivyMD](https://kivymd.readthedocs.io/en/latest/)
- Python community

---
*This project was created as a 12th grade project and is planned to evolve into a powerful cross-platform utility tool.*

