import React, { useState } from 'react';
import { sendLoadData, sendWeatherData, sendHolidaysData } from '../services/DataService';

const DataImportComponent = () => {
    const [loadData, setLoadData] = useState([]);
    const [weatherData, setWeatherData] = useState([]);
    const [holidayFile, setHolidayFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleLoadFiles = (event) => {
        const files = event.target.files;
        const filesArray = Array.from(files);
        setLoadData(filesArray);
        
        console.log(`Selected ${filesArray.length} CSV files`);
    };

    const handleWeatherFiles = (event) => {
        const files = event.target.files;
        const filesArray = Array.from(files);
        setWeatherData(filesArray);
    };

    const handleHolidayFile = (event) => {
        const selectedFile = event.target.files[0];
        setHolidayFile(selectedFile);
    };

    const handleSubmitData = async () => {
        if (loadData.length === 0 && weatherData.length === 0 && !holidayFile) {
            alert("No data to send!");
            return;
        }

        setLoading(true);

        try {
            
            if (loadData.length > 0) {
                await sendLoadData(loadData);
                alert(`Load data uploaded! ${loadData.length} files processed.`);
            }

            
            if (weatherData.length > 0) {
                await sendWeatherData(weatherData);
                alert(`Weather data uploaded! ${weatherData.length} files processed.`);
            }

            
            if (holidayFile) {
                await sendHolidaysData(holidayFile);
                alert("Holidays data uploaded!");
            }

        } catch (error) {
            alert(error.response?.data?.message || "Error uploading data");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="component-container">
            <h2 className="component-title"> Import Data</h2>
            
            
            <div className="form-group">
                <label>Load data (CSV):</label>
                <input 
                    type="file" 
                    webkitdirectory="true" 
                    multiple 
                    onChange={handleLoadFiles}
                    className="form-input"
                    accept=".csv"
                />
                {loadData.length > 0 && (
                    <div className="file-info">
                        Selected: {loadData.length} CSV files
                        <br />
                        <small>First: {loadData[0].name}</small>
                    </div>
                )}
            </div>

            
            <div className="form-group">
                <label>Weather data (CSV):</label>
                <input 
                    type="file" 
                    webkitdirectory="true" 
                    multiple 
                    onChange={handleWeatherFiles}
                    className="form-input"
                    accept=".csv"
                />
                {weatherData.length > 0 && (
                    <div className="file-info">
                        Selected: {weatherData.length} CSV files
                    </div>
                )}
            </div>

            
            <div className="form-group">
                <label>Holidays data (Excel):</label>
                <input 
                    type="file" 
                    webkitdirectory="true" 
                    onChange={handleHolidayFile}
                    className="form-input"
                    accept=".xlsx,.xls"
                />
                {holidayFile && (
                    <div className="file-info">
                        Selected: {holidayFile.name}
                    </div>
                )}
            </div>

            <button 
                onClick={handleSubmitData}
                disabled={loading}
                className="form-button data-import-button"
            >
                {loading ? "Uploading..." : "SEND DATA"}
            </button>
        </div>
    );
};

export default DataImportComponent;
