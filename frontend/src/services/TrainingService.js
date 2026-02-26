import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

export const trainModel = async (startDate, endDate, hyperparams) => {
    return axios.post(`${API_URL}/api/training/train`, {
      startDate,
      endDate,
      hyperparams
    });
  };




