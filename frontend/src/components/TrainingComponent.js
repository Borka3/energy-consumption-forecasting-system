import React, { useState } from 'react';
import { trainModel } from '../services/TrainingService';
import '../components.css';

const TrainingComponent = () => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [loading, setLoading] = useState(false);
    const [layers, setLayers] = useState(2);
    const [neurons, setNeurons] = useState(64);
    const [epochs, setEpochs] = useState(50);
    const [batchSize, setBatchSize] = useState(32);
    const [learningRate, setLearningRate] = useState(0.001);
    const [activation, setActivation] = useState('relu');
    const [optimizer, setOptimizer] = useState('adam');
    const [metrics, setMetrics] = useState(null);
    const [message, setMessage] = useState(null);

    const handleSubmit = async () => {
        if (!startDate || !endDate) {
            setMessage(" Pick both dates!");
            return;
        }

        if (startDate > endDate) {
            setMessage(" End date must be after start date!");
            return;
        }

        const hyperparams = {
            layers,
            neurons,
            epochs,
            batch_size: batchSize,
            learning_rate: learningRate,
            activation,
            optimizer
        };

        setLoading(true);
        setMessage(null);
        setMetrics(null);

        try {
            const response = await trainModel(startDate, endDate, hyperparams);
            console.log("Backend response:", response.data);

            setMessage(response.data.message || " Training successfully completed!");
            setMetrics(response.data.data?.metrics || null);

            setStartDate('');
            setEndDate('');
        } catch (error) {
            setMessage(error.response?.data?.message || " Error during training");
            setMetrics(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="component-container">
            <h2 className="component-title"> Training Model</h2>

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

            <div className="form-group">
                <label>Layers:</label>
                <input type="number" value={layers} onChange={(e) => setLayers(e.target.value)} />
            </div>

            <div className="form-group">
                <label>Neurons per layer:</label>
                <input type="number" value={neurons} onChange={(e) => setNeurons(e.target.value)} />
            </div>

            <div className="form-group">
                <label>Epochs:</label>
                <input type="number" value={epochs} onChange={(e) => setEpochs(e.target.value)} />
            </div>

            <div className="form-group">
                <label>Batch size:</label>
                <input type="number" value={batchSize} onChange={(e) => setBatchSize(e.target.value)} />
            </div>

            <div className="form-group">
                <label>Learning rate:</label>
                <input
                    type="number"
                    step="0.0001"
                    value={learningRate}
                    onChange={(e) => setLearningRate(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label>Activation:</label>
                <select value={activation} onChange={(e) => setActivation(e.target.value)}>
                    <option value="relu">relu</option>
                    <option value="sigmoid">sigmoid</option>
                    <option value="tanh">tanh</option>
                </select>
            </div>

            <div className="form-group">
                <label>Optimizer:</label>
                <select value={optimizer} onChange={(e) => setOptimizer(e.target.value)}>
                    <option value="adam">adam</option>
                    <option value="sgd">sgd</option>
                    <option value="rmsprop">rmsprop</option>
                </select>
            </div>

            <button
                onClick={handleSubmit}
                disabled={loading}
                className="form-button training-button"
            >
                {loading ? "Training..." : "TRAIN MODEL"}
            </button>

            {message && (
                <div className="metrics-box">
                    <h3>{message}</h3>
                    {metrics && (
                        <>
                            <p>Train MAPE: {metrics.train_mape.toFixed(2)}%</p>
                            <p>Test MAPE: {metrics.test_mape.toFixed(2)}%</p>
                            <p>Train RMSE: {metrics.train_rmse.toFixed(2)}</p>
                            <p>Test RMSE: {metrics.test_rmse.toFixed(2)}</p>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

export default TrainingComponent;