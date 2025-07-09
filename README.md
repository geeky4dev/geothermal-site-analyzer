# 🌋 Geothermal Site Feasibility Analyzer — Fullstack Web App  

---

## 🚀 Project Overview  

This project is a **simple Fullstack Web Application** that helps users evaluate the feasibility of a geothermal site based on location input.     
Users can input coordinates or click on a map, and the app returns a **feasibility score** using geological, terrain, and climate data.  

---

![geothermal](https://github.com/user-attachments/assets/13a012b3-0e35-4b0e-8e4f-eda8f2b65b0c)


---

## 🛠️ Tech Stack  

- **Frontend:** React + Leaflet.js (interactive map, user input, data visualization)    
- **Backend:** Flask (Python) + Geospatial libraries (GDAL, Rasterio, GeoPandas)    
- **Data Sources:**    
  - Global Heat Flow raster data    
  - Tectonic Plate Boundaries (GeoJSON)    
  - Surface Temperature raster data    
  - Groundwater datasets (optional / future)  

---

## 📁 Folder Structure  

/geothermal-site-feasibility-analyzer  
│
├── backend/  
│ │ ├── app.py # Flask backend API server  
│ │ ├── data/  
│ │ │ ├── heatflow.tif # Heat flow raster file  
│ │ │ ├── temperature.tif # Temperature raster file  
│ │ │ └── tectonics.geojson # Tectonic plates GeoJSON  
│ ├── requirements.txt # Python dependencies  
│ └── utils.py # Helper functions (optional)  
│
├── frontend/  
│ │ ├── src/  
│ │ │ ├── components/  
│ │ │ │ └── MapInput.jsx # React Leaflet map input component  
│ │ │ ├── App.jsx # React main app component  
│ │ │ ├── index.jsx # React app entry point  
│ │ │ └── styles.css # CSS styles  
│ ├── public/  
│ ├── package.json # Frontend dependencies and scripts  
│ └── vite.config.js # Vite config (if using Vite)  
│
├── README.md # This file  
└── .gitignore # Git ignore rules  


---

## 🧑‍💻 Step-by-Step Development Guide  

### 1️⃣ Backend Setup — Flask API  

- Create a virtual environment:    
  
  python3 -m venv venv  
  source venv/bin/activate   # Linux/macOS  
  venv\Scripts\activate      # Windows  

Install dependencies:  

pip install flask flask-cors rasterio geopandas shapely pyproj numpy  
Prepare your data folder with the required GeoTIFF and GeoJSON files.  

Write app.py to:  

Load geospatial data on startup  
Provide API endpoints /api/score (POST) and /api/test-sites (GET)  
Implement raster sampling and feasibility scoring logic  
Run Flask backend:

flask run --port=5001  

2️⃣ Frontend Setup — React + Leaflet  
Initialize React app (using Vite or Create React App):  

npm create vite@latest frontend --template react  
cd frontend  
npm install  
Install Leaflet and Axios:  

npm install leaflet react-leaflet axios  
Create MapInput.jsx component:  

Show interactive map  
Allow user to click or enter coordinates  
Fetch feasibility score from Flask backend  
Display results dynamically  
Update App.jsx to use MapInput.  
Start frontend dev server:  

npm run dev  

3️⃣ Connect Frontend & Backend  
Ensure Flask backend has CORS enabled to allow calls from frontend:  

from flask_cors import CORS  
app = Flask(__name__)  
CORS(app)  
Use Axios or Fetch in React to call backend API endpoints.  

Test with /api/test-sites GET endpoint to fetch predefined test coordinates and their feasibility scores.  

4️⃣ Testing & Debugging  
Run backend with debug=True for detailed error logs.  
Check browser console for CORS or network errors.  
Verify geospatial data files paths and projections are correct.  
Use Postman or curl to test backend endpoints independently.  

5️⃣ Optional Improvements  
Add user authentication  
Add groundwater data integration   
Improve UI/UX with better visualization and tooltips  
Deploy backend and frontend on cloud platforms (Heroku, Render, Vercel)  
Add caching for geospatial queries  

📚 Useful Links  
React Docs  
Leaflet Docs  
Flask Docs  
Flask-CORS  
Rasterio Docs  
GeoPandas Docs  

🙌 Contributing
Feel free to open issues or submit pull requests! All contributions welcome.
________________________________________
📄 License
MIT License — use freely, with attribution. Contributions welcome!  
Made by geeky4dev with ☀️ and ❤️ for renewable energy enthusiasts!  

🙌 Happy coding and may your geothermal sites be super feasible! 🌍🔥    
