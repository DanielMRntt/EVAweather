import 'dotenv/config';
import {get} from 'env-var';

export const envs = {
    PORT: get('PORT').default('80').asPortNumber(),
    PUBLIC_PATH: get('PUBLIC_PATH').default('public').asString(),
    WEATHER_API_KEY: get('WEATHER_API_KEY').required().asString(),
    WEATHER_API_BASE_URL: get('WEATHER_API_BASE_URL').default('https://api.openweathermap.org/data/2.5/').asString(),
    WEATHER_API_GEO_URL: get('WEATHER_API_GEO_URL').default('https://api.openweathermap.org/geo/1.0/direct').asString(),

    POSTGRES_URL: get('POSTGRES_URL').required().asString(),
    POSTGRES_DB_NAME: get('POSTGRES_DB').required().asString(),
    POSTGRES_USER: get('POSTGRES_USER').required().asString(),
    POSTGRES_PASS: get('POSTGRES_PASSWORD').required().asString(),
}