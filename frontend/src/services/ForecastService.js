import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;


export const beginForecast = async (startDate, days ) => {
    return axios.post(`${API_URL}/api/forecast/generate`, {
        startDate,
        days: parseInt(days),
        
    });
};

