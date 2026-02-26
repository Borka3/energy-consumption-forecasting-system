import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

export const showData = async (startDate, endDate) => {
    return axios.post(`${API_URL}/api/results/forecasts`, {
        startDate: startDate,
        endDate: endDate
    });
};



