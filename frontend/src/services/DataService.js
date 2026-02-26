import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL;

export const sendLoadData = async (files) => {
    const chunkSize = 50; 
    const numberOfChunks = Math.ceil(files.length / chunkSize);
    
    console.log(`Uploading ${files.length} files in ${numberOfChunks} chunks`);
    
    for (let i = 0; i < numberOfChunks; i++) {
        const start = i * chunkSize;
        const end = (i + 1) * chunkSize;
        const chunk = files.slice(start, end);
        const formData = new FormData();
        
        for (let j = 0; j < chunk.length; j++) {
            formData.append(`file${j + 1}`, chunk[j]);
        }
        
        try {
            const response = await axios.post(`${API_URL}/api/data/load`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            });
            console.log(`Chunk ${i + 1}/${numberOfChunks} uploaded:`, response.data);
        } catch(err) {
            console.error(`Error uploading chunk ${i + 1}:`, err);
            throw err;
        }
    }
};

export const sendWeatherData = async (files) => {
    const formData = new FormData();
    for(let i = 0; i < files.length; i++) {
        formData.append(`file${i + 1}`, files[i]);
    }
    
    return axios.post(`${API_URL}/api/data/weather`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

export const sendHolidaysData = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return axios.post(`${API_URL}/api/data/holidays`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};