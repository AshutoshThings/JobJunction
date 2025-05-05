# Job Junction

🚀 **Live Demo**: [https://404lab.pythonanywhere.com/](https://404lab.pythonanywhere.com/)

Job Junction is a lightweight platform that connects **labour contractors** with **available workers**. It uses a simple call-based registration system for workers and provides an easy-to-use interface for contractors to hire them at fixed wages.

## 🌟 Features

- 📞 **Worker Availability via Missed Call**  
  Workers register themselves as available by simply giving a missed call. Their numbers are recorded in a JSON file.

- 🧑‍💼 **Contractor Web Interface**  
  Contractors can view available workers and hire them based on availability.

- 📦 **Simple JSON-Based Storage**  
  Data is stored in lightweight JSON files:
  - `workers.json`: Contains registered worker details
  - `available_workers_calls.json`: Records recent missed calls (available workers)
  - `contractors.json`: Registered contractors

- ⚡ **Quick Deployment**  
  Run the backend with a simple Python script – no complex infrastructure needed.
  
---

## 🛠 Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/ashutoshthings/JobJunction.git
   cd JobJunction
2. Install the required dependencies:

```bash
   pip install -r requirements.txt
```
3. Run the application:
  ```bash
   python app.py
```
#Project Structure
```
job-junction/
├── templates/                  # all the htmls 
├── static/                     # contains all the image files
├── available_workers_calls.json  # Stores missed call data (available workers)
├── contractors.json            # List of contractors
├── workers.json                # Registered worker details
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── app.py                      # Main server application 
```
