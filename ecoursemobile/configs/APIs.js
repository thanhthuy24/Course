import axios from "axios";

const BASE_URL = 'http:/192.168.2.5:8000/';

export const endpoints = {
    'categories': '/categories/',
    'courses': '/courses/'
};

export default axios.create(
    {
        baseURL: BASE_URL
});
