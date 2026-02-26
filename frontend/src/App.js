import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LayoutComponent from './components/LayoutComponent';
import DataImportComponent from './components/DataImportComponent';
import TrainingComponent from './components/TrainingComponent';
import ForecastComponent from './components/ForecastComponent';
import ResultsComponent from './components/ResultsComponent';
import './App.css';
import './components.css';


function App() {
    return (
        <Router>
            <LayoutComponent>
                <Routes>
                    <Route path="/" element={<Navigate to="/data" replace />} />
                    <Route path="/data" element={<DataImportComponent />} />
                    <Route path="/training" element={<TrainingComponent />} />
                    <Route path="/forecast" element={<ForecastComponent />} />
                    <Route path="/results" element={<ResultsComponent />} />
                </Routes>
                

            </LayoutComponent>
        </Router>
    );
}

export default App;