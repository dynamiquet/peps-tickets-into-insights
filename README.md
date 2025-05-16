# 📊 PEPS Ticket Into Insight Project 📊

Turning raw event ticket data into actionable insights for smarter resource planning at Carleton College’s PEPS department.

## 🔍 Overview

This project analyzes event ticket data from TeamDynamix (TDX) used by PEPS (Presentation, Events, and Production Support) to uncover patterns in event scheduling, workload distribution, and resource demand. Our goal is to provide clear, visual tools to help the department better anticipate and manage logistical needs.

---
## 🛠️ How to Use


1. **Install dependencies**  
   Run the following in your terminal:  

   > pip install -r requirements.txt


2. **Generating plots**

    Run the following command to generate plots using matplotlib and Seaborn libraries.
    
    > python3 Scripts/plot_tdx_peps.py
    

    Feel free to change functions in the function `main`  in file `plot_tdx_peps` to choose what plots you want to generate.

## 📁 Project Structure

```
.
├── Data/                 # Raw and processed data files
├── Scripts/              # Python scripts for data processing and analysis
├── Results/              # Output visualizations, reports, and summaries
├── README.md             # Project overview and documentation
└── requirements.txt      # Python dependencies for the project
```

---

## ⚙️ Technologies Used

- **Python**: Data processing and visualization
- **Pandas**: Data wrangling
- **Matplotlib & Seaborn**: Charting and visualizations
- **Google Apps Script**: Cleaning and exporting data from Google Sheets
---

## 📈 Key Visualizations

- Heatmaps of event frequency by week of term and day
- Bubble graphs showing venue activity over time
- Bar charts of most used locations
- Time-based trends for resource planning

---

## 💡 Lessons Learned

- Clean, well-labeled data is everything
- Visuals must match the **story you’re trying to tell**
- Collaboration between technical and operational stakeholders = key

---

## 🙋‍♀️ Team

- **Dynamique Twizere** ('27)
- **Auiannce Euwing** ('26)
- **Paula Lackie** — Supervisor and mentor

---

## 📄 License

This project is for educational and departmental use at Carleton College. If you're interested in using or adapting it, feel free to reach out to @plackie @wiebkekuhn 