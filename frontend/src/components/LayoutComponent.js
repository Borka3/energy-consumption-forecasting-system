import React from 'react';
import { Link } from 'react-router-dom';
import '../components.css';

const LayoutComponent = ({ children }) => {
    return (
        <div className="layout-container">
            <header className="layout-header">
                <h1 className="layout-title">⚡ Electricity Forecast</h1>
                <nav className="layout-nav">
                    <Link to="/data" className="layout-link">Import Data</Link>
                    <Link to="/training" className="layout-link">Training</Link>
                    <Link to="/forecast" className="layout-link">Forecast</Link>
                    <Link to="/results" className="layout-link">Results</Link>
                </nav>
            </header>
            
            <main className="layout-main">
                {children}
            </main>
        </div>
    );
};

export default LayoutComponent;