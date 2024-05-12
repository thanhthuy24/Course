import axios from "axios";

const BASE_URL = 'http:/192.168.2.5:8000/';

export const endpoints = {
    'categories': '/categories/',
    'courses': '/courses/',
    'lessons': (courseId) => `/courses/${courseId}/lessons/`,
    'lesson-detail': (lessonId) => `/lessons/${lessonId}/`,
    'comments': (lessonId) => `/lessons/${lessonId}/comments/`
};

export default axios.create(
    {
        baseURL: BASE_URL
});
