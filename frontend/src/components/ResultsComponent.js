import React, { useState } from 'react';
import { showData } from '../services/ResultsService';

import '../components.css';


const ResultsComponent = () => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [loading, setLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [predictedData, setPredictedData] = useState([]);

    const handleSubmit = async () => {
        if (!startDate || !endDate) {
            alert("Pick both dates!");
            return;
        }
        if (startDate > endDate) {
            alert("End date must be after start date!");
            return;
        }

        setLoading(true);
        try {
            const response = await showData(startDate, endDate);
            setPredictedData(response.data.data.forecasts || []);
            setShowModal(true);
        } catch (error) {
            alert(error.response?.data?.message || "Error loading data");
        } finally {
            setLoading(false);
        }
    };

    const closeModal = () => {
        setShowModal(false);
        setPredictedData([]);
    };

    return (
        <div className="component-container">
            <h2 className="component-title"> Results</h2>

            <div className="form-group">
                <label>Start date:</label>
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="form-input"
                />
            </div>

            <div className="form-group">
                <label>End date:</label>
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="form-input"
                />
            </div>

            <button
                onClick={handleSubmit}
                disabled={loading}
                className="form-button results-button"
            >
                {loading ? "Loading..." : "SHOW DATA"}
            </button>

            {showModal && (
                <div className="modal-overlay" onClick={closeModal}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Forecast Data</h3>
                            <button onClick={closeModal} className="modal-close-btn">✕</button>
                        </div>

                        <div className="modal-body">
                            {predictedData.length > 0 && (
                                <table className="data-table">
                                    <thead>
                                        <tr>
                                            <th>Timestamp</th>
                                            <th>Predicted Load (MW)</th>
                                            <th>Location</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {predictedData.map((item, index) => (
                                            <tr key={index}>
                                                <td>{item.timestamp}</td>
                                                <td>{item.predicted_load?.toFixed(2)}</td>
                                                <td>{item.location}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            )}
                        </div>

                        <div className="modal-footer">
                            <button onClick={closeModal} className="close-modal-btn">
                                CLOSE
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ResultsComponent;